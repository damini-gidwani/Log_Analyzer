import argparse
import json
import os

def log_files(direc):
    logFiles=[]
    for file in os.listdir(direc):
        if(file.endswith(".log")):
            path=os.path.join(direc,file)
            logFiles.append(path)
    return logFiles

def read_logs(log_file):
    try:
        with open(log_file, "r") as file:
            return file.read()

    except FileNotFoundError:
        print(f"Error: '{log_file}' not found.")
        return None


def analyze_logs(data):
    logs_list = data.splitlines()
    keywords = {
    "ERROR": [
        "error",
        "failed",
        "failure",
        "critical",
        "panic",
        "fatal",
        "denied",
        "refused"
    ],

    "WARNING": [
        "warning",
        "timeout",
        "deprecated",
        "retry"
    ],

    "INFO": [
        "started",
        "connected",
        "loaded",
        "accepted",
        "success"
    ]
    }
    counts = {
    "ERROR": 0,
    "WARNING": 0,
    "INFO": 0
    }
    for log in logs_list:
        log_lower = log.lower()

        if any(word in log_lower for word in keywords["ERROR"]):
            counts["ERROR"] += 1

        elif any(word in log_lower for word in keywords["WARNING"]):
            counts["WARNING"] += 1

        elif any(word in log_lower for word in keywords["INFO"]):
            counts["INFO"] += 1
    return counts, len(logs_list), logs_list


def print_report(counts, total_logs):
    print("\n=========================")
    print("     LOG REPORT 📊")
    print("=========================\n")

    print(f"Total Logs : {total_logs}\n")

    print(f"INFO    : {counts['INFO']}")
    print(f"WARNING : {counts['WARNING']}")
    print(f"ERROR   : {counts['ERROR']}")

    print("\n=========================")

def top_issues(logs_list, top_n=5):

    issues = {}

    keywords = [
        "error",
        "failed",
        "failure",
        "critical",
        "panic",
        "fatal",
        "denied",
        "refused",
        "timeout",
        "warning"
    ]

    for log in logs_list:
        log_lower = log.lower()

        for keyword in keywords:
            if keyword in log_lower:
                issues[keyword] = issues.get(keyword, 0) + 1
                break

    sorted_issues = sorted(
        issues.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_issues[:top_n]

def build_json(counts, total_logs, logs_list, top=None):

    data = {
        "total_logs": total_logs,
        "counts": counts,
        "logs": logs_list
    }

    if top:
        data["top_issues"] = top

    return data

def save_json(file_name, data):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)   

def build_report(counts, total_logs, top=None):
    report = ""

    report += "\n=========================\n"
    report += "     LOG REPORT 📊\n"
    report += "=========================\n\n"

    report += f"Total Logs : {total_logs}\n\n"

    report += f"INFO    : {counts['INFO']}\n"
    report += f"WARNING : {counts['WARNING']}\n"
    report += f"ERROR   : {counts['ERROR']}\n"

    if top:
        report += "\nTOP ISSUES\n\n"

        for issue, count in top:
            report += f"{issue} -> {count}\n"

    report += "\n=========================\n"

    return report

def analyze_directory(directory, top_n=5):
    all_logs = []
    files = log_files(directory)

    if len(files) == 0:
        return None, None, None

    overall_counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    total_files = 0

    for file in files:
        data = read_logs(file)

        if data is None:
            continue

        counts, total_logs, logs_list = analyze_logs(data)

        all_logs.extend(logs_list)

        overall_counts["INFO"] += counts["INFO"]
        overall_counts["WARNING"] += counts["WARNING"]
        overall_counts["ERROR"] += counts["ERROR"]

        total_files += 1

    top = top_issues(all_logs, top_n)

    return overall_counts, total_files, top
    
def build_directory_report(overall_counts, total_files, top):

    report = ""

    report += "\n====================\n"
    report += " OVERALL SUMMARY\n"
    report += "====================\n\n"

    report += f"Total Files : {total_files}\n\n"

    report += f"INFO    : {overall_counts['INFO']}\n"
    report += f"WARNING : {overall_counts['WARNING']}\n"
    report += f"ERROR   : {overall_counts['ERROR']}\n"

    report += "\nTOP ISSUES ACROSS ALL FILES\n\n"

    for issue, count in top:
        report += f"{issue} -> {count}\n"

    return report

def build_directory_json(overall_counts, total_files, top):

    return {
        "total_files": total_files,
        "counts": overall_counts,
        "top_issues": top
    }
    

def main():
    parser = argparse.ArgumentParser(description="-- Log Analyzer --")
    parser.add_argument("--log")
    parser.add_argument(
    "--top",
    type=int,
    default=5,
    help="Show top N logs"
    )
    parser.add_argument("--output",help="file in which report will appear!!!")
    parser.add_argument("--dir")
    
    args = parser.parse_args()
    
    if not args.log and not args.dir:
        parser.error("Provide either --log or --dir")
    
    top_n = args.top
    out_f = args.output
    
    if args.dir:
        result = analyze_directory(args.dir, top_n)

        if result == (None, None, None):
            print("No log files found in directory")
            return

        overall_counts, total_files, top = result
        
        print("\n====================")
        print(" OVERALL SUMMARY")
        print("====================\n")

        print(f"Total Files : {total_files}\n")

        print(f"INFO    : {overall_counts['INFO']}")
        print(f"WARNING : {overall_counts['WARNING']}")
        print(f"ERROR   : {overall_counts['ERROR']}")

        print("\nTOP ISSUES ACROSS ALL FILES\n")

        for issue, count in top:
            print(f"{issue} -> {count}")

        if out_f:

            report = build_directory_report(
                overall_counts,
                total_files,
                top
            )

            json_data = build_directory_json(
                overall_counts,
                total_files,
                top
            )

            if out_f.endswith(".txt"):
                with open(out_f, "w") as f:
                    f.write(report)        
            elif out_f.endswith(".json"):
                save_json(out_f, json_data)
            else:
                print("❌ Error: Only .json and .txt supported")
        return
    
    data = read_logs(args.log)
    
    if data is None:
        return

    counts, total_logs, logs_list = analyze_logs(data)
    
    top = top_issues(logs_list,top_n)
    
    print("\nTOP ISSUES:")
    for issue, count in top:
       print(f"{issue} -> {count}")

    report = build_report(counts, total_logs, top)
    json_data = build_json(counts, total_logs, logs_list, top)
    
    if out_f:

        if out_f.endswith(".json"):
            save_json(out_f, json_data)

        elif out_f.endswith(".txt"):
            with open(out_f, "w", encoding="utf-8") as f:
                f.write(report)

        else:
           print("❌ Error: Only .json and .txt supported")

    else:
        print(report)

if __name__ == "__main__":
    main()