# Basic intern class
class Intern:
    def __init__(self, intern_id, name, email, domain, duration):
        self.intern_id = intern_id
        self.name = name
        self.email = email
        self.domain = domain
        self.duration = duration

    def __str__(self):
        # Print string format
        return f"{self.name} from {self.domain} domain"
