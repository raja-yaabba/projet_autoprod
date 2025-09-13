from pymongo import MongoClient
from bson.objectid import ObjectId

class TaskDB:
    def __init__(self, uri="mongodb://mongo-db:27017/", db_name="todolist"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["tasks"]

    def get_all_tasks(self):
        return list(self.collection.find())

    def get_task(self, task_id):
        return self.collection.find_one({"_id": ObjectId(task_id)})

    def add_task(self, task, description):
        return self.collection.insert_one({
            "task": task,
            "description": description,
            "completed": False
        })

    def toggle_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            self.collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": {"completed": not task.get("completed", False)}}
            )

    def update_task(self, task_id, task_title, description):
        self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"task": task_title, "description": description}}
        )

    def delete_task(self, task_id):
        self.collection.delete_one({"_id": ObjectId(task_id)})
