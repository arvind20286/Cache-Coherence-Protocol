class CacheLine:
    def __init__(self, line_size):
        self.state = "I"  # Initial state is Invalid
        self.valid = False
        self.tag = None
        self.data = [0] * line_size
        self.last_used = -1  # To keep track of usage for LRU

class CacheSet:
    def __init__(self, associativity, line_size):
        self.lines = [CacheLine(line_size) for _ in range(associativity)]

    def get_lru_line(self):
        # Get the line that was least recently used (has the smallest last_used value)
        return min(self.lines, key=lambda line: line.last_used)

class CacheMemory:
    def __init__(self, size, line_size, associativity, core_id):
        self.size = size
        self.line_size = line_size
        self.associativity = associativity
        self.num_sets = size // (line_size * associativity)
        self.sets = [CacheSet(associativity, line_size) for _ in range(self.num_sets)]
        self.core_id = core_id
        self.time = 0  # Global time for LRU policy
