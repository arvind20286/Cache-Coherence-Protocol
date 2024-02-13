#Invalid













class Logger:
    def __init__(self, cache_memory, directory_controller, memory):
        self.cache_memory = cache_memory
        self.directory_controller = directory_controller
        self.memory = memory

    def log_cache_state(self):
        # Log the state of the cache memory after executing each instruction
        for i in range(len(self.cache_memory.cache)):
            for j in range(len(self.cache_memory.cache[i].lines)):
                line = self.cache_memory.cache[i].lines[j]
                if line.valid:
                    print(f"Cache Set {i}, Line {j}: Valid, Tag {line.tag}, Data {line.data}")
                else:
                    print(f"Cache Set {i}, Line {j}: Invalid")

    def log_directory_state(self):
        # Log the state of directory entries after executing each instruction
        for i in range(len(self.directory_controller.directory)):
            entry = self.directory_controller.directory[i]
            print(f"Block {i}: State {entry.state}, Owner {entry.owner}, Sharers {entry.sharers}")

    def log_memory_content(self):
        # Log the content of the main memory after executing each instruction
        for i in range(len(self.memory)):
            print(f"Memory Location {i}: {self.memory[i]}")

        # Add a separator for clarity
        print('-' * 40)