from models.person import Person

class User(Person):
    _id_counter = 0

    def __init__(self, name, email, user_id=None):
        super().__init__(name, email)
        if user_id is None:
            User._id_counter += 1
            self._user_id = User._id_counter
        else:
            if not isinstance(user_id, int) or user_id <= 0:
                raise ValueError("User ID must be a positive integer")
            self._user_id = user_id
            if user_id > User._id_counter:
                User._id_counter = user_id

    @property
    def id(self):
        return self._user_id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("User ID must be a positive integer")
        self._user_id = value
        if value > User._id_counter:
            User._id_counter = value

    def __str__(self):
        return f"User #{self.id}: {self.name} ({self.email})"

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"
