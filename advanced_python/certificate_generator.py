# Yield to print certificates
def simple_certificate_generator(names):
    for n in names:
        yield f"Certificate generated for {n}"
