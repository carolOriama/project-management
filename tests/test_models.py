import pytest
from models.person import Person
from models.user import User
from models.project import Project
from models.task import Task

def test_person_validation():
    p = Person("Alex Smith", "alex@example.com")
    assert p.name == "Alex Smith"
    assert p.email == "alex@example.com"

    with pytest.raises(ValueError):
        p.name = "   "
    with pytest.raises(ValueError):
        p.name = "12345"  # name must contain at least one letter
    with pytest.raises(ValueError):
        p.email = "invalidemail"
    with pytest.raises(TypeError):
        p.name = 123

def test_user_inheritance_and_id():
    User._id_counter = 0
    u1 = User("Alex Smith", "alex@example.com")
    u2 = User("Bob Jones", "bob@example.com")
    assert u1.id == 1
    assert u2.id == 2
    assert isinstance(u1, Person)
    
    u3 = User("Charlie Brown", "charlie@example.com", user_id=10)
    assert u3.id == 10
    assert User._id_counter == 10
    
    u4 = User("Danny", "danny@example.com")
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
    task = Task("Implement CLI", "CLI Tool", status="Pending", assigned_to="alex@example.com")
    assert task.title == "Implement CLI"
    assert task.status == "Pending"
    assert task.assigned_to == "alex@example.com"

    task.complete()
    assert task.status == "Completed"

    with pytest.raises(ValueError):
        task.status = "In Progress"

def test_contributors():
    proj = Project("CLI Tool", "A great project", "2026-06-30", "alex@example.com")
    task1 = Task("Implement CLI", "CLI Tool", status="Pending", assigned_to="alex@example.com")
    task2 = Task("Write Tests", "CLI Tool", status="Pending", assigned_to="bob@example.com")
    task3 = Task("Refactor", "CLI Tool", status="Pending", assigned_to=None)
    
    proj.add_task(task1)
    proj.add_task(task2)
    proj.add_task(task3)
    
    assert proj.contributors == ["alex@example.com", "bob@example.com"]
