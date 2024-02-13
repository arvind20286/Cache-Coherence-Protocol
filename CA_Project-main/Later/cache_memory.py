#Invalid













class CacheLine:
    def __init__(self, line_size):
        self.valid = False
        self.tag = None
        self.data = [0] * line_size

class CacheSet:
    def __init__(self, associativity, line_size):
        self.lines = [CacheLine(line_size) for _ in range(associativity)]

class CacheMemory:
    def __init__(self, size, line_size, associativity):
        self.size = size  # Total size of the cache in bytes
        self.line_size = line_size  # Size of each cache line in bytes
        self.associativity = associativity  # Number of lines in each set
        self.num_sets = size // (line_size * associativity)
        self.cache = [CacheSet(associativity, line_size) for _ in range(self.num_sets)]

    def read(self, address):
        # Calculate the cache set index, line index, and offset from the address
        set_index, offset = divmod(address, self.line_size * self.associativity)
        line_index, offset = divmod(offset, self.line_size)

        # Check if the cache line is valid and the tags match
        for line in self.cache[set_index].lines:
            if line.valid and line.tag == line_index:
                # Implement LRU policy (move the accessed line to the most recently used position)
                self.cache[set_index].lines.remove(line)
                self.cache[set_index].lines.insert(0, line)
                return line.data[offset]

        return None  # Cache miss

    def write(self, address, data):
        # Calculate the cache set index, line index, and offset from the address
        set_index, offset = divmod(address, self.line_size * self.associativity)
        line_index, offset = divmod(offset, self.line_size)

        # Write data to the cache line
        line = self.cache[set_index].lines[0]  # Use the least recently used line
        line.data[offset] = data
        line.valid = True
        line.tag = line_index

    def dump_cache(self):
        for i, cache_set in enumerate(self.cache):
            for j, line in enumerate(cache_set.lines):
                if line.valid:
                    print(f"Cache Set {i}, Line {j}: Tag {line.tag}, Data {line.data}")
