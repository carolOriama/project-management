import os
import sys
import argparse
from models.user import User
from models.project import Project
from models.task import Task
from utils.data_manager import DataManager
from utils.helpers import (
    print_success,
    print_error,
    print_warning,
    print_header,
    console
)
from rich.table import Table

def get_data_manager():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    return DataManager(data_dir)

def find_user(users, query):
    """Finds a user by email or name (case-insensitive)."""
    for u in users:
        if u.email.lower() == query.lower():
            return u
    for u in users:
        if u.name.lower() == query.lower():
            return u
    return None

def find_project(projects, title):
    for p in projects:
        if p.title.lower() == title.lower():
            return p
    return None

def cmd_add_user(args, users, projects, tasks, dm):
    for u in users:
        if u.email.lower() == args.email.lower():
            print_error(f"User with email '{args.email}' already exists.")
            sys.exit(1)
    try:
        user = User(name=args.name, email=args.email)
        users.append(user)
        dm.save_data(users, projects, tasks)
        print_success(f"User '{user.name}' ({user.email}) successfully created with ID {user.id}!")
    except (ValueError, TypeError) as e:
        print_error(str(e))
        sys.exit(1)

def cmd_list_users(args, users, projects, tasks, dm):
    if not users:
        print_warning("No users found.")
        return
    table = Table(title="All Users", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Name", style="bold")
    table.add_column("Email")
    for u in users:
        table.add_row(str(u.id), u.name, u.email)
    console.print(table)

def cmd_add_project(args, users, projects, tasks, dm):
    owner = find_user(users, args.user)
    if not owner:
        print_error(f"User '{args.user}' not found. Please create the user first.")
        sys.exit(1)
    
    if find_project(projects, args.title):
        print_error(f"Project with title '{args.title}' already exists.")
        sys.exit(1)

    try:
        project = Project(
            title=args.title,
            description=args.description or "",
            due_date=args.due_date,
            owner_email=owner.email
        )
        projects.append(project)
        dm.save_data(users, projects, tasks)
        print_success(f"Project '{project.title}' successfully created for owner '{owner.name}'!")
    except (ValueError, TypeError) as e:
        print_error(str(e))
        sys.exit(1)

def cmd_list_projects(args, users, projects, tasks, dm):
    filtered_projects = projects
    if args.user:
        user = find_user(users, args.user)
        if not user:
            print_error(f"User '{args.user}' not found.")
            sys.exit(1)
        filtered_projects = [
            p for p in projects
            if p.owner_email.lower() == user.email.lower() or user.email.lower() in [c.lower() for c in p.contributors]
        ]
        title_str = f"Projects for {user.name} ({user.email})"
    else:
        title_str = "All Projects"

    if not filtered_projects:
        print_warning("No projects found.")
        return

    table = Table(title=title_str, show_header=True, header_style="bold magenta")
    table.add_column("Title", style="bold cyan")
    table.add_column("Owner Email")
    table.add_column("Due Date", style="green")
    table.add_column("Tasks (Comp/Total)", justify="center")
    table.add_column("Contributors", style="yellow")
    
    for p in filtered_projects:
        comp = sum(1 for t in p.tasks if t.status == "Completed")
        tot = len(p.tasks)
        tasks_status = f"{comp}/{tot}"
        contribs_str = ", ".join(p.contributors) if p.contributors else "None"
        table.add_row(p.title, p.owner_email, p.due_date, tasks_status, contribs_str)
    console.print(table)

def cmd_add_task(args, users, projects, tasks, dm):
    project = find_project(projects, args.project)
    if not project:
        print_error(f"Project '{args.project}' not found.")
        sys.exit(1)

    for t in project.tasks:
        if t.title.lower() == args.title.lower():
            print_error(f"Task '{args.title}' already exists in project '{project.title}'.")
            sys.exit(1)

    assignee_email = None
    if args.assigned_to:
        assignee = find_user(users, args.assigned_to)
        if not assignee:
            print_error(f"Assigned user '{args.assigned_to}' not found.")
            sys.exit(1)
        assignee_email = assignee.email

    try:
        task = Task(
            title=args.title,
            project_title=project.title,
            status="Pending",
            assigned_to=assignee_email
        )
        tasks.append(task)
        project.add_task(task)
        dm.save_data(users, projects, tasks)
        assignee_str = f"assigned to '{args.assigned_to}'" if assignee_email else "unassigned"
        print_success(f"Task '{task.title}' successfully added to project '{project.title}' ({assignee_str})!")
    except (ValueError, TypeError) as e:
        print_error(str(e))
        sys.exit(1)

def cmd_list_tasks(args, users, projects, tasks, dm):
    project = find_project(projects, args.project)
    if not project:
        print_error(f"Project '{args.project}' not found.")
        sys.exit(1)

    if not project.tasks:
        print_warning(f"No tasks found in project '{project.title}'.")
        return

    table = Table(title=f"Tasks in Project: {project.title}", show_header=True, header_style="bold magenta")
    table.add_column("Title", style="bold cyan")
    table.add_column("Status", justify="center")
    table.add_column("Assigned To")

    for t in project.tasks:
        status_color = "green" if t.status == "Completed" else "yellow"
        status_str = f"[{status_color}]{t.status}[/{status_color}]"
        assignee = t.assigned_to if t.assigned_to else "Unassigned"
        table.add_row(t.title, status_str, assignee)
    console.print(table)

def cmd_complete_task(args, users, projects, tasks, dm):
    project = find_project(projects, args.project)
    if not project:
        print_error(f"Project '{args.project}' not found.")
        sys.exit(1)

    task = None
    for t in project.tasks:
        if t.title.lower() == args.title.lower():
            task = t
            break

    if not task:
        print_error(f"Task '{args.title}' not found in project '{project.title}'.")
        sys.exit(1)

    try:
        task.complete()
        for gt in tasks:
            if gt.project_title.lower() == project.title.lower() and gt.title.lower() == task.title.lower():
                gt.status = "Completed"
                break

        dm.save_data(users, projects, tasks)
        print_success(f"Task '{task.title}' in project '{project.title}' is now marked as Completed!")
    except (ValueError, TypeError) as e:
        print_error(str(e))
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Multi-user Project Tracker CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to run")

    parser_add_user = subparsers.add_parser("add-user", help="Create a new user")
    parser_add_user.add_argument("--name", required=True, help="User's full name")
    parser_add_user.add_argument("--email", required=True, help="User's email address (unique)")

    subparsers.add_parser("list-users", help="List all registered users")

    parser_add_project = subparsers.add_parser("add-project", help="Create a new project")
    parser_add_project.add_argument("--title", required=True, help="Project title (unique)")
    parser_add_project.add_argument("--user", required=True, help="Owner's email or name")
    parser_add_project.add_argument("--description", help="Project description")
    parser_add_project.add_argument("--due-date", required=True, help="Due date in YYYY-MM-DD format")

    parser_list_projects = subparsers.add_parser("list-projects", help="List all projects")
    parser_list_projects.add_argument("--user", help="Filter projects by owner/contributor email or name")

    parser_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    parser_add_task.add_argument("--project", required=True, help="Project title")
    parser_add_task.add_argument("--title", required=True, help="Task title")
    parser_add_task.add_argument("--assigned-to", help="Assigned user's email or name")

    parser_list_tasks = subparsers.add_parser("list-tasks", help="List tasks in a project")
    parser_list_tasks.add_argument("--project", required=True, help="Project title")

    parser_complete_task = subparsers.add_parser("complete-task", help="Mark a task as complete")
    parser_complete_task.add_argument("--project", required=True, help="Project title")
    parser_complete_task.add_argument("--title", required=True, help="Task title")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    dm = get_data_manager()
    users, projects, tasks = dm.load_data()

    commands = {
        "add-user": cmd_add_user,
        "list-users": cmd_list_users,
        "add-project": cmd_add_project,
        "list-projects": cmd_list_projects,
        "add-task": cmd_add_task,
        "list-tasks": cmd_list_tasks,
        "complete-task": cmd_complete_task
    }

    if args.command in commands:
        commands[args.command](args, users, projects, tasks, dm)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
