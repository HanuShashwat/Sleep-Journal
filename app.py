import sqlite3
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/records', methods=['GET'])
def get_records():
    conn = get_db_connection()
    records = conn.execute('SELECT * FROM sleep_records ORDER BY wake_date DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in records])

@app.route('/api/records', methods=['POST'])
def add_record():
    data = request.json
    wake_date_str = data.get('wake_date')
    sleep_time_str = data.get('sleep_time')
    wake_time_str = data.get('wake_time')

    if not wake_date_str or not sleep_time_str or not wake_time_str:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        wake_date = datetime.datetime.strptime(wake_date_str, "%Y-%m-%d").date()
        sleep_time_obj = datetime.datetime.strptime(sleep_time_str, "%H:%M").time()
        wake_time_obj = datetime.datetime.strptime(wake_time_str, "%H:%M").time()
    except ValueError:
        return jsonify({'error': 'Invalid date or time format'}), 400

    # Calculate duration
    sleep_dt = datetime.datetime.combine(wake_date, sleep_time_obj)
    if sleep_time_obj > wake_time_obj:
        sleep_dt = sleep_dt - datetime.timedelta(days=1)
        
    wake_dt = datetime.datetime.combine(wake_date, wake_time_obj)
    
    duration = wake_dt - sleep_dt
    duration_minutes = int(duration.total_seconds() / 60)
    
    if duration_minutes < 0:
        return jsonify({'error': 'Sleep duration cannot be negative'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sleep_records (wake_date, sleep_time, wake_time, duration_minutes)
        VALUES (?, ?, ?, ?)
    ''', (wake_date_str, sleep_time_str, wake_time_str, duration_minutes))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'duration_minutes': duration_minutes}), 201

@app.route('/api/average', methods=['GET'])
def get_average():
    month_str = request.args.get('month') # expected YYYY-MM
    if not month_str:
        month_str = datetime.date.today().strftime("%Y-%m")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT AVG(duration_minutes), COUNT(id)
        FROM sleep_records
        WHERE wake_date LIKE ?
    ''', (f"{month_str}-%",))
    
    result = cursor.fetchone()
    conn.close()
    
    avg_minutes = int(result[0]) if result[0] is not None else 0
    count = result[1] if result[1] is not None else 0
    
    return jsonify({
        'month': month_str,
        'average_minutes': avg_minutes,
        'count': count
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
