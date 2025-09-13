from flask import Flask, render_template, request, redirect, url_for
from model import Task, TaskDB

app = Flask(__name__)
db = TaskDB()

@app.route("/")
def index():
    tasks = db.get_all_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    description = request.form["description"]
    db.add_task(task, description)
    return redirect(url_for("index"))

@app.route("/check/<task_id>")
def check(task_id):
    db.toggle_task(task_id)
    return redirect(url_for("index"))

@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = db.get_task(task_id)
    if request.method == "POST":
        task_title = request.form["task"]
        description = request.form["description"]
        db.update_task(task_id, task_title, description)
        return redirect(url_for("index"))
    return render_template("edit.html", task=task)

@app.route("/delete/<task_id>", methods=["POST"])
def delete(task_id):
    db.delete_task(task_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
