# Custom error classes
class InvalidEmailError(Exception): pass
class InvalidDurationError(Exception): pass

# Form validation code
def validate_intern_data(name, email, domain, duration):
    if "@" not in email:
        raise InvalidEmailError("Please enter a valid email")
        
    if int(duration) > 12:
        raise InvalidDurationError("Internship cannot be longer than 1 year")
        
    return "Data is valid"
