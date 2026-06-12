import re

class Person:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Name cannot be empty")
        # Ensure it contains letters/spaces/punctuation, not just numbers or symbols
        if not re.search(r"[a-zA-Z]", stripped):
            raise ValueError("Name must contain at least one letter")
        self._name = stripped

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        stripped = value.strip()
        # Simple regex validation for email
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, stripped):
            raise ValueError(f"Invalid email format: '{value}'")
        self._email = stripped

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, email={self.email!r})"
