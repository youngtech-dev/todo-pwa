# ✅ Flask Todo App

A simple task management web app built with Flask and SQLAlchemy. Organise your tasks into lists, add notes, mark them complete, and keep things tidy with full CRUD support.

---

## Features

- 📋 Create and delete **todo lists**
- ➕ Add, edit, and delete **tasks** within lists
- ✔️ Mark tasks as **complete**
- 🗒️ Attach **notes** to any task
- 💾 Persistent storage via **SQLite** (or any SQLAlchemy-compatible database)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | [Flask](https://flask.palletsprojects.com/) |
| Database ORM | [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) + SQLAlchemy |
| Forms | Flask-WTF / WTForms |
| Server | Gunicorn (production) |
| Config | python-dotenv |

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/youngtech-dev/todo-pwa.git
   cd todo-pwa
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:
   ```env
   SQLALCHEMY_DATABASE_URI=sqlite:///project.db
   ```
   Omit this variable to use the default SQLite database.

5. **Run the app**
   ```bash
   python main.py
   ```

   The app will be available at `http://127.0.0.1:5000`.

---

## Project Structure

```
.
├── main.py            # App factory, database models, and routes
├── forms.py           # WTForms form definitions
├── requirements.txt   # Python dependencies
├── templates/         # Jinja2 HTML templates
│   ├── index.html
│   ├── task.html
│   ├── new-task.html
│   ├── edit-task.html
│   └── new-list.html
└── .env               # Environment variables (not committed)
```

---

## Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Home — view all lists and tasks |
| GET | `/<task_id>` | View a single task |
| GET / POST | `/new-task` | Create a new task |
| GET / POST | `/edit-task/<task_id>` | Edit an existing task |
| GET / POST | `/new-list` | Create a new list |
| POST | `/complete-task/<task_id>` | Mark a task as complete |
| POST | `/delete-task/<task_id>` | Delete a task |
| POST | `/delete-list/<list_id>` | Delete a list and its tasks |

---

## Deployment

To run with Gunicorn in production:

```bash
gunicorn main:app
```

---

## License

This project is open source and available under the [MIT License](LICENSE).
