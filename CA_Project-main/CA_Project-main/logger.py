class Logger:
    def __init__(self, list_of_cache_memory, directory_controller, memory):
        self.list_of_cache_memory = list_of_cache_memory
        self.directory_controller = directory_controller
        self.memory = memory

    def log_cache_state(self, core_id, dump_file):
        for core_id in range(len(self.list_of_cache_memory)):
            dump_file.write(f"***Core {core_id} Cache:\n")
            for set_num in range(self.list_of_cache_memory[core_id].num_sets):
                dump_file.write(f"\tSet {set_num}:\n")
                for line_num in range(len(self.list_of_cache_memory[core_id].sets[set_num].lines)):
                    line = self.list_of_cache_memory[core_id].sets[set_num].lines[line_num]
                    if line.valid:
                        dump_file.write(f"\tLine {line_num}: Valid, State {line.state},  Tag {line.tag}, Data {line.data}\n")
                    else:
                        dump_file.write(f"\tLine {line_num}: Invalid\n")

    def log_directory_state(self, dump_file):
        # Log the state of directory entries after executing each instruction
        dump_file.write("*** Directory:\n")
        for i in range(len(self.directory_controller.directory)):
            entry = self.directory_controller.directory[i]
            # print(f"Block {i}: State {entry.state}, Owner {entry.owner}, Sharers {entry.sharers}")
            dump_file.write(f"Block {i}: State {entry.state}, Owner {entry.owner}, Sharers {entry.sharers}\n")
        dump_file.write('\n\n')

    def log_memory_content(self, dump_file):
        # Log the content of the main memory after executing each instruction
        dump_file.write("*** Main Memory:\n")
        for i in range(len(self.memory)):
            # print(f"Memory Location {i}: {self.memory[i]}")
            dump_file.write(f"Memory Location {i}: {self.memory[i]}\n")

        # Add a separator for clarity
        # print('-' * 40)
        dump_file.write('-' * 40 + '\n')