# Multi-User Project Tracker CLI Tool

A Python-based command-line interface (CLI) application designed to manage and track users, projects, and tasks. Features rich terminal outputs, strict object-oriented data validation, many-to-many relationship tracking (via project contributors), and robust local JSON file persistence.

## Features

- **User Management**: Create and track users with auto-incremented IDs and email format validation.
- **Project Tracking**: Create projects assigned to owner users, with strict due-date (YYYY-MM-DD) parsing and validation.
- **Task Assignment & Completion**: Assign tasks to projects, optionally delegate them to contributors, and mark them completed.
- **Many-to-Many Relationships**: Dynamically computes project contributors based on task assignments.
- **Local Persistence**: Automatically saves and loads your graph of users, projects, and tasks to local JSON files in the `data/` directory.
- **Beautiful Console UI**: Leverages `rich` for elegant tables, color-coded statuses, and styled headers.

---

## Installation

### Method 1: Using Pipenv (Recommended)

1. Clone or navigate to the repository directory.
2. Install the dependencies and virtual environment:
   ```bash
   pipenv install --dev
   ```
3. Run CLI commands prefixing with `pipenv run`:
   ```bash
   pipenv run python3 main.py --help
   ```

### Method 2: Using standard `pip`

1. Clone or navigate to the repository directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run CLI commands directly:
   ```bash
   python3 main.py --help
   ```

---

## Usage Guide & Examples

All subcommands are fully documented in the help menu:
```bash
python3 main.py --help
```

### 1. User Commands

#### Add a new user
```bash
python3 main.py add-user --name "Alex Smith" --email "Jane Wainaina"
python3 main.py add-user --name "Bob Jones" --email "John Kiriamiti@gmail.com"
```

#### List all users
```bash
python3 main.py list-users
```

### 2. Project Commands

#### Create a project
Projects must specify an owner user (by email or name) and a valid due date (YYYY-MM-DD):
```bash
python3 main.py add-project --title "CLI Tool" --user "Alex Smith" --description "Build a CLI Tool" --due-date "2026-06-30"
```

#### List all projects (or filter by user)
```bash
python3 main.py list-projects
python3 main.py list-projects --user "Jane Wainaina"
```

### 3. Task Commands

#### Add a task to a project
Tasks can optionally be assigned to users (by email or name):
```bash
python3 main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "keithaustine@gmail.com"
python3 main.py add-task --project "CLI Tool" --title "Write Unit Tests"
```

#### List tasks in a project
```bash
python3 main.py list-tasks --project "CLI Tool"
```

#### Complete a task
```bash
python3 main.py complete-task --project "CLI Tool" --title "Implement add-task"
```

---

## Running Unit Tests

The test suite includes validation tests, persistence manager tests, and CLI subcommand integration tests.

Run tests using pytest:
```bash
pipenv run pytest
```
or
```bash
pytest
```
