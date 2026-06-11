# 📊 Log Analyzer CLI Tool

A Python-based Command Line Interface (CLI) tool that analyzes log files and generates structured reports in TXT and JSON formats.  
It helps in quickly understanding system logs by summarizing log levels and identifying frequently occurring log messages.


## 🚀 Features

- Read log files from a given path
- Count log levels:
  - INFO
  - WARNING
  - ERROR
- Find top occurring log messages (based on level filter)
- Generate human-readable **text report**
- Export structured **JSON report**
- CLI-based arguments using `argparse`
- Handles file errors safely


## 🧠 Tech Stack

- Python 3
- argparse (CLI handling)
- json module (data serialization)
- File handling (I/O operations)


## 📁 Project Structure

log_analyzer/
│
├── analyzer.py        # Main script
├── logs/
        - Sample.log
└── README.md


## ⚙️ How It Works

1. Reads the log file
2. Splits logs into individual lines
3. Counts log levels (INFO, WARNING, ERROR)
4. Finds most frequent log messages
5. Builds:
   - Text report OR
   - JSON report
6. Saves output file or prints in terminal


## ▶️ Usage

### 🔹 Basic Run (Prints report in terminal)
python analyzer.py --log logs/sample.log
 
### 🔹 Generate Text Report (.txt file)
python analyzer.py --log logs/sample.log --output report.txt

### 🔹 Generate JSON Report (.json file)
python analyzer.py --log logs/sample.log --output report.json

### 🔹 Filter logs by level + show top results
python analyzer.py --log logs/sample.log --level error --top 5

### 🔹 Combine everything (full analysis)
python analyzer.py --log logs/sample.log --level warning --top 3 --output report.json