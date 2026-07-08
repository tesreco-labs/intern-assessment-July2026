# Inheriting from two classes
class Employee:
    def work(self): 
        return "I am working"

class Mentor:
    def greet(self): 
        return "Hello students"
        
    def mentor_intern(self, name): 
        return f"Teaching {name}"

class TESRECOMentor(Employee, Mentor):
    def __init__(self, name, age, emp_id, dept, spec, exp):
        self.name = name
        self.dept = dept
        self.spec = spec
        
    def display_info(self):
        return f"Mentor {self.name} teaches {self.spec}"
