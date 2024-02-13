#Invalid













from cache_memory import CacheMemory
from directory import DirectoryController
from instruction_parser import InstructionParser
from core import Core
from logger import Logger
from testcases import TestCases


def main():
    # Define the system parameters
    num_cores = 2
    num_blocks = 64

    # Initialize components
    cache_memory = CacheMemory(size=num_blocks, line_size=1, associativity=1)
    directory_controller = DirectoryController(num_cores, num_blocks)
    memory = [0] * num_blocks
    logger = Logger(cache_memory, directory_controller, memory)
    instruction_parser = InstructionParser(num_cores, directory_controller, cache_memory)

    # Initialize cores
    cores = [Core(core_id=i, cache_memory=cache_memory, directory_controller=directory_controller, instruction_parser=instruction_parser) for i in range(num_cores)]

    # Run test cases to simulate cache coherence behavior
    test_cases = TestCases(num_cores, num_blocks, cache_memory, directory_controller, logger)
    test_cases.run_test_cases()

    # Log the final state after test cases
    print("\nFinal State:")
    logger.log_cache_state()
    logger.log_directory_state()
    logger.log_memory_content()

if __name__ == "__main__":
    main()