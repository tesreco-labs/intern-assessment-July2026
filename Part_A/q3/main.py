class InternIdGenarator:
    """Iterator class to generate unique intern IDs."""
    
    def __init__(self):
        self.id = 1

    def __iter__(self):
        return self
    
    def __next__(self):
        id = f"TES{self.id}"
        self.id += 1
        return id
    
ids = InternIdGenarator()

print(next(ids))
print(next(ids))
print(next(ids))