import os
import json
import pytest
from utils.data_manager import DataManager
from models.user import User
from models.project import Project
from models.task import Task

def test_missing_files_handling(tmp_path):
    dm = DataManager(str(tmp_path))
    users, projects, tasks = dm.load_data()
    assert users == []
    assert projects == []
    assert tasks == []

def test_malformed_json_handling(tmp_path):
    dm = DataManager(str(tmp_path))
    os.makedirs(str(tmp_path), exist_ok=True)
    with open(dm.users_file, "w") as f:
        f.write("invalid json data")
    users, projects, tasks = dm.load_data()
    assert users == []
    assert projects == []
    assert tasks == []

def test_save_and_load_flow(tmp_path):
    dm = DataManager(str(tmp_path))
    
    user = User("Alice Maina", "alicemaina@gmail.com")
    project = Project("CLI Tracker", "A tracking tool", "2026-12-31", "alicemaina@gmail.com")
    task1 = Task("Write code", "CLI Tracker", "Pending", "alicemaina@gmail.com")
    task2 = Task("Test code", "CLI Tracker", "Pending", None)
    
    users = [user]
    projects = [project]
    tasks = [task1, task2]
    
    dm.save_data(users, projects, tasks)
    
    new_dm = DataManager(str(tmp_path))
    new_users, new_projects, new_tasks = new_dm.load_data()
    
    assert len(new_users) == 1
    assert len(new_projects) == 1
    assert len(new_tasks) == 2
    
    assert new_users[0].name == "Alice Maina"
    assert new_users[0].email == "alicemaina@gmail.com"
    assert new_projects[0].title == "CLI Tracker"
    assert new_projects[0].owner_email == "alicemaina@gmail.com"
    
    assert len(new_projects[0].tasks) == 2
    assert new_projects[0].tasks[0].title == "Write code"
    assert new_projects[0].tasks[0].assigned_to == "alicemaina@gmail.com"
    assert new_projects[0].tasks[1].title == "Test code"
    assert new_projects[0].tasks[1].assigned_to is None
