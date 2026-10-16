# JSON Import and Validation App

A Flask web application for uploading and validating JSON files and storing valid records in PostgreSQL.

The application provides a simple web interface for importing structured data and viewing saved records.

## Project Purpose

This project demonstrates a basic data import workflow:

1. Upload a JSON file.
2. Validate its structure and field values.
3. Save valid records to PostgreSQL.
4. View stored records in a web interface.

The application can serve as a starting point for an internal data import tool. For example, it could help teams import event lists, scheduled tasks, or appointment records exported from another system.

Validation helps detect incorrectly formatted data before it is stored in the database.

## Features

- JSON file upload through a web form.
- Input validation using Pydantic.
- PostgreSQL integration through SQLAlchemy.
- A table view for stored records.
- HTML templates built with Jinja2.

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Pydantic
- HTML and Jinja2
- Gunicorn and nginx for Linux deployment

## Requirements

- Python 3.8+ or the version required by the installed dependencies
- PostgreSQL 12+
- Gunicorn and nginx for production deployment on Linux

## Installation and Setup

### 1. Install Python Dependencies

Open a terminal in the project directory.

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Create the PostgreSQL Database

Connect to PostgreSQL as an administrator, such as the `postgres` user.

Run the following commands separately:

```sql
CREATE DATABASE flask_db;
```

```sql
CREATE USER username WITH PASSWORD 'replace_with_a_secure_password';
```

```sql
GRANT ALL PRIVILEGES ON DATABASE flask_db TO username;
```

Next, connect to the `flask_db` database and run:

```sql
GRANT ALL ON SCHEMA public TO username;
```

In `psql`, you can switch databases with:

```text
\c flask_db
```

In pgAdmin, open a new Query Tool window for the `flask_db` database.

Replace the example username and password with your own credentials.

### 3. Configure Environment Variables

The `.env.example` file contains example configuration values without real credentials.

Copy it to `.env`.

#### Linux / macOS

```bash
cp .env.example .env
```

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Update the database connection string in `.env`:

```dotenv
DATABASE_URI=postgresql://username:replace_with_a_secure_password@localhost:5432/flask_db
```

Use the same database name, username, and password that you configured in PostgreSQL.

The connection URL must match the PostgreSQL driver installed by the project.

Keep `.env` private. Do not commit real passwords or other secrets to Git.

The `.env.example` file should remain in the repository so that other developers know which variables they need to configure.

Recommended `.gitignore` entries:

```gitignore
.env
.env.*
!.env.example

.venv/
__pycache__/
*.py[cod]
.idea/
```

### 4. Run Locally

```bash
python app.py
```

Open the address shown in the terminal.

Gunicorn and nginx are not required for local development.

### 5. Verify the Database Connection

From the project directory, start the Flask shell:

```bash
python -m flask --app app shell
```

Run:

```python
from sqlalchemy import text
from extensions import db

db.session.execute(text("SELECT 1")).scalar()
```

A result of `1` confirms that the application can execute a database query.

To check the PostgreSQL database name and user:

```python
db.session.execute(
  text("SELECT current_database(), current_user")
).one()
```

To check the full import workflow, upload the example JSON file and open the records page.

## Deployment with Gunicorn and nginx

The following instructions are intended for a Linux server.

### 1. Configure Gunicorn

Create `gunicorn.conf.py`:

```python
workers = 4
bind = "127.0.0.1:8000"
worker_class = "sync"
```

Start the application from the project directory with the virtual environment activated:

```bash
gunicorn -c gunicorn.conf.py app:app
```

The worker count is an example and should be adjusted for the server's resources.

### 2. Configure nginx

On an Ubuntu/Debian-style nginx installation, create:

```text
/etc/nginx/sites-available/flask_app
```

Add:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Replace `your_domain.com` with your domain or server address.

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

This is a basic HTTP deployment example. A production deployment should also include HTTPS, process supervision, logging, and appropriate access restrictions.

## Project Structure

```text
project/
├── app.py
├── config.py
├── extensions.py
├── models.py
├── schemas.py
├── routes.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── first.json
└── templates/
    ├── base.html
    ├── index.html
    ├── upload.html
    ├── entries.html
    └── about.html
```

- `app.py` — application entry point.
- `config.py` — application and database configuration.
- `extensions.py` — Flask extension initialization.
- `models.py` — SQLAlchemy database models.
- `schemas.py` — Pydantic validation schemas.
- `routes.py` — Blueprint routes for request handling.
- `requirements.txt` — Python dependencies.
- `.env.example` — environment configuration template without real credentials.
- `.env` — private local configuration, created during setup and excluded from Git.
- `first.json` — example JSON file for testing uploads.
- `templates/` — Jinja2 HTML templates.

## JSON Format

The uploaded file must contain a JSON array of objects.

Each object must include:

- `name` — a string shorter than 50 characters.
- `date` — a date and time in `YYYY-MM-DD_HH:mm` format.

Example:

```json
[
    {
        "name": "Team meeting",
        "date": "2026-10-20_10:30"
    },
    {
        "name": "Project review",
        "date": "2026-10-21_15:00"
    }
]
```

## Possible Use Cases

The application's name-and-date record format can be used as a starting point for:

- Importing event schedules from another system.
- Uploading appointment lists.
- Importing scheduled tasks.
- Validating exported JSON data before storing it.
- Replacing manual entry with a batch upload workflow.

These are possible applications of the project, not separate implemented modules.

## Ideas for Future Development

- Duplicate detection.
- Search and date filtering.
- Pagination for large datasets.
- A detailed validation report with record numbers and error descriptions.
- Import history with file names and timestamps.
- User authentication and access control.
- CSV export.
- Automated tests for validation and upload routes.

## Author

Vladislav Tarasevich
