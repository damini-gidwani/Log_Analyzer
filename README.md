# 📊 Log Analyzer CLI Tool

A simple Python-based CLI tool to analyze log files and generate reports.  
It can process a single log file or an entire directory of log files.

---

## 🚀 Features

- Analyze single `.log` file
- Analyze multiple log files in a directory
- Classify logs into:
  - INFO
  - WARNING
  - ERROR
- Find top recurring issues
- Export reports in:
  - JSON format
  - TXT format
- Simple command-line interface (CLI)

---

## 📁 Project Structure

log_analyzer_project/
│
├── log/                  # Directory for multiple log files
│   ├── app.log
│   ├── auth.log
│   └── docker.log
|
|
├── logs/                   # single log file storage
│   └── sample.log
│
│
├── analyzer.py           # Main Python CLI script (your code)
│
├── README.md             # Project documentation

---

## ⚙️ Requirements

- Python 3.x

No external libraries required.

---

## ▶️ How to Run

### 🔹 Analyze a single log file

```bash
python log_analyzer.py --log sample.log
```

### 🔹 Analyze a directory of log files

```bash
python log_analyzer.py --dir logs/
```

---

## 📤 Save Output to File

### Save as TXT

```bash
python log_analyzer.py --log sample.log --output report.txt
```

### Save as JSON

```bash
python log_analyzer.py --log sample.log --output report.json
```

---

## 🔢 Top Issues

Control number of top issues using `--top`:

```bash
python log_analyzer.py --log sample.log --top 10
```

(Default is 5)

---

## 📌 CLI Arguments

| Argument | Description |
|----------|-------------|
| `--log` | Path to single log file |
| `--dir` | Path to directory of log files |
| `--top` | Number of top issues |
| `--output` | Output file (.txt or .json) |

---

## ⚠️ Rules

- Provide either `--log` OR `--dir`
- Only `.txt` and `.json` output supported

