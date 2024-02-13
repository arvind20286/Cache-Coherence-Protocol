class DirectoryEntry:
    def __init__(self, num_cores):
        self.state = 'I'  # Initialize to 'Invalid' state
        self.owner = -1  # No owner initially
        self.sharers = [False] * num_cores  # Initialize sharers list



class DirectoryController:
    def __init__(self, num_cores, num_blocks, main_memory, list_of_cache_controller):
        self.num_cores = num_cores
        self.num_blocks = num_blocks
        self.directory = [DirectoryEntry(num_cores) for _ in range(num_blocks)]
        self.main_memory = main_memory
        self.list_of_cache_controller = list_of_cache_controller
        self.directory_updates = 0

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

    def getModified(self, address, core_id):
        print("Got GetModified transaction from core", core_id, "for address", address, "with state", self.get_state(address))
        if self.get_state(address) == "I":
            print("Block is in invalid state in directory, Sending data", self.main_memory[address], "to core", core_id, "from main memory")
            self.update_owner(address, core_id)
            self.update_state(address, "M")
            self.directory_updates += 1
            return self.main_memory[address]
    
        elif self.get_state(address) == "S":
            print("Block is in shared state in directory, Sending data ", self.main_memory[address], "to core", core_id, "from main memory")
            self.remove_sharer(address, core_id)
            self.update_owner(address, core_id)
            self.update_state(address, "M")
            list_of_sharers = self.get_sharers(address)
            for cache_controller in self.list_of_cache_controller:
                if cache_controller.core_id in list_of_sharers:
                    self.remove_sharer(address, cache_controller.core_id)
                    cache_controller.make_invalid(address)
            self.directory_updates += 1
            return self.main_memory[address]

        elif self.get_state(address) == "O":
            print("Block is in owned state in directory, Sending data ", "to core", core_id, "from cache of core", self.get_owner(address))
            if self.get_owner(address) != core_id:
                curr_owner = self.get_owner(address)
                data = 0
                for cache_controller in self.list_of_cache_controller:
                    if cache_controller.core_id == curr_owner:
                        data = cache_controller.make_invalid(address)
                        break
                list_of_sharers = self.get_sharers(address)
                for cache_controller in self.list_of_cache_controller:
                    if cache_controller.core_id in list_of_sharers:
                        self.remove_sharer(address, cache_controller.core_id)
                        cache_controller.make_invalid(address)

                self.update_owner(address, core_id)
                self.update_state(address, "M")
                self.directory_updates += 1
                return data

            elif self.get_owner(address) == core_id:
                list_of_sharers = self.get_sharers(address)
                for cache_controller in self.list_of_cache_controller:
                    if cache_controller.core_id in list_of_sharers:
                        self.remove_sharer(address, cache_controller.core_id)
                        cache_controller.make_invalid(address)
                self.update_state(address, "M")
                self.directory_updates += 1
                return self.main_memory[address]

        elif self.get_state(address) == "M":
            print("Block is in modified state in directory, Sending data ", "to core", core_id, "from cache of core", self.get_owner(address))
            if self.get_owner(address) != core_id:
                curr_owner = self.get_owner(address)
                data = 0
                for cache_controller in self.list_of_cache_controller:
                    if cache_controller.core_id == curr_owner:
                        data = cache_controller.make_invalid(address)
                        break
    
                self.update_owner(address, core_id)
                self.update_state(address, "M")
                self.directory_updates += 1
                return data
    
        else:
            return None

    def getShared(self, core_id, address):
        print("Got GetShared transaction from core", core_id, "for address", address, "with state", self.get_state(address))
        if self.get_state(address) == "I":
            print("Block is in invalid state in directory, Sending data", self.main_memory[address], "to core", core_id, "from main memory")
            self.update_state(address, "S")
            self.add_sharer(address, core_id)
            self.directory_updates += 1
            return self.main_memory[address]

        elif self.get_state(address) == "S":
            self.add_sharer(address, core_id)
            print(f"Block is in shared state in directory, Sending data {self.main_memory[address]} to core {core_id} from main memory")
            self.directory_updates += 1
            return self.main_memory[address]

        elif self.get_state(address) == "O":
            if self.get_owner(address) != core_id:
                curr_owner = self.get_owner(address)
                data = 0
                for cache_controller in self.list_of_cache_controller:
                    if cache_controller.core_id == curr_owner:
                        data = cache_controller.read(address)
                        break

                self.add_sharer(address, core_id)
                self.directory_updates += 1
                print(f"Block is in owned state in directory, Sending data {data} to core {core_id} from cache of owner core {curr_owner}")
                return data

        elif self.get_state(address) == "M":
            if self.get_owner(address) != core_id:
                curr_owner = self.get_owner(address)
                data = 0
                for cache_controller in self.list_of_cache_controller:
                    if cache_controller.core_id == curr_owner:
                        data = cache_controller.make_owner(address)
                        break

                self.add_sharer(address, core_id)
                self.update_state(address, "O")
                self.main_memory[address] = data
                self.directory_updates += 1
                print(f"Block is in modified state in directory, Sending data {data} to core {core_id} from cache of core {curr_owner}")
                return data

        else:
            return None
    def put(self,  address, data ,core_id ):
        self.update_owner(address, -1)  # No owner
        self.update_state(address, "I")
        list_of_sharers = self.get_sharers(address)
        for cache_controller in self.list_of_cache_controller:
            if cache_controller.core_id in list_of_sharers:
                self.remove_sharer(address, cache_controller.core_id)
                cache_controller.make_invalid(address)

        if data is not None:
            self.main_memory[address] = data
            print(f"Put transaction from core {core_id} for address {address} with data {data}, updated main memory")

        else:
            print(f"Put transaction from core {core_id} for address {address}")
        self.directory_updates += 1

        return None