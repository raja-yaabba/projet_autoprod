from flask import Flask, render_template, request, redirect, url_for
from model import db, Task

app = Flask(__name__)

# Connexion MySQL via SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@mysql-db:3306/demo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Création des tables si elles n’existent pas
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_title = request.form["task"]
    description = request.form["description"]
    new_task = Task(task=task_title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/check/<int:task_id>")
def check(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = Task.query.get(task_id)
    if request.method == "POST":
        task.task = request.form["task"]
        task.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", task=task)

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
