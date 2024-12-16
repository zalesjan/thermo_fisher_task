# GitHub Event Count API

## Introduction

The **GitHub Event Count API** is a Python application that streams GitHub events, stores them in an SQLite database, and exposes a REST API that allows users to query the count of specific event types for a given repository within a specified time window.

This application continuously polls the [GitHub Events API](https://api.github.com/events) for `WatchEvent`, `PullRequestEvent`, and `IssuesEvent`, stores them in a local SQLite database, and allows users to query counts of these events using an easy-to-use HTTP API.

---

## Prerequisites

To run this application, you will need:

- **Python 3.x** installed on your system
- **pip** (Python package installer)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   **Note:** If `requirements.txt` is not present, you can manually install the dependencies:

   ```bash
   pip install flask requests
   ```

3. **Initialize the SQLite database** The database is automatically initialized when you run the application. No manual action is required.

---

## Usage

### 1. **Start the Application**

Run the following command to start the application:

```bash
python github_event_api.py
```

This will do the following:

- Initialize an SQLite database (`events.db`) to store event data.
- Start a Flask API server on [**http://localhost:5000**](http://localhost:5000).
- Start a background thread to continuously poll the GitHub Events API every 60 seconds.

### 2. **Query Event Counts**

To query the count of event types for a specific repository within a given time window, you can use the following HTTP GET request format:

**Endpoint:**

```
GET /events/count
```

**Query Parameters:**

| Parameter    | Type    | Required | Description                                  |
| ------------ | ------- | -------- | -------------------------------------------- |
| `repository` | string  | Yes      | The repository name (e.g., `python/cpython`) |
| `start_time` | integer | Yes      | The start time (UNIX timestamp)              |
| `end_time`   | integer | Yes      | The end time (UNIX timestamp)                |

**Example Request:**

```bash
curl "http://localhost:5000/events/count?repository=python/cpython&start_time=1638336000&end_time=1638412399"
```

**Example Response:**

```json
{
  "repository": "python/cpython",
  "event_counts": {
    "WatchEvent": 20,
    "PullRequestEvent": 15,
    "IssuesEvent": 10
  }
}
```

### 3. **Stopping the Application**

To stop the application, press **Ctrl+C** in the terminal.

---

## API Endpoints

### **GET /events/count**

Queries the count of event types for a specific repository within a given time window.

#### **Request Parameters**

| Parameter    | Description                                  |
| ------------ | -------------------------------------------- |
| `repository` | The repository name (e.g., `python/cpython`) |
| `start_time` | The start time as a UNIX timestamp           |
| `end_time`   | The end time as a UNIX timestamp             |

#### **Response**

The response will be a JSON object containing the count of the following event types:

- `WatchEvent`
- `PullRequestEvent`
- `IssuesEvent`

**Example Response:**

```json
{
  "repository": "python/cpython",
  "event_counts": {
    "WatchEvent": 20,
    "PullRequestEvent": 15,
    "IssuesEvent": 10
  }
}
```

**Error Response:**

```json
{
  "error": "Missing required parameters: repository, start_time, and end_time."
}
```

---

## Application Structure

```
├── github_event_api.py     # Main application script
├── events.db               # SQLite database (auto-created on first run)
├── requirements.txt        # Python dependencies (Flask, Requests, etc.)
└── README.md               # This README file
```

---

## How It Works

1. **Event Streaming**

   - A background thread fetches events from the [GitHub Events API](https://api.github.com/events) every 60 seconds.
   - Only `WatchEvent`, `PullRequestEvent`, and `IssuesEvent` are stored in the SQLite database.

2. **Data Storage**

   - The data is stored in a local SQLite database (`events.db`) with the following schema:

   ```sql
   CREATE TABLE IF NOT EXISTS events (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       repo_name TEXT,
       event_type TEXT,
       event_time INTEGER
   );
   ```

3. **API Endpoints**

   - Users can query the count of the event types (`WatchEvent`, `PullRequestEvent`, and `IssuesEvent`) for a specific repository and time range using the `/events/count` endpoint.

---

## Error Handling

- **Invalid Parameters:** If `repository`, `start_time`, or `end_time` are missing or improperly formatted, the API will return an error message with a 400 status code.
- **Request Failures:** If the GitHub API request fails, it logs an error message but continues polling.

---

## Logs and Debugging

- While the application is running, log messages will be printed to the console, providing updates on the event streaming process.
- Errors and exceptions are caught and displayed as logs.

---

## Assumptions

- The application only tracks events that occur after it starts. Historical events are not loaded.
- Only the event types `WatchEvent`, `PullRequestEvent`, and `IssuesEvent` are tracked.

---

## Possible Enhancements

- **Error Handling**: Add retry logic for API failures and exponential backoff.
- **Performance**: Use bulk inserts for database writes to improve performance.
- **Scalability**: Use a more robust database (e.g., PostgreSQL) for production systems.
- **Security**: Add rate-limiting, API authentication, and input validation.
- **Environment Variables**: Externalize configurations (API URL, poll interval) to environment variables.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

---

## Contact

If you have any questions or need support, please contact [Your Name] at [Your Email].

