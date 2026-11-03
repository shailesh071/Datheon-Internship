# Python Internship Projects

<div align="center">

  <h2>Python Internship Projects</h2>
  <p>A collection of Python projects developed as part of my internship at Datheon.</p>

  <img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Projects-3-success?style=for-the-badge" alt="Projects">
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge" alt="Status">

</div>

---

## About This Repository

This repository contains three Python projects developed during my internship at Datheon. Each project focuses on different programming concepts, including basic game development, CSV file handling, portfolio calculations, and filesystem automation.

## Projects

### 1. Hangman Game

**Difficulty:** Beginner

A command-line word guessing game where players try to guess a hidden word one letter at a time before running out of attempts.

**Features:**
- Random word selection from an English word list.
- Tracks correctly and incorrectly guessed letters.
- Prevents repeated guesses.
- Displays a visual hangman using ASCII art.
- Limits the number of incorrect attempts.
- Allows players to play again.

**Technologies Used:**
- Python 3
- Random Module
- Pathlib Module
- File Handling

**Project Folder:** `Hangman/`

---

### 2. Stock Portfolio Performance Tracker

**Difficulty:** Beginner

A Python-based application that tracks stock investments by calculating total investment, current portfolio value, and profit or loss for each holding.

**Features:**
- Accepts stock ticker symbols, purchase prices, and share quantities.
- Loads available stock symbols from a CSV file.
- Retrieves current stock prices using the optional `yfinance` library.
- Supports manual price entry when live price retrieval is unavailable.
- Calculates investment value and profit or loss.
- Calculates percentage gain or loss.
- Saves portfolio summaries to a CSV file.

**Technologies Used:**
- Python 3
- CSV Module
- File Handling
- yfinance (Optional)

**Project Folder:** `Stock-Portfolio-Tracker/`

---

### 3. Automated File Organizer & Cleanup Utility

**Difficulty:** Intermediate

A Python-based utility that automatically organizes files into separate folders according to their file extensions. It helps keep directories clean and organized.

**Features:**
- Automatically identifies files by extension.
- Creates Documents, Images, Videos, Archives, Code, and Others folders.
- Moves files into their appropriate categories.
- Prevents duplicate filename conflicts.
- Handles permission and file operation errors.
- Skips directories and symbolic links.
- Maintains an activity log.
- Displays a summary of moved, skipped, and failed files.

**Technologies Used:**
- Python 3
- OS Module
- Shutil Module
- Pathlib Module
- Logging Module

**Project Folder:** `File-Organizer/`

---

## Repository Structure

```text
Datheon-Internship/
│
├── Hangman/
│   ├── hangman.py
│   ├── google-10000-english-no-swears.txt
│   └── README.md
│
├── Stock-Portfolio-Tracker/
│   ├── portfolio.py
│   ├── constituents.csv
│   └── README.md
|   └── portfolio_summary.csv
│
├── File-Organizer/
│   ├── organizer.py
│   └── README.md
│
└── README.md
```

## Requirements

- Python 3.x
- Code editor (VS Code recommended)
- Git (for repository management)

For the Stock Portfolio Tracker, install the optional dependency:

```bash
pip install yfinance
```

## How to Run

1. Clone this repository:

```bash
git clone https://github.com/shailesh071/Datheon-Internship.git
```

2. Open the repository folder.

3. Navigate to the project folder you want to run.

4. Execute the Python file:

```bash
python filename.py
```

Replace `filename.py` with the appropriate Python file name for the selected project.

## Learning Outcomes

Through these projects, I practiced:

- Python programming fundamentals.
- Functions, loops, and conditional statements.
- Working with external files and CSV data.
- Exception handling and input validation.
- Using Python standard libraries.
- Automating filesystem operations.
- Organizing and maintaining GitHub repositories.

## Acknowledgement

These projects were developed as part of my Python internship at **Datheon**.

---

<div align="center">
  <p>Developed by <strong>Shailesh</strong></p>
  <p>Python Internship Projects | 2026</p>
</div>
