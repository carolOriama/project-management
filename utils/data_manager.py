import os
import json
from models.user import User
from models.project import Project
from models.task import Task

class DataManager:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.projects_file = os.path.join(data_dir, "projects.json")
        self.tasks_file = os.path.join(data_dir, "tasks.json")

    def load_data(self):
        users = []
        users_dict = {}
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, "r") as f:
                    data = json.load(f)
                    User._id_counter = 0
                    for item in data:
                        user = User(
                            name=item["name"],
                            email=item["email"],
                            user_id=item.get("id")
                        )
                        users.append(user)
                        users_dict[user.email] = user
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            users = []
            users_dict = {}

        projects = []
        projects_dict = {}
        try:
            if os.path.exists(self.projects_file):
                with open(self.projects_file, "r") as f:
                    data = json.load(f)
                    for item in data:
                        project = Project(
                            title=item["title"],
                            description=item.get("description", ""),
                            due_date=item["due_date"],
                            owner_email=item["owner_email"]
                        )
                        projects.append(project)
                        projects_dict[project.title] = project
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            projects = []
            projects_dict = {}

        tasks = []
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, "r") as f:
                    data = json.load(f)
                    for item in data:
                        task = Task(
                            title=item["title"],
                            project_title=item["project_title"],
                            status=item.get("status", "Pending"),
                            assigned_to=item.get("assigned_to")
                        )
                        tasks.append(task)
                        if task.project_title in projects_dict:
                            projects_dict[task.project_title].add_task(task)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            tasks = []

        return users, projects, tasks

    def save_data(self, users, projects, tasks):
        os.makedirs(self.data_dir, exist_ok=True)

        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "name": user.name,
                "email": user.email
            })

        projects_data = []
        for project in projects:
            projects_data.append({
                "title": project.title,
                "description": project.description,
                "due_date": project.due_date,
                "owner_email": project.owner_email
            })

        tasks_data = []
        for task in tasks:
            tasks_data.append({
                "title": task.title,
                "project_title": task.project_title,
                "status": task.status,
                "assigned_to": task.assigned_to
            })

        with open(self.users_file, "w") as f:
            json.dump(users_data, f, indent=4)

        with open(self.projects_file, "w") as f:
            json.dump(projects_data, f, indent=4)

        with open(self.tasks_file, "w") as f:
            json.dump(tasks_data, f, indent=4)
