# Sleep Journal (Web Application)

A modern, interactive web application written in Python (Flask) and React (Vite) to track your daily sleep duration. It calculates your sleep duration, stores the data locally using SQLite, and provides insights and visual trends.

## Features

- **Add Sleep Records**: Log your sleep time and wake time. The program automatically calculates the duration.
- **Beautiful Dashboard**: A rich, dark-mode glassmorphism interface.
- **Sleep Data Visualization**: View recent sleep trends via an interactive bar chart.
- **Monthly Averages**: Keep track of how well you're sleeping on average each month.
- **Local Database**: All your sleep entries are saved to a local `sleep_journal.db` SQLite database file.

## Prerequisites

- Node.js (v18+)
- Python 3.x

## How to Run

### 1. Start the Backend API (Python)

Open a terminal, navigate to the project directory, and run the backend:

```bash
# Install dependencies if you haven't already
pip install flask flask-cors

# Run the Flask API
python app.py
```

The backend will run on `http://127.0.0.1:5000/`.

### 2. Start the Frontend Web App (React)

Open a **new** terminal, navigate to the `frontend` folder, and start the Vite dev server:

```bash
cd frontend

# Install dependencies if you haven't already
npm install

# Run the dev server
npm run dev
```

Vite will provide a localhost URL (usually `http://localhost:5173`). Open that URL in your browser to start tracking your sleep!
