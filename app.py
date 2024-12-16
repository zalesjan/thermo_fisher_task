import os
import requests
import sqlite3
import threading
import time
from flask import Flask, request, jsonify

# Configuration
GITHUB_API_URL = 'https://api.github.com/events'
EVENT_TYPES = ['WatchEvent', 'PullRequestEvent', 'IssuesEvent']
DB_NAME = 'events.db'
POLL_INTERVAL = 60  # Poll every 60 seconds

# Initialize the Flask app
app = Flask(__name__)

# Database setup

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_name TEXT,
            event_type TEXT,
            event_time INTEGER
        )
    ''')
    conn.commit()
    conn.close()


# Event streaming from GitHub

def fetch_github_events():
    """Continuously stream events from the GitHub API and store them in the database."""
    while True:
        try:
            response = requests.get(GITHUB_API_URL, headers={'Accept': 'application/vnd.github.v3+json'})
            response.raise_for_status()
            events = response.json()
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            for event in events:
                event_type = event.get('type')
                if event_type in EVENT_TYPES:
                    repo_name = event['repo']['name']
                    event_time = int(time.time())
                    cursor.execute(
                        'INSERT INTO events (repo_name, event_type, event_time) VALUES (?, ?, ?)',
                        (repo_name, event_type, event_time)
                    )
            
            conn.commit()
            conn.close()
            
            print("Successfully fetched and stored events.")
        except Exception as e:
            print(f"Error fetching events: {e}")
        
        time.sleep(POLL_INTERVAL)  # Wait for the next poll


# REST API endpoint

@app.route('/events/count', methods=['GET'])
def get_event_counts():
    """Handle GET requests to query the count of event types for a given repository."""
    repository = request.args.get('repository')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not repository or not start_time or not end_time:
        return jsonify({"error": "Missing required parameters: repository, start_time, and end_time."}), 400
    
    try:
        start_time = int(start_time)
        end_time = int(end_time)
    except ValueError:
        return jsonify({"error": "start_time and end_time must be integers representing UNIX timestamps."}), 400
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    event_counts = {}
    for event_type in EVENT_TYPES:
        cursor.execute(
            'SELECT COUNT(*) FROM events WHERE repo_name = ? AND event_type = ? AND event_time BETWEEN ? AND ?',
            (repository, event_type, start_time, end_time)
        )
        count = cursor.fetchone()[0]
        event_counts[event_type] = count
    
    conn.close()
    
    return jsonify({
        "repository": repository,
        "event_counts": event_counts
    })


# Main execution logic
if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Start the GitHub event streaming in a separate thread
    threading.Thread(target=fetch_github_events, daemon=True).start()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
