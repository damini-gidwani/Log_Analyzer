# Log Analyzer

A Python CLI tool to analyze log files.

## Features

- Count INFO, WARNING, and ERROR logs
- Display top N log messages
- Filter logs by level
- Sort messages by frequency
- Command-line interface using argparse

## Usage

python analyzer.py --log logs/sample.log

python analyzer.py --log logs/sample.log --level ERROR

python analyzer.py --log logs/sample.log --level ERROR --top 5