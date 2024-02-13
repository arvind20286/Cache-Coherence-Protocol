import random
import CacheMemory

class CacheController:
    def __init__(self, cache_memory, core_id, directory_controller):
        self.cache_memory = cache_memory
        self.core_id = core_id
        self.directory_controller = directory_controller
    def find_block(self, address, update_time = True):
        line_size = self.cache_memory.line_size
        num_sets = self.cache_memory.num_sets

        index = (address // line_size) % num_sets
        set_to_access = self.cache_memory.sets[index]

        # Placeholder for the tag calculation
        tag = address // (line_size * num_sets)

        # Check if the block is in the set
        for line in set_to_access.lines:
            if line.valid and line.tag == tag:
                # Cache hit: update the last used time and return the data
                if update_time:
                    line.last_used = self.cache_memory.time
                    self.cache_memory.time += 1
                return line
        return None

    def load_shared(self, address):
        print(f"---- Core {self.core_id} is requesting to load shared address {address} ----")
        block = self.find_block(address)
        if block is not None and block.state == "S":
            print("Cache hit and Data is not in invalid state")
            # return block.data
            #return block
        elif block is not None and (block.state == "M" or block.state == "O"):
            print("Cache hit and Data is in modified state")
            # need to request to directory controller to invalidate other sharers
            # ,but they should already be invalidated if the block is in modified state
            # return block.data
            #return block

        else:
            print("Cache miss")
            # need to request to directory controller
            data = self.directory_controller.getShared(self.core_id, address)
            block = self.write(address, data)
            block.state = "S"
            return 0

        return 1

    def load_modified(self, address):
        print(f"---- Core {self.core_id} is requesting to load modified address {address} ----")
        block = self.find_block(address)
        if block is not None and block.state == "M":
            print("Cache hit and Data is in modified state")
            # need to request to directory controller to invalidate other sharers
            # ,but they should already be invalidated if the block is in modified state
            # return block.data
        

        elif block is not None and (block.state == "S" or block.state == "O"):
            print("Cache hit and Data is in shared state")
            # need to request to directory controller to invalidate other sharers
#           block.data = self.directory_controller.getModified(address, self.core_id).data
            data = self.directory_controller.getModified(address, self.core_id)
            block = self.write(address, data, False)
            block.state = "M"

        else:
            print("Cache miss")
            # need to request to directory controller
            #req_block = self.directory_controller.getModified(address, self.core_id).data
            print("GetModified transaction is sent to directory controller")
            data = self.directory_controller.getModified(address, self.core_id)
            # if cache is full, need to evict a block
            block = self.write(address, data)
            block.state = "M"
            return 0

        return 1

    def invalidate(self, address):
        print(f"---- Core {self.core_id} is requesting to invalidate address {address} ----")
        block = self.find_block(address)
        if block is not None and block.state == "M":
            print("Cache hit and Data is in modified state")
            # make a put request to directory controller and sending the data and the directory controller
            self.directory_controller.put(address, block.data, self.core_id)
            # will update the memory and then
            self.make_invalid(address)

        elif block is not None and block.state == "S":
            print("Cache hit and Data is in shared state")
            # make a put request to directory controller and not sending the data and the directory controller
            # the directory controller will delete the sharer from the list
            self.directory_controller.put(address, None, self.core_id)
            self.make_invalid(address)

        elif block is not None and block.state == "O":
            print("Cache hit and Data is in owned state")
            # make a put request to directory controller and not sending the data and the directory controller
            # the directory controller will delete the sharer from the list
            self.directory_controller.put(address, block.data, self.core_id)
            self.make_invalid(address)

        else:
            print("Cache miss")
            # do nothing
            return 0

        return 1

    def add(self, address, immediate):
        print(f"---- Core {self.core_id} is requesting to add immediate {immediate} to address {address} ----")
        block = self.find_block(address)
        if block is not None and block.state == "M":
            print("Cache hit and Data is in modified state")
            block.data += immediate
            # make a put request to directory controller and sending the data and the directory controller
            self.directory_controller.main_memory[address] = block.data

        elif block is not None and (block.state == "S" or block.state == "O"):
            print("Cache hit and Data is in shared state")
            block.state = "M"
            # make a get modified transaction to directory controller
            data = self.directory_controller.getModified(address, self.core_id)
            data += immediate
            block = self.write(address, data)
            # make a put request to directory controller and sending the data and the directory controller
            self.directory_controller.main_memory[address] = block.data
            # need to request to directory controller to invalidate other sharers

        else:
            print("Cache miss")
            # need to request to directory controller
            # if cache is full, need to evict a block
            block = self.write(address, self.directory_controller.getModified(address, self.core_id))
            block.state = "M"
            block.data += immediate
            # make a put request to directory controller and sending the data and the directory controller
            self.directory_controller.main_memory[address] = block.data
            return 0

        return 1

    def make_invalid(self, address):
        block = self.find_block(address, False)
        data = None
        if block is not None and block.state == "M":
            data = block.data
        if block is not None:
            block.state = "I"
            block.valid = False
            block.tag = None
        return data

    def make_shared(self, address):
        block = self.find_block(address, False)
        data = None
        if block is not None and block.state == "M":
            data = block.data
        if block is not None:
            block.state = "S"
        return data

    def make_owner(self, address):
        block = self.find_block(address, False)
        data = None
        if block is not None and block.state == "M":
            data = block.data
        if block is not None:
            block.state = "O"
        return data

    def read(self, address):
        if self.find_block(address, False) is not None:
            return self.find_block(address, False).data

        return None  # Cache miss

    def write(self, address, data, update_time = True):
        line_size = self.cache_memory.line_size
        num_sets = self.cache_memory.num_sets

        index = (address // line_size) % num_sets
        set_to_access = self.cache_memory.sets[index]

        # Placeholder for the tag calculation
        tag = address // (line_size * num_sets)

        # Check if the block is in the set
        for line in set_to_access.lines:
            if line.valid and line.tag == tag:
                # Cache hit: update the last used time and return the data
                if update_time:
                    line.last_used = self.cache_memory.time
                    self.cache_memory.time += 1
                line.data = data
                return line

        # Cache miss: choose a line to replace using LRU policy
        line_to_replace = set_to_access.get_lru_line()
        if line_to_replace.valid :
            self.invalidate(line_to_replace.tag * line_size * num_sets + index * line_size)
        line_to_replace.data = data
        line_to_replace.tag = tag
        line_to_replace.valid = True
        line_to_replace.last_used = self.cache_memory.time
        self.cache_memory.time += 1

        return line_to_replace
