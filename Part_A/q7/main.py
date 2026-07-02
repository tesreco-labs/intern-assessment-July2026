class Person:
    """Represents a person with a name."""

    def __init__(self, name):
        self.name = name
    
    def about(self):
        """Displays person details."""
        print("name is:",self.name)

class Employee(Person):
    """Represents an employee with an employee ID."""

    def __init__(self, name, empId):
        Person.__init__(self, name)
        self.empId = empId
    
    def about(self):
        """Displays employee details."""
        print(f"name is:{self.name} and employee id is:{self.empId}")

class Mentor(Person):
    """Represents a mentor with a mentor ID."""

    def __init__(self, name, mntId):
        Person.__init__(self, name)
        self.mntId = mntId

    def about(self):
        """Displays mentor details."""
        print(f"name is:{self.name} and mentor id is:{self.mntId}")

class TESRECOMentor(Employee, Mentor):
    """Represents a TESRECO mentor with employee and mentor roles."""

    def __init__(self, name, empId, mntId, domain):
        Employee.__init__(self, name, empId)
        Mentor.__init__(self, name, mntId)
        self.domain = domain

    def about(self):
        """Displays complete TESRECO mentor details."""
        print(f"name is:{self.name} and employee id is:{self.empId} and mentor id is:{self.mntId} and domain is:{self.domain}")


TESMentor1 = TESRECOMentor("XYZ", "789", "123", "AI/ML")
TESMentor1.about()

mentor1 = Mentor("PQR", "123")
mentor1.about()

p1 = Person("ABC")
p1.about()

