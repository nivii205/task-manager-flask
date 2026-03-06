import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT,
        deadline TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        deadline = request.form["deadline"]

        cursor.execute(
            "INSERT INTO tasks (title, description,priority,deadline) VALUES (?, ?, ?, ?)",
            (title, description, priority, deadline)
        )
        conn.commit()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t[5]==1])
    pending_tasks = total_tasks - completed_tasks

    conn.close()
    return render_template("index.html", tasks=tasks,total_tasks=total_tasks,completed_tasks=completed_tasks,pending_tasks=pending_tasks)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        deadline = request.form["deadline"]

        cursor.execute(
            "UPDATE tasks SET title=?, description=?, priority=?, deadline=? WHERE id=?",
            (title, description, priority, deadline, id)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = cursor.fetchone()
    conn.close()

    return render_template("edit.html", task=task)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/complete/<int:id>")
def complete(id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET completed = 1 WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

 import os

 init_db()

 if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
