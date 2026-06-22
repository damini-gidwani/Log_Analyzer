# 📊 Log Analyzer (Dockerized + CLI Tool)

A Python-based log analysis tool that scans log files from a single file or a directory, categorizes logs (INFO, WARNING, ERROR), detects top issues, and generates reports in TXT or JSON format. The project is fully containerized using Docker + Docker Compose and includes logging, exception handling, and deployment automation.

---

## 🚀 Features

- Analyze single log file or entire directory
- Categorize logs into INFO, WARNING, ERROR
- Detect top recurring issues
- Generate output reports in .txt and .json formats
- Docker support (containerized execution)
- Docker Compose for easy deployment
- Logging using Python logging module
- Strong exception handling

---

## 📁 Project Structure

log_analyzer_project/
├── analyzer.py
├── generate_logs.py
├── dockerfile
├── docker-compose.yml
├── deploy.sh
├── logs/
├── log/
├── README.md

---

## ⚙️ Installation (Local)

git clone "https://github.com/damini-gidwani/Log_Analyzer.git"
cd log_analyzer_project
pip install -r requirements.txt

(If requirements.txt not present, no external dependencies needed)

---

## ▶️ Usage (CLI)

### Analyze single file
python analyzer.py --log logs/sample.log

### Analyze directory
python analyzer.py --dir log/

### Show top N issues
python analyzer.py --log logs/sample.log --top 5

### Save output report
python analyzer.py --log logs/sample.log --output report.txt
python analyzer.py --log logs/sample.log --output report.json

---

## 🐳 Docker Usage

### Build image
docker build -t log-analyzer .

### Run container
docker run log-analyzer --log logs/sample.log

---

## ⚙️ Docker Compose Usage

### Build + Run
docker compose up --build

### Run in background
docker compose up -d

### Stop containers
docker compose down

---

## 📜 Deployment Script

chmod +x deploy.sh
./deploy.sh

---

## 🧠 How It Works

1. Reads log file or directory
2. Splits logs into lines
3. Matches keywords:
   - ERROR → error, failed, critical, etc.
   - WARNING → timeout, retry, etc.
   - INFO → started, success, etc.
4. Counts occurrences
5. Finds top issues
6. Generates:
   - Console output
   - JSON or TXT report

---

## 📦 Output Example

=========================
LOG REPORT 📊
=========================

Total Logs : 120

INFO : 50
WARNING : 30
ERROR : 40

TOP ISSUES
error -> 20
failed -> 15
timeout -> 10

---

## 🐛 Error Handling

- Invalid file path handled safely
- Missing directory handled
- Permission errors logged
- Docker container errors handled

---

## 📌 Tech Stack

Python 3, argparse, logging, Docker, Docker Compose, Bash

---


## 👨‍💻 Author

Built for learning:
- Logging
- Docker
- System design basics
- File processing in Python