import uuid

class Task:
    def __init__(self, task, description):
        self._id = str(uuid.uuid4())
        self.task = task
        self.description = description
        self.completed = False

class TaskDB:
    def __init__(self):
        self.tasks = []

    def get_all_tasks(self):
        return self.tasks

    def get_task(self, task_id):
        return next((t for t in self.tasks if t._id == task_id), None)

    def add_task(self, task, description):
        self.tasks.append(Task(task, description))

    def toggle_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.completed = not task.completed

    def update_task(self, task_id, task_title, description):
        task = self.get_task(task_id)
        if task:
            task.task = task_title
            task.description = description

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t._id != task_id]
