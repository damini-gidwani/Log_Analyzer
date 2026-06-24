import argparse
import json
import os
import re
import logging
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

KEYWORDS = {
    "ERROR": [
        "error", "failed", "failure", "critical",
        "panic", "fatal", "denied", "refused"
    ],
    "WARNING": [
        "warning", "timeout", "deprecated", "retry"
    ],
    "INFO": [
        "started", "connected", "loaded", "accepted", "success"
    ],
}


ISSUE_KEYWORDS = [
    "error", "failed", "failure", "critical", "panic",
    "fatal", "denied", "refused", "timeout", "warning"
]

_COMPILED = {
    level: [re.compile(rf"\b{re.escape(word)}\b") for word in words]
    for level, words in KEYWORDS.items()
}
_COMPILED_ISSUES = [
    (word, re.compile(rf"\b{re.escape(word)}\b")) for word in ISSUE_KEYWORDS
]


def _matches_any(patterns: list[re.Pattern], text: str) -> bool:
    return any(p.search(text) for p in patterns)


def log_files(direc: str) -> list[str]:
    try:
        if not os.path.exists(direc):
            logger.error(f"Directory not found: {direc}")
            return []

        if not os.path.isdir(direc):
            logger.error(f"Not a directory: {direc}")
            return []

        return [
            os.path.join(direc, f)
            for f in os.listdir(direc)
            if f.endswith(".log")
        ]

    except Exception as e:
        logger.error(f"dir error : {e}")
        return []


def read_logs(log_file: str) -> Optional[str]:
    logger.info(f"Reading {log_file} ...")
    try:
        if not os.path.exists(log_file):
            logger.error(f"File not found: {log_file}")
            return None

        with open(log_file, "r", encoding="utf-8") as file:
            return file.read()

    except PermissionError:
        logger.error(f"Permission denied: {log_file}")
        return None

    except Exception as e:
        logger.error(f"❌ Error reading file: {e}")
        return None



def analyze_logs(data: Optional[str]) -> tuple[dict[str, int], int, list[str]]:
    if not data:
        return {"INFO": 0, "WARNING": 0, "ERROR": 0}, 0, []

    logs_list = data.splitlines()
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}

    for log in logs_list:
        log_lower = log.lower()

        if _matches_any(_COMPILED["ERROR"], log_lower):
            counts["ERROR"] += 1
        elif _matches_any(_COMPILED["WARNING"], log_lower):
            counts["WARNING"] += 1
        elif _matches_any(_COMPILED["INFO"], log_lower):
            counts["INFO"] += 1

    return counts, len(logs_list), logs_list


def top_issues(logs_list: list[str], top_n: int = 5) -> list[tuple[str, int]]:
    issues: dict[str, int] = {}

    for log in logs_list:
        log_lower = log.lower()
        for keyword, pattern in _COMPILED_ISSUES:
            if pattern.search(log_lower):
                issues[keyword] = issues.get(keyword, 0) + 1
                break  # one keyword counted per line, avoids double-counting

    return sorted(issues.items(), key=lambda item: item[1], reverse=True)[:top_n]


def analyze_directory(
    directory: str, top_n: int = 5
) -> tuple[Optional[dict], Optional[int], Optional[list]]:
    files = log_files(directory)
    if not files:
        return None, None, None

    all_logs: list[str] = []
    overall_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    total_files = 0

    for file in files:
        data = read_logs(file)
        if data is None:
            continue

        counts, _, logs_list = analyze_logs(data)
        all_logs.extend(logs_list)

        for key in overall_counts:
            overall_counts[key] += counts[key]

        total_files += 1

    top = top_issues(all_logs, top_n)
    return overall_counts, total_files, top


def build_report(
    counts: dict[str, int],
    total: int,
    top: Optional[list[tuple[str, int]]] = None,
    *,
    mode: str = "file",
) -> str:
    if mode == "dir":
        title = " OVERALL SUMMARY"
        total_label = "Total Files"
    else:
        title = "     LOG REPORT 📊"
        total_label = "Total Logs"

    lines = [
        "\n=========================",
        title,
        "=========================\n",
        f"{total_label} : {total}\n",
        f"INFO    : {counts['INFO']}",
        f"WARNING : {counts['WARNING']}",
        f"ERROR   : {counts['ERROR']}",
    ]

    if top:
        header = "\nTOP ISSUES ACROSS ALL FILES\n" if mode == "dir" else "\nTOP ISSUES\n"
        lines.append(header)
        lines.extend(f"{issue} -> {count}" for issue, count in top)
    elif top is not None:
        lines.append("\n(no recurring issues found)")

    lines.append("\n=========================")
    return "\n".join(lines)


def build_json(
    counts: dict[str, int],
    total: int,
    top: Optional[list] = None,
    logs_list: Optional[list[str]] = None,
    *,
    mode: str = "file",
) -> dict:
    if mode == "dir":
        data = {"total_files": total, "counts": counts}
    else:
        data = {"total_logs": total, "counts": counts, "logs": logs_list or []}

    if top:
        data["top_issues"] = top

    return data


def save_json(file_name: str, data: dict) -> None:
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except PermissionError:
        logger.error(f"❌ Permission denied: {file_name}")
    except Exception as e:
        logger.error(f"❌ Error saving JSON: {e}")


def write_output(out_f: str, report: str, json_data: dict) -> None:
    if out_f.endswith(".json"):
        save_json(out_f, json_data)
    elif out_f.endswith(".txt"):
        with open(out_f, "w", encoding="utf-8") as f:
            f.write(report)
    else:
        logger.error("❌ Error: Only .json and .txt supported")


def run_file_mode(log_path: str, top_n: int, out_f: Optional[str]) -> None:
    data = read_logs(log_path)
    if data is None:
        return

    counts, total_logs, logs_list = analyze_logs(data)
    top = top_issues(logs_list, top_n)

    report = build_report(counts, total_logs, top, mode="file")
    json_data = build_json(counts, total_logs, top, logs_list, mode="file")

    if out_f:
        write_output(out_f, report, json_data)
    else:
        print(report)


def run_dir_mode(directory: str, top_n: int, out_f: Optional[str]) -> None:
    overall_counts, total_files, top = analyze_directory(directory, top_n)

    if overall_counts is None:
        logger.warning("No log files found in directory")
        return

    report = build_report(overall_counts, total_files, top, mode="dir")
    json_data = build_json(overall_counts, total_files, top, mode="dir")

    if out_f:
        write_output(out_f, report, json_data)
    else:
        print(report)


def main() -> None:
    logger.info("Log Analyzer started")
    parser = argparse.ArgumentParser(description="-- Log Analyzer --")
    parser.add_argument("--log", help="path to a single .log file")
    parser.add_argument("--dir", help="path to a directory of .log files")
    parser.add_argument("--top", type=int, default=5, help="show top N issues")
    parser.add_argument("--output", help="save report to a .txt or .json file")

    args = parser.parse_args()

    if not args.log and not args.dir:
        parser.error("Provide either --log or --dir")

    if args.log and args.dir:
        parser.error("Provide only one of --log or --dir, not both")

    if args.dir:
        run_dir_mode(args.dir, args.top, args.output)
    else:
        run_file_mode(args.log, args.top, args.output)

    logger.info("Log Analyzer ended successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\n❌ Process stopped by user")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
