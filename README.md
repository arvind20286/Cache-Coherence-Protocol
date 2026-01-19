# Cache Simulator README

## Overview
This project simulates a cache coherence system with multiple cores, cache memories, a directory controller, and main memory. The goal is to model and analyze the behavior of a cache coherence protocol to ensure data consistency across different cores in a multi-core processor.

## Files Description
1. `main.py`: The main script orchestrates the simulation. It initializes cache memories, the directory controller, and other components. The script reads instructions from an input file, executes them, and logs the system state. It also generates plots and log files for analysis.

2. `CacheMemory.py`: This module defines the structure of the cache memory system. It includes two main classes: `CacheLine` representing a single cache line, and `CacheSet` representing a set of cache lines. The `CacheMemory` class orchestrates these sets and manages cache operations such as reading and writing. It also implements the Least Recently Used (LRU) line replacement policy.

3. `CacheController.py`: Defines the `CacheController` class, handling cache operations, block finding, and interaction with the directory controller.

4. `directory.py`: Includes `DirectoryEntry` and `DirectoryController` classes for managing cache coherence and interactions between different caches.

5. `Logger.py`: The logger records the state of cache memories, the directory controller, and main memory after each instruction execution. The `Logger` class in this module facilitates tracking and analysis of the cache coherence system's dynamics over time.

6. `Plot.py`: This module generates plots for average latency and miss rates based on core access logs. It utilizes data collected during the simulation to create visual representations, aiding in understanding system performance.

## Instruction Semantics
- The simulator follows a simplified instruction set to simulate cache operations.
- Instructions include cache read/write and cache coherence commands.
- Each instruction is parsed and executed to simulate its effect on cache states and memory.

## Building Instructions
- Ensure you have Python (version 3.x or above) installed on your system.
- No external libraries are required for the basic functionality of this simulator.
- For visualizing results (if required), install matplotlib using `pip install matplotlib`.

## Usage Instructions
1. Navigate to the directory containing the simulator files.
2. Run the simulator using the command line:
   ```
   python main.py
   ```
3. Optional command line arguments can be provided to customize the simulation parameters such as the number of cores, cache size, etc.
4. The simulator will execute and provide output based on the predefined test cases or instructions fed into the system.

## Output
The simulation generates log files (`dump.txt` and `dump2.txt`) and plots (`average_latency.png` and `miss_rates.png`) for analyzing cache and directory states, memory content, and system performance metrics.

## Additional Notes
- Modify `main.py` to include different test scenarios or to change the default system configuration.
- For detailed logging, check the `Logger` class functionality within the code.
- The simulator is extensible for further features like different cache replacement policies or coherence protocols.