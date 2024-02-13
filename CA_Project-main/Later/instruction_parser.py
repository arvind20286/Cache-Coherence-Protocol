#Invalid













class InstructionParser:
    def __init__(self, num_cores, directory_controller, cache_memory):
        self.num_cores = num_cores
        self.directory_controller = directory_controller
        self.cache_memory = cache_memory

    def parse_instruction(self, instruction):
        parts = instruction.split()
        core_id = int(parts[0])
        opcode = parts[1]

        if opcode == 'LS':
            address = int(parts[2])
            # Handle Load Shared (LS) instruction
            self.handle_load_shared(core_id, address)
        elif opcode == 'LM':
            address = int(parts[2])
            # Handle Load Modified (LM) instruction
            self.handle_load_modified(core_id, address)
        elif opcode == 'IN':
            address = int(parts[2])
            # Handle Invalidate (IN) instruction
            self.handle_invalidate(core_id, address)
        elif opcode == 'ADD':
            address = int(parts[2])
            immediate = int(parts[3])
            # Handle Add (ADD) instruction
            self.handle_add(core_id, address, immediate)
        else:
            print(f"Unknown opcode: {opcode}")

    def handle_load_shared(self, core_id, address):
        block_index = address  # For simplicity, we assume a direct-mapped cache
        state = self.directory_controller.get_state(block_index)
        if state == 'M':
            # If the block is in 'Modified' state, we need to write it back to memory
            owner = self.directory_controller.get_owner(block_index)
            if owner != core_id:
                # The current core doesn't own the block, so we need to invalidate it in the owner's cache
                self.directory_controller.update_state(block_index, 'I')
                self.directory_controller.remove_sharer(block_index, owner)
                print(f"Core {core_id} invalidated block {block_index} in Core {owner}'s cache")
        # Load data from memory or cache and update the cache state
        self.cache_memory.read(address)
        print(f"Core {core_id} loaded shared data from block {block_index}")

    def handle_load_modified(self, core_id, address):
        block_index = address  # For simplicity, we assume a direct-mapped cache
        state = self.directory_controller.get_state(block_index)
        if state == 'M':
            # If the block is in 'Modified' state, it means the current core already has a copy
            # No need to read from memory or update directory, just load from cache
            self.cache_memory.read(address)
            print(f"Core {core_id} loaded modified data from its own cache")
        elif state == 'S':
            # If the block is in 'Shared' state, we need to invalidate it in other cores' caches
            self.invalidate_other_caches(core_id, block_index)
            # Load data from memory or cache and update the cache state
            self.cache_memory.read(address)
            self.directory_controller.update_state(block_index, 'M')
            self.directory_controller.update_owner(block_index, core_id)
            print(f"Core {core_id} loaded modified data from block {block_index}")
        else:
            # The block is in 'Invalid' state, so we can directly load from memory
            self.cache_memory.read(address)
            self.directory_controller.update_state(block_index, 'M')
            self.directory_controller.update_owner(block_index, core_id)
            print(f"Core {core_id} loaded modified data from memory and became the owner")

    def handle_invalidate(self, core_id, address):
        block_index = address  # For simplicity, we assume a direct-mapped cache
        state = self.directory_controller.get_state(block_index)
        if state == 'M':
            owner = self.directory_controller.get_owner(block_index)
            if owner != core_id:
                # If the block is in 'Modified' state and the current core doesn't own it, invalidate the owner's cache
                self.directory_controller.update_state(block_index, 'I')
                self.directory_controller.remove_sharer(block_index, owner)
                print(f"Core {core_id} invalidated block {block_index} in Core {owner}'s cache")
        elif state == 'S':
            # If the block is in 'Shared' state, remove the current core from the sharers list
            self.directory_controller.remove_sharer(block_index, core_id)
            print(f"Core {core_id} invalidated block {block_index} from its sharers")
        # In the 'Invalid' state, there's nothing to do

    def handle_add(self, core_id, address, immediate):
        block_index = address  # For simplicity, we assume a direct-mapped cache
        # Load data from cache and update the cache state
        data = self.cache_memory.read(address)
        data += immediate
        self.cache_memory.write(address, data)
        print(f"Core {core_id} added {immediate} to data in block {block_index}")

    def invalidate_other_caches(self, core_id, block_index):
        for i in range(self.num_cores):
            if i != core_id:
                self.handle_invalidate(i, block_index)

