# Simple loop to generate IDs
class InternIDIterator:
    def __init__(self, start=101, stop=105):
        self.start = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.start > self.stop:
            raise StopIteration
        
        # Creates TES101, TES102 etc.
        new_id = f"TES{self.start}"
        self.start += 1
        return new_id
