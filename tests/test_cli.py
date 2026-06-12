import sys
import pytest
from unittest.mock import patch
from main import main

def test_cli_help():
    with patch("sys.argv", ["main.py"]):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0

def test_cli_add_user_command(tmp_path):
    with patch("main.get_data_manager") as mock_gdm:
        from utils.data_manager import DataManager
        dm = DataManager(str(tmp_path))
        mock_gdm.return_value = dm
        
        with patch("sys.argv", ["main.py", "add-user", "--name", "Charlie", "--email", "charlie@example.com"]):
            main()
            
        users, _, _ = dm.load_data()
        assert len(users) == 1
        assert users[0].name == "Charlie"
        assert users[0].email == "charlie@example.com"

def test_cli_add_project_command(tmp_path):
    with patch("main.get_data_manager") as mock_gdm:
        from utils.data_manager import DataManager
        dm = DataManager(str(tmp_path))
        mock_gdm.return_value = dm
        
        with patch("sys.argv", ["main.py", "add-user", "--name", "Charlie", "--email", "charlie@example.com"]):
            main()
            
        with patch("sys.argv", ["main.py", "add-project", "--title", "CLI-App", "--user", "Charlie", "--description", "Project desc", "--due-date", "2026-06-30"]):
            main()
            
        _, projects, _ = dm.load_data()
        assert len(projects) == 1
        assert projects[0].title == "CLI-App"
        assert projects[0].description == "Project desc"
        assert projects[0].due_date == "2026-06-30"
        assert projects[0].owner_email == "charlie@example.com"

def test_cli_add_and_complete_task_command(tmp_path):
    with patch("main.get_data_manager") as mock_gdm:
        from utils.data_manager import DataManager
        dm = DataManager(str(tmp_path))
        mock_gdm.return_value = dm
        
        with patch("sys.argv", ["main.py", "add-user", "--name", "Charlie", "--email", "charlie@example.com"]):
            main()
        with patch("sys.argv", ["main.py", "add-project", "--title", "CLI-App", "--user", "Charlie", "--due-date", "2026-06-30"]):
            main()
        with patch("sys.argv", ["main.py", "add-task", "--project", "CLI-App", "--title", "Coding", "--assigned-to", "charlie@example.com"]):
            main()
            
        _, projects, tasks = dm.load_data()
        assert len(tasks) == 1
        assert tasks[0].title == "Coding"
        assert tasks[0].status == "Pending"
        assert tasks[0].assigned_to == "charlie@example.com"
        
        with patch("sys.argv", ["main.py", "complete-task", "--project", "CLI-App", "--title", "Coding"]):
            main()
            
        _, _, tasks_after = dm.load_data()
        assert tasks_after[0].status == "Completed"
