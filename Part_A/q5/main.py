class InvalidEmailError(Exception):
    """Raised when the email address is invalid."""
    pass

class InvalidDurationError(Exception):
    """Raised when the internship duration is invalid."""
    pass

def intern_info(email, duration):
    """Validates intern email and internship duration."""

    if(duration < 0):
        raise InvalidDurationError("Internship duration can't be negative")
    if "@" not in email:
        raise InvalidEmailError("Email is invalid")
    print("email:",email,"duration:",duration)
    
# intern_info("abcgmail.com", 5)
# intern_info("abc@gmail.com", -1)
# intern_info("abcgmail.com", -1)
intern_info("abc@gmail.com", 5)