import re


class InvalidEmailError(Exception):
    """Raised when an intern email address is invalid."""


class InvalidDurationError(Exception):
    """Raised when internship duration is invalid."""


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_email(email):
    if not email or not EMAIL_PATTERN.match(email):
        raise InvalidEmailError("Invalid email address.")
    return True


def validate_duration(duration):
    if not isinstance(duration, int) or duration <= 0:
        raise InvalidDurationError("Duration must be a positive integer.")
    return True


def validate_intern_data(name, email, domain, duration):
    if not name or not domain:
        raise ValueError("Name and domain are required.")
    validate_email(email)
    validate_duration(duration)
    return True
