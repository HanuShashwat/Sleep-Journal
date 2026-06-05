# Sleep Journal

A simple, interactive command-line application written in Python to track your daily sleep duration. It calculates your sleep duration, stores the data locally using SQLite, and provides insights such as your monthly average sleep.

## Features

- **Add Sleep Records**: Input your sleep time and wake time (in 24-hour format). The program automatically figures out if your sleep started the previous day and calculates the exact duration.
- **View Monthly Averages**: Easily look up your average sleep duration for the current month or any past month.
- **View All Records**: See a chronological list of all your past sleep records.
- **Local Database**: All your sleep entries are saved to a local `sleep_journal.db` SQLite database file, so your data persists between sessions.

## Prerequisites

- Python 3.x
- No external libraries required (uses Python's standard library).

## How to Run

1. Open your terminal or command prompt.
2. Navigate to the folder containing the script:
   ```bash
   cd "path/to/Sleep Journal"
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. Follow the interactive menu to log your sleep and view your statistics!

## Usage Example

When you run the application, you will be presented with a menu:

```
=== Sleep Tracker Menu ===
1. Add Sleep Record
2. View Monthly Average
3. View All Records
4. Exit
```

**Adding a Record:**
```
--- Add New Sleep Record ---
Enter wake-up date (YYYY-MM-DD) [default: 2026-06-05]: 
Enter sleep time (HH:MM, 24-hour format): 23:30
Enter wake time (HH:MM, 24-hour format): 07:15

Record saved! You slept for 7 hours and 45 minutes.
```
