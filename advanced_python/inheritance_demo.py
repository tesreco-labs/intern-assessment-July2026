class Person:
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def display(self):
        return f"Person Name: {self.name}"


class Employee(Person):
    def __init__(self, employee_id, **kwargs):
        super().__init__(**kwargs)
        self.employee_id = employee_id


class Mentor(Person):
    def __init__(self, specialization, **kwargs):
        super().__init__(**kwargs)
        self.specialization = specialization


class TESRECOMentor(Employee, Mentor):
    def __init__(self, name, employee_id, specialization):
        super().__init__(
            name=name,
            employee_id=employee_id,
            specialization=specialization,
        )

    def display(self):
        return (
            f"TESRECO Mentor: {self.name}, "
            f"Employee ID: {self.employee_id}, "
            f"Specialization: {self.specialization}"
        )


def get_mro():
    return [cls.__name__ for cls in TESRECOMentor.__mro__]
