from datetime import datetime

class Project:
    def __init__(self, title: str, description: str, due_date: str, owner_email: str, tasks=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_email = owner_email
        self.tasks = tasks if tasks is not None else []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        self._title = stripped

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        self._description = value.strip()

    @property
    def due_date(self) -> str:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Due date must be a string")
        stripped = value.strip()
        try:
            datetime.strptime(stripped, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Due date '{value}' must be in YYYY-MM-DD format")
        self._due_date = stripped

    @property
    def owner_email(self) -> str:
        return self._owner_email

    @owner_email.setter
    def owner_email(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Owner email must be a string")
        stripped = value.strip()
        if "@" not in stripped or "." not in stripped:
            raise ValueError("Invalid owner email format")
        self._owner_email = stripped

    @property
    def contributors(self) -> list:
        contribs = set()
        for task in self.tasks:
            if task.assigned_to:
                contribs.add(task.assigned_to)
        return sorted(list(contribs))

    def add_task(self, task):
        self.tasks.append(task)

    def __str__(self) -> str:
        return f"Project '{self.title}' (Due: {self.due_date}, Tasks: {len(self.tasks)}, Owner: {self.owner_email})"

    def __repr__(self) -> str:
        return f"Project(title={self.title!r}, owner={self.owner_email!r}, tasks_count={len(self.tasks)})"
