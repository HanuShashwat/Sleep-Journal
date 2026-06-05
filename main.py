import sqlite3
import datetime
import os
import sys

DB_NAME = "sleep_journal.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sleep_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wake_date TEXT NOT NULL,
            sleep_time TEXT NOT NULL,
            wake_time TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_record():
    print("\n--- Add New Sleep Record ---")
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    wake_date_str = input(f"Enter wake-up date (YYYY-MM-DD) [default: {today_str}]: ").strip()
    if not wake_date_str:
        wake_date_str = today_str
        
    try:
        wake_date = datetime.datetime.strptime(wake_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    sleep_time_str = input("Enter sleep time (HH:MM, 24-hour format): ").strip()
    wake_time_str = input("Enter wake time (HH:MM, 24-hour format): ").strip()

    try:
        sleep_time_obj = datetime.datetime.strptime(sleep_time_str, "%H:%M").time()
        wake_time_obj = datetime.datetime.strptime(wake_time_str, "%H:%M").time()
    except ValueError:
        print("Invalid time format. Please use HH:MM (24-hour).")
        return

    # Calculate duration
    # Assume sleep started on the previous day if sleep time is greater than wake time
    sleep_dt = datetime.datetime.combine(wake_date, sleep_time_obj)
    if sleep_time_obj > wake_time_obj:
        sleep_dt = sleep_dt - datetime.timedelta(days=1)
        
    wake_dt = datetime.datetime.combine(wake_date, wake_time_obj)
    
    duration = wake_dt - sleep_dt
    duration_minutes = int(duration.total_seconds() / 60)
    
    if duration_minutes < 0:
        print("Error: Sleep duration cannot be negative.")
        return
        
    hours = duration_minutes // 60
    minutes = duration_minutes % 60
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sleep_records (wake_date, sleep_time, wake_time, duration_minutes)
        VALUES (?, ?, ?, ?)
    ''', (wake_date_str, sleep_time_str, wake_time_str, duration_minutes))
    conn.commit()
    conn.close()
    
    print(f"\nRecord saved! You slept for {hours} hours and {minutes} minutes.")

def view_monthly_average():
    print("\n--- View Monthly Average ---")
    current_month_str = datetime.date.today().strftime("%Y-%m")
    month_str = input(f"Enter month (YYYY-MM) [default: {current_month_str}]: ").strip()
    if not month_str:
        month_str = current_month_str
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # SQLite uses string matching for dates formatted as YYYY-MM-DD
    cursor.execute('''
        SELECT AVG(duration_minutes), COUNT(id)
        FROM sleep_records
        WHERE wake_date LIKE ?
    ''', (f"{month_str}-%",))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0] is not None:
        avg_minutes = int(result[0])
        count = result[1]
        hours = avg_minutes // 60
        minutes = avg_minutes % 60
        print(f"\nAverage sleep for {month_str}: {hours} hours and {minutes} minutes (based on {count} records).")
    else:
        print(f"\nNo records found for {month_str}.")

def view_all_records():
    print("\n--- All Sleep Records ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT wake_date, sleep_time, wake_time, duration_minutes FROM sleep_records ORDER BY wake_date DESC')
    records = cursor.fetchall()
    conn.close()
    
    if not records:
        print("No records found.")
        return
        
    for idx, row in enumerate(records, 1):
        wake_date, sleep_time, wake_time, dur_min = row
        hours = dur_min // 60
        minutes = dur_min % 60
        print(f"{idx}. {wake_date}: Slept {sleep_time} -> Woke up {wake_time} | Duration: {hours}h {minutes}m")

def main():
    init_db()
    
    while True:
        print("\n=== Sleep Tracker Menu ===")
        print("1. Add Sleep Record")
        print("2. View Monthly Average")
        print("3. View All Records")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            add_record()
        elif choice == '2':
            view_monthly_average()
        elif choice == '3':
            view_all_records()
        elif choice == '4':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
