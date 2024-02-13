class TestCases:
    def __init__(self, num_cores, num_blocks, cache_memory, directory_controller, logger):
        self.num_cores = num_cores
        self.num_blocks = num_blocks
        self.cache_memory = cache_memory
        self.directory_controller = directory_controller
        self.logger = logger

    def run_test_cases(self):
        # Test case 1: Load Shared (LS) instruction with shared data
        print("Test Case 1: Load Shared (LS) with shared data")
        self.cache_memory.write(0, 42)  # Write data to a memory location
        self.directory_controller.update_state(0, 'S')  # Set the directory entry state to 'Shared'
        self.logger.log_cache_state()
        self.logger.log_directory_state()

        # Test case 2: Load Modified (LM) instruction with owned data
        print("\nTest Case 2: Load Modified (LM) with owned data")
        self.cache_memory.write(1, 55)  # Write data to a memory location
        self.directory_controller.update_state(1, 'M')  # Set the directory entry state to 'Modified'
        self.directory_controller.update_owner(1, 0)  # Set the owner to core 0
        self.logger.log_cache_state()
        self.logger.log_directory_state()

        # Test case 3: Add (ADD) instruction
        print("\nTest Case 3: Add (ADD) instruction")
        self.cache_memory.write(2, 10)  # Write data to a memory location
        self.directory_controller.update_state(2, 'I')  # Set the directory entry state to 'Invalid'
        self.logger.log_cache_state()
        self.logger.log_directory_state()

        # Test case 4: Invalid state transition
        print("\nTest Case 4: Invalid state transition")
        self.directory_controller.update_state(3, 'S')  # Set the directory entry state to 'Shared'
        self.directory_controller.update_owner(3, 1)  # Set the owner to core 1
        self.directory_controller.add_sharer(3, 0)  # Add core 0 as a sharer
        self.cache_memory.write(3, 30)  # Write data to a memory location
        self.directory_controller.update_state(3, 'M')  # Attempt an invalid state transition
        self.logger.log_cache_state()
        self.logger.log_directory_state()

