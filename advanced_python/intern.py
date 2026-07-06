from .exceptions import validate_duration, validate_email


class Intern:
    def __init__(self, intern_id, name, email, domain, duration):
        self._intern_id = intern_id
        self._name = name
        self._email = None
        self._domain = domain
        self._duration = None
        self.set_email(email)
        self.set_duration(duration)

    def get_intern_id(self):
        return self._intern_id

    def set_intern_id(self, intern_id):
        self._intern_id = intern_id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_email(self):
        return self._email

    def set_email(self, email):
        validate_email(email)
        self._email = email

    def get_domain(self):
        return self._domain

    def set_domain(self, domain):
        self._domain = domain

    def get_duration(self):
        return self._duration

    def set_duration(self, duration):
        validate_duration(duration)
        self._duration = duration

    def __str__(self):
        return (
            f"Intern({self._intern_id}, {self._name}, {self._email}, "
            f"{self._domain}, {self._duration} months)"
        )
