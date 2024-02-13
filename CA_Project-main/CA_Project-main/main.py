from CacheMemory import CacheMemory
from directory import DirectoryController
from instruction_parser import InstructionParser
#from core import Core
from logger import Logger
#from testcases import TestCases
from CacheController import CacheController
import sys
import matplotlib.pyplot as plt
import plot
def main():
    # Define the system parameters
    num_cores = 4
    num_blocks = 64
    cycle = 0
    hit_time = 1
    memory = [0] * num_blocks
    cache_controller_list = []
    cache_memory_list = []
    core_access_logs = [[], [], [], []]

    for i in range(num_cores):
        core_id = i
        cache_memory = CacheMemory(size= 4, line_size=1, associativity=2, core_id= core_id)
        cache_controller = CacheController(cache_memory ,core_id,None)
        cache_controller_list.append(cache_controller)
        cache_memory_list.append(cache_memory)

    directory_controller = DirectoryController(num_cores, num_blocks, memory, cache_controller_list)

    for cache_controller in cache_controller_list:
        cache_controller.directory_controller = directory_controller

    file_path = 'input6.txt'
    input_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            input_lines.append(line)

    dump_file = open("dump.txt", "w")
    logger = Logger(cache_memory_list, directory_controller, memory)
    # input_lines = ['0	LM	34', '0	ADD	62	2']
    directory_updates_points = []
    for instruction in input_lines:
        if instruction == '0	LM	5':
            pass
        parts = instruction.split()
        for i in range(len(parts)):
            parts[i] = parts[i].strip()

        access_type = None
        core_id = int(parts[0])
        opcode = parts[1]
        if 0<= int(parts[0])< num_cores and 0<=int(parts[2])< 64:
            if opcode == 'LS':
                address = int(parts[2])
                access_type = cache_controller_list[core_id].load_shared(address)

            elif opcode == 'LM':
                address = int(parts[2])
                access_type = cache_controller_list[core_id].load_modified(address)

            elif opcode == 'IN':
                address = int(parts[2])
                access_type = cache_controller_list[core_id].invalidate(address)


            elif opcode == 'ADD':
                if len(parts) == 4:
                    address = int(parts[2])
                    immediate = int(parts[3])
                    access_type = cache_controller_list[core_id].add(address,immediate)
                else:
                    print("Error: ADD instruction requires an immediate value")

            else:
                print(f"Unknown opcode: {opcode}")
                continue

            if access_type is not None:
                if access_type == 1:
                    print('hit')
                core_access_logs[core_id].append(('hit' if access_type == 1 else 'miss', cycle))
            cycle += 1
            directory_updates_points.append(directory_controller.directory_updates)

            dump_file.write(f"Core {core_id} executed instruction {instruction}\n")
            logger.log_cache_state(core_id, dump_file)
            logger.log_directory_state(dump_file)
            # logger.log_memory_content(dump_file)
        else:
            print("Error: Core ID or address out of range")

    f = open("dump2.txt", "w")
    logger.log_directory_state(f)
    logger.log_memory_content(f)
    f.close()
    dump_file.close()
    print(core_access_logs)
    plot.generate_plots(core_access_logs, hit_time, 2*hit_time)
    plt.plot(directory_updates_points[:30])
    plt.xlabel('Time')
    plt.ylabel('Directory updates')
    plt.title('Directory updates vs Time')
    plt.show()
    print('Num of directory updates: ', directory_controller.directory_updates)


if __name__ == "__main__":
    main()