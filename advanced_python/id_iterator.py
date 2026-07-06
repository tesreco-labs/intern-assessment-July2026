class InternIDIterator:
    def __init__(self, start=1, limit=None):
        self.current = start
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None and self.current > self.limit:
            raise StopIteration

        intern_id = f"TES{self.current:03d}"
        self.current += 1
        return intern_id
