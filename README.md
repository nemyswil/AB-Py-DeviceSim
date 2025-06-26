# 🧪 PLC Valve Simulation Engine

This Python-based simulation engine mimics industrial valve behavior by interacting with a Rockwell PLC using `pylogix`. It simulates open/close commands and updates feedback tags accordingly.

---

## 🚀 Features

- Reads valve definitions from an Excel spreadsheet (`devices.xlsm`)
- Simulates open/close valve behavior with feedback signals
- Communicates with Allen-Bradley PLCs using Ethernet/IP
- Realistic delays and threading support
- Bit-level digital I/O writing using `SINT` manipulation
- Easy-to-use and extend

---

## 📁 Project Structure

simulation_engine/
│

├── main.py # Simulation loop

├── valve.py # Valve logic

├── parser.py # Excel device parser

├── plc_io.py # PLC communication interface

├── devices.xlsm # Your valve definitions spreadsheet

├── requirements.txt # Project dependencies

├── setup_env.bat # One-click setup for Windows

└── README.md # You're here!


---

## 🛠️ Setup Instructions

### 🧵 Option 1: Manual Setup

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv SimVenv
   SimVenv\Scripts\activate
Install dependencies:


pip install -r requirements.txt
Run the simulation:


python main.py
🖱️ Option 2: One-Click Setup (Windows)
Double-click setup_env.bat in File Explorer. It will:

Create the virtual environment

Activate it

Install all dependencies

Launch the simulation

📊 Spreadsheet Format (devices.xlsm)
Your spreadsheet must have these column headers (case-sensitive):

Tag Name	DESCRIPTION	PLCIO Tags
XV1231	open	IOPLC0416:14:O.6
XV1231	open feedback	IOPLC0416:6:I.0
XV1231	closed feedback	IOPLC0416:6:I.1

Each valve should have at least:

An open command

An open feedback

A closed feedback

Incomplete valve definitions are skipped with a warning.

✅ Example Console Output

Loaded 21 valves. Starting simulation...
Running simulation... |
XV1231: Open command detected.
XV1231: Opened - Feedback updated.
📦 Regenerating requirements.txt
If you add new packages:


pip freeze > requirements.txt

💬 Questions?
Open an issue or contact your automation developer team.
