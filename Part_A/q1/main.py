class Intern:
    """
    Represents an intern in the TESRECO Internship Management System.

    Attributes:
        intern_id (str): Unique ID assigned to the intern.
        name (str): Full name of the intern.
        email (str): Email address of the intern.
        domain (str): Internship domain (e.g., Data Science, Python).
        duration (int): Internship duration (e.g., 3 weeks).
    """
    
    def __init__(self, intern_id, name, email, domain, duration):
        """
        Initialize an Intern object.

        Args:
            intern_id (str): Unique intern ID.
            name (str): Name of the intern.
            email (str): Email address.
            domain (str): Internship domain.
            duration (int): Internship duration.
        """
        self.intern_id = intern_id
        self.name = name
        self.email = email
        self.domain = domain
        self.duration = duration

    def set_intern_id(self, intern_id):
        """
        Set the intern ID.

        Args:
            intern_id (str): New intern ID.
        """
        self.intern_id = intern_id

    def set_name(self, name):
        """
        Set the intern's name.

        Args:
            name (str): New name.
        """
        self.name = name

    def set_email(self, email):
        """
        Set the intern's email address.

        Args:
            email (str): New email address.
        """
        self.email = email

    def set_domain(self, domain):
        """
        Set the internship domain.

        Args:
            domain (str): Internship domain.
        """
        self.domain = domain

    def set_duration(self, duration):
        """
        Set the internship duration.

        Args:
            duration (int): Internship duration.
        """
        self.duration = duration

    def get_intern_id(self):
        """
        Get the intern ID.

        Returns:
            str: Intern ID.
        """
        return self.intern_id

    def get_name(self):
        """
        Get the intern's name.

        Returns:
            str: Intern name.
        """
        return self.name

    def get_email(self):
        """
        Get the intern's email address.

        Returns:
            str: Email address.
        """
        return self.email

    def get_domain(self):
        """
        Get the internship domain.

        Returns:
            str: Internship domain.
        """
        return self.domain

    def get_duration(self):
        """
        Get the internship duration.

        Returns:
            int: Internship duration.
        """
        return self.duration

    def __str__ (self):
        """
        Return a human-readable string representation of the Intern object.

        Returns:
            str: Formatted intern details.
        """
        return f"intern_id: {self.intern_id}, name:{self.name}, email:{self.email}, domain:{self.domain}, duration:{self.duration}"
    

intern1 = Intern("TES101", "David", "david@gmail.com", "AI/ML", 4)
print(intern1)

print("----- Getter Methods -----")
print("Intern ID:", intern1.get_intern_id())
print("Name:", intern1.get_name())
print("Email:", intern1.get_email())
print("Domain:", intern1.get_domain())
print("Duration:", intern1.get_duration(), "weeks")

print("----- Updating Intern Details Using Setters -----")
intern1.set_name("David Walker")
intern1.set_email("david.walker@gmail.com")
intern1.set_domain("Python")
intern1.set_duration(6)

print("Updated Details:")
print(intern1)