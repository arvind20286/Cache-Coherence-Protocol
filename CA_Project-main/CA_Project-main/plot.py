import matplotlib.pyplot as plt
def calculate_metrics(core_access_logs, hit_time, miss_penalty):
    average_latencies = {}
    miss_rates = {}
    hit_rates = {}
    total_accesses = {}
    total_misses = {}
    miss_penalty = 2 * hit_time
     # This would be incremented during your simulation

    # Calculate average latency and miss rate for each core
    for core_id, accesses in enumerate(core_access_logs):
        total_time = 0
        total_accesses[core_id] = len(accesses)
        total_misses[core_id] = sum(1 for access_type, _ in accesses if access_type == 'miss')

        for access_type, cycle_number in accesses:
            if access_type == 'hit':
                total_time += hit_time
            else:
                total_time += hit_time + miss_penalty
        hit_rates[core_id] = (total_accesses[core_id] - total_misses[core_id]) / total_accesses[core_id]
        miss_rates[core_id] = total_misses[core_id] / total_accesses[core_id]
        # average_latencies[core_id] = total_time / total_accesses[core_id]
        average_latencies[core_id] = (hit_rates[core_id] * hit_time) + (miss_rates[core_id] * miss_penalty)

    return average_latencies, miss_rates

def generate_plots(core_access_logs, hit_time, miss_penalty):
    average_latencies, miss_rates = calculate_metrics(core_access_logs, hit_time, miss_penalty)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(average_latencies.values(), 'o-')
    plt.xticks(list(average_latencies.keys()))
    plt.xlabel('Core ID')
    plt.ylabel('Average Latency')
    plt.subplot(1, 2, 2)
    plt.plot(miss_rates.values(), 'o-')
    plt.xticks(list(miss_rates.keys()))
    plt.xlabel('Core ID')
    plt.ylabel('Miss Rate')
    plt.show()
