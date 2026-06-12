class Task:
    VALID_STATUSES = {"Pending", "Completed"}

    def __init__(self, title: str, project_title: str, status: str = "Pending", assigned_to: str = None):
        self.title = title
        self.project_title = project_title
        self.status = status
        self.assigned_to = assigned_to

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Task title must be a string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Task title cannot be empty")
        self._title = stripped

    @property
    def project_title(self) -> str:
        return self._project_title

    @project_title.setter
    def project_title(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Project title must be a string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Project title cannot be empty")
        self._project_title = stripped

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Status must be a string")
        capitalized = value.strip().capitalize()
        if capitalized not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self._status = capitalized

    @property
    def assigned_to(self) -> str:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: str):
        if value is None:
            self._assigned_to = None
            return
        if not isinstance(value, str):
            raise TypeError("Assigned user email must be a string or None")
        stripped = value.strip()
        if not stripped:
            self._assigned_to = None
            return
        if "@" not in stripped or "." not in stripped:
            raise ValueError("Invalid assigned user email format")
        self._assigned_to = stripped

    def complete(self):
        self.status = "Completed"

    def __str__(self) -> str:
        assignee = self.assigned_to if self.assigned_to else "Unassigned"
        return f"Task '{self.title}' [{self.status}] (Assigned to: {assignee})"

    def __repr__(self) -> str:
        return f"Task(title={self.title!r}, status={self.status!r}, assigned_to={self.assigned_to!r})"
