class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Name cannot be empty")
        has_letter = False
        for char in stripped:
            if char.isalpha():
                has_letter = True
                break
        if not has_letter:
            raise ValueError("Name must contain at least one letter")
        self._name = stripped

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        stripped = value.strip()
        if "@" not in stripped or "." not in stripped:
            raise ValueError(f"Invalid email format: '{value}'")
        parts = stripped.split("@")
        if len(parts) != 2 or not parts[0] or not parts[1] or "." not in parts[1]:
            raise ValueError(f"Invalid email format: '{value}'")
        self._email = stripped

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, email={self.email!r})"
