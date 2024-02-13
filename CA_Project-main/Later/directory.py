#Invalid













class DirectoryEntry:
    def __init__(self, num_cores):
        self.state = 'I'  # Initialize to 'Invalid' state
        self.owner = -1  # No owner initially
        self.sharers = [False] * num_cores  # Initialize sharers list

class DirectoryController:
    def __init__(self, num_cores, num_blocks):
        self.num_cores = num_cores
        self.num_blocks = num_blocks
        self.directory = [DirectoryEntry(num_cores) for _ in range(num_blocks)]

    def get_state(self, block_index):
        # Get the state of a directory entry for a specific block
        return self.directory[block_index].state

    def get_owner(self, block_index):
        # Get the owner of a directory entry for a specific block
        return self.directory[block_index].owner

    def get_sharers(self, block_index):
        # Get the list of sharers of a directory entry for a specific block
        sharers = []
        for core_id, sharer in enumerate(self.directory[block_index].sharers):
            if sharer:
                sharers.append(core_id)
        return sharers

    def update_state(self, block_index, new_state):
        # Update the state of a directory entry for a specific block
        self.directory[block_index].state = new_state

    def update_owner(self, block_index, new_owner):
        # Update the owner of a directory entry for a specific block
        self.directory[block_index].owner = new_owner

    def add_sharer(self, block_index, core_id):
        # Add a core as a sharer for a specific block
        self.directory[block_index].sharers[core_id] = True

    def remove_sharer(self, block_index, core_id):
        # Remove a core from the list of sharers for a specific block
        self.directory[block_index].sharers[core_id] = False
