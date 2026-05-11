# ---------- IMPORTS ---------- #

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from forms import NewTaskForm, EditTaskForm, NewListForm
from dotenv import load_dotenv
from datetime import datetime
import secrets
import os

# Import ".env" file.
load_dotenv()

# ---------- INIT APP ---------- #

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

# ---------- INIT DATABASE ---------- #

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///project.db"
db.init_app(app)

# ---------- DATABASE TABLES ---------- #

class TodoList(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25), nullable=False)

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="todo_list",
        cascade="all, delete-orphan"
    )


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25), nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[str] = mapped_column(String(250))
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    list_id: Mapped[int] = mapped_column(
        ForeignKey("todo_list.id"),
        nullable=False
    )

    todo_list: Mapped["TodoList"] = relationship(
        back_populates="tasks"
    )

with app.app_context():
    db.create_all()

# ---------- ROUTES ---------- #

@app.route("/")
def index():
    lists = db.session.execute(db.select(TodoList)).scalars().all()

    return render_template("index.html", lists=lists)

@app.route("/<int:task_id>")
def task(task_id):
    task_ = db.session.get(Task, task_id)

    return render_template("task.html", task=task_)

@app.route("/new-task", methods=["GET", "POST"])
def new_task():

    if request.method == "POST":

        new_task_ = Task (
            title=request.form.get("title"),
            date_created=datetime.now(),
            notes=request.form.get("notes"),
            completed=False,
            list_id=request.form.get("list_id")
        )
        db.session.add(new_task_)
        db.session.commit()

        return redirect(url_for("index"))

    lists = db.session.execute(db.select(TodoList).order_by(TodoList.title)).scalars().all()
    form = NewTaskForm()
    form.list_id.choices = [(lst.id, lst.title) for lst in lists]

    return render_template("new-task.html", form=form)

@app.route("/edit-task/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    if request.method == "POST":

        task_to_edit = db.session.get(Task, task_id)
        task_to_edit.title = request.form.get("title")
        task_to_edit.notes = request.form.get("notes")
        task_to_edit.list_id = request.form.get("list_id")
        db.session.commit()

        return redirect(url_for("index"))

    lists = db.session.execute(db.select(TodoList).order_by(TodoList.title)).scalars().all()
    form = EditTaskForm()
    form.list_id.choices = [(lst.id, lst.title) for lst in lists]

    task_ = db.session.get(Task, task_id)

    return render_template("edit-task.html", form=form, task=task_)

@app.route("/new-list", methods=["GET", "POST"])
def new_list():

    if request.method == "POST":

        new_list_ = TodoList (
            title=request.form.get("title"),
        )
        db.session.add(new_list_)
        db.session.commit()

        return redirect(url_for("index"))

    form = NewListForm()

    return render_template("new-list.html", form=form)


@app.route("/complete-task/<task_id>", methods=["POST"])
def complete_task(task_id):
    task_ = db.session.get(Task, task_id)
    task_.completed = True
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete-task/<task_id>", methods=["POST"])
def delete_task(task_id):
    db.session.delete(db.session.get(Task, task_id))
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete-list/<list_id>", methods=["POST"])
def delete_list(list_id):
    db.session.delete(db.session.get(TodoList, list_id))
    db.session.commit()

    return redirect(url_for("index"))

# ---------- MAIN LOOP ---------- #

if __name__ == "__main__":
    app.run()
