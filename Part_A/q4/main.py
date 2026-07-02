def certificate_generator(names):
    """Generates internship certificates one by one."""
    
    for name in names:
        yield f"Certificate Generated for {name}"
    yield "no more interns left"

interns = ["Khushi", "Raushan"]

certificate = certificate_generator(interns)

print(next(certificate))
print(next(certificate))
print(next(certificate))