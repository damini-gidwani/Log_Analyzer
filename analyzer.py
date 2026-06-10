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
    args = parser.parse_args()
    level = args.level.upper() if args.level else None
    data = read_logs(args.log)
    top_n = args.top
    

    if data is None:
        return

    counts, total_logs, logs_list = analyze_logs(data)

    print_report(counts, total_logs)
    
    if level and level not in ["INFO", "WARNING", "ERROR"]:
        print("Invalid level.\n Use INFO, WARNING, or ERROR")
        return
    
    if level:
        print(f"\n- TOP {top_n} {level} LOGS -\n")
        top = top_logs(logs_list, level)
        
        for msg, count in top[:top_n]:
            print(f"{msg} -> {count}")


if __name__ == "__main__":
    main()