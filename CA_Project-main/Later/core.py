#Invalid













class Core:
    def __init__(self, core_id, cache_memory, directory_controller, instruction_parser):
        self.core_id = core_id
        self.cache_memory = cache_memory
        self.directory_controller = directory_controller
        self.instruction_parser = instruction_parser

    def issue_load_shared(self, address):
        # Construct and execute a Load Shared (LS) instruction
        instruction = f"{self.core_id} LS {address}"
        self.instruction_parser.parse_instruction(instruction)

    def issue_load_modified(self, address):
        # Construct and execute a Load Modified (LM) instruction
        instruction = f"{self.core_id} LM {address}"
        self.instruction_parser.parse_instruction(instruction)

    def issue_invalidate(self, address):
        # Construct and execute an Invalidate (IN) instruction
        instruction = f"{self.core_id} IN {address}"
        self.instruction_parser.parse_instruction(instruction)

    def issue_add(self, address, immediate):
        # Construct and execute an Add (ADD) instruction
        instruction = f"{self.core_id} ADD {address} {immediate}"
        self.instruction_parser.parse_instruction(instruction)
