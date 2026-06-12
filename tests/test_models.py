import pytest
from models.person import Person
from models.user import User
from models.project import Project
from models.task import Task

def test_person_validation():
    p = Person("John Kiriamiti", "johnkiriamniti@example.com")
    assert p.name ==  "John Kiriamiti"
    assert p.email == "johnkiriamniti@example.com"

    with pytest.raises(ValueError):
        p.name = "   "
    with pytest.raises(ValueError):
        p.name = "12345"
    with pytest.raises(ValueError):
        p.email = "invalidemail"
    with pytest.raises(TypeError):
        p.name = 123

def test_user_inheritance_and_id():
    User._id_counter = 0
    u1 = User("Alex Smith", "johnkiriamniti@example.com")
    u2 = User("Minerva Ekwe", "minervaekwe@example.com")
    assert u1.id == 1
    assert u2.id == 2
    assert isinstance(u1, Person)
    
    u3 = User("Chipphirah Wambugu", "chipphirahwambugu@example.com", user_id=10)
    assert u3.id == 10
    assert User._id_counter == 10
    
    u4 = User("Danny", "danny@gmail.com")
    assert u4.id == 11

def test_project_validation():
    proj = Project("CLI Tool", "A great project", "2026-06-30", "alex@example.com")
    assert proj.title == "CLI Tool"
    assert proj.description == "A great project"
    assert proj.due_date == "2026-06-30"
    assert proj.owner_email == "alex@example.com"

    with pytest.raises(ValueError):
        proj.due_date = "2026/06/30"
    with pytest.raises(ValueError):
        proj.owner_email = "invalid_email"
    with pytest.raises(ValueError):
        proj.title = ""

def test_task_validation_and_completion():
    task = Task("Implement CLI", "CLI Tool", status="Pending", assigned_to="merlinpendragon@gmail.com")
    assert task.title == "Implement CLI"
    assert task.status == "Pending"
    assert task.assigned_to == "merlinpendragon@gmail.com"

    task.complete()
    assert task.status == "Completed"

    with pytest.raises(ValueError):
        task.status = "In Progress"

def test_contributors():
    proj = Project("CLI Tool", "A great project", "2026-06-30", "merlinpendragon@gmail.com")
    task1 = Task("Implement CLI", "CLI Tool", status="Pending", assigned_to="merlinpendragon@gmail.com")
    task2 = Task("Write Tests", "CLI Tool", status="Pending", assigned_to="charlenemuthoni@gmail.com")
    task3 = Task("Refactor", "CLI Tool", status="Pending", assigned_to=None)
    
    proj.add_task(task1)
    proj.add_task(task2)
    proj.add_task(task3)
    
    assert proj.contributors == ["merlinpendragon@gmail.com", "johnkiriamniti@example.com"]
