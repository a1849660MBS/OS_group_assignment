import sys
import time
import matplotlib.pyplot as plt
from clockmmu import ClockMMU
from lrummu import LruMMU
from randmmu import RandMMU

def run_simulation(input_file, frames, replacement_mode, debug_mode):
    PAGE_OFFSET = 12  # Page size is 2^12 = 4KB
    no_events = 0

    # Setup MMU based on replacement mode
    if replacement_mode == "rand":
        mmu = RandMMU(frames)
    elif replacement_mode == "lru":
        mmu = LruMMU(frames)
    elif replacement_mode == "clock":
        mmu = ClockMMU(frames)
    else:
        raise ValueError("Invalid replacement mode. Valid options are [rand, lru, clock]")

    # Set debug mode
    if debug_mode == "debug":
        mmu.set_debug()
    elif debug_mode == "quiet":
        mmu.reset_debug()

    with open(input_file, 'r', encoding='utf-8') as trace_file:
        for trace_line in trace_file:
            trace_cmd = trace_line.strip().split()

            # Skip summary lines
            if any(keyword in trace_line for keyword in ["total memory frames", "events in trace", "total disk reads", "total disk writes", "page fault rate"]):
                continue

            # Ensure the line has exactly two parts: address and mode
            if len(trace_cmd) != 2:
                continue

            try:
                logical_address = int(trace_cmd[0], 16)
                page_number = logical_address >> PAGE_OFFSET

                if trace_cmd[1] == "R":
                    mmu.read_memory(page_number)
                elif trace_cmd[1] == "W":
                    mmu.write_memory(page_number)
                else:
                    continue

                no_events += 1
            except ValueError:
                continue

    page_fault_rate = mmu.get_total_page_faults() / no_events if no_events > 0 else 0
    return no_events, page_fault_rate, mmu.get_total_disk_reads(), mmu.get_total_disk_writes()

def main():
    """Main function to run the memory simulator and plot results."""
    if len(sys.argv) < 3:
        print("Usage: python memsim.py inputfile debugmode")
        return

    input_file = sys.argv[1]
    debug_mode = sys.argv[2].lower()

    frame_sizes = [2**i for i in range(11)]  # Memory frames from 2^0 to 2^10
    replacement_modes = ['lru', 'rand', 'clock']
    
    # Dictionaries to store results
    page_fault_rates = {mode: [] for mode in replacement_modes}
    runtimes = {mode: [] for mode in replacement_modes}

    # Loop through each replacement mode
    for replacement_mode in replacement_modes:
        print(f"Running simulation for {replacement_mode}...")

        for frames in frame_sizes:
            start_time = time.time()  # Start timer
            try:
                no_events, page_fault_rate, _, _ = run_simulation(input_file, frames, replacement_mode, debug_mode)
            except ValueError as e:
                print(e)
                return
            end_time = time.time()  # End timer

            runtime = end_time - start_time  # Calculate runtime
            runtimes[replacement_mode].append(runtime)
            page_fault_rates[replacement_mode].append(page_fault_rate)

            print(f"Frames: {frames}, Mode: {replacement_mode}, Events: {no_events}, Page Fault Rate: {page_fault_rate:.4f}, Runtime: {runtime:.4f}s")

    # Plotting results
    plt.figure(figsize=(10, 5))

    # Page Fault Rate plot (left)
    plt.subplot(1, 2, 1)
    for mode in replacement_modes:
        plt.plot(frame_sizes, page_fault_rates[mode], marker='o', label=mode)
    plt.xscale('log', base=2)
    plt.xlabel('Number of Frames (log scale)')
    plt.ylabel('Page Fault Rate')
    plt.title('Page Fault Rate vs. Memory Frames')
    plt.legend()
    plt.grid(True)

    # Runtime plot (right)
    plt.subplot(1, 2, 2)
    for mode in replacement_modes:
        plt.plot(frame_sizes, runtimes[mode], marker='o', label=mode)
    plt.xscale('log', base=2)
    plt.xlabel('Number of Frames (log scale)')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime vs. Memory Frames')
    plt.legend()
    plt.grid(True)

    # Make layout tight and show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
