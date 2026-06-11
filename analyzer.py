import argparse


def read_logs(log_file):
    try:
        with open(log_file, "r") as file:
            return file.read()

    except FileNotFoundError:
        print(f"Error: '{log_file}' not found.")
        return None


def analyze_logs(data):
    logs_list = data.splitlines()

    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    for log in logs_list:
        if log.startswith("INFO"):
            counts["INFO"] += 1

        elif log.startswith("WARNING"):
            counts["WARNING"] += 1

        elif log.startswith("ERROR"):
            counts["ERROR"] += 1

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

def top_logs(logslist,level):
    top_er={}
    
    for log in logslist:
        if log.startswith(level):
            msg=log.replace(level+" ","",1)
            if msg in top_er:
                top_er[msg]+=1
            else:
                top_er[msg]=1
                
    sorted_logs = sorted(
    top_er.items(),
    key=lambda item: item[1],
    reverse=True
    )
    return sorted_logs
        
def build_report(counts, total_logs, logs_list, level=None, top_n=5):
    report = ""

    report += "\n=========================\n"
    report += "     LOG REPORT 📊\n"
    report += "=========================\n\n"

    report += f"Total Logs : {total_logs}\n\n"

    report += f"INFO    : {counts['INFO']}\n"
    report += f"WARNING : {counts['WARNING']}\n"
    report += f"ERROR   : {counts['ERROR']}\n"

    report += "\n=========================\n"

    if level:
        top = top_logs(logs_list, level)

        report += f"\nTOP {top_n} {level} LOGS\n\n"

        for msg, count in top[:top_n]:
            report += f"{msg} -> {count}\n"

    return report            

def main():
    parser = argparse.ArgumentParser(description="-- Log Analyzer --")
    parser.add_argument("--log", required=True)
    parser.add_argument("--level")
    parser.add_argument(
    "--top",
    type=int,
    default=5,
    help="Show top N logs"
    )
    parser.add_argument("--output",help="file in which report will appear!!!")
    args = parser.parse_args()
    level = args.level.upper() if args.level else None
    data = read_logs(args.log)
    top_n = args.top
    out_f = args.output
    
    if data is None:
        return

    counts, total_logs, logs_list = analyze_logs(data)

    report = build_report(counts, total_logs, logs_list, level, top_n)
    
    if out_f:
        with open(out_f, "w" , encoding="utf-8") as f:
            f.write(report)
    else:
        print(report)


if __name__ == "__main__":
    main()