"""
Memory Simulator
"""
import sys
from clockmmu import ClockMMU
from lrummu import LruMMU
from randmmu import RandMMU

def main():
    """Main function to run the memory simulator."""
    PAGE_OFFSET = 12  # Page size is 2^12 = 4KB

    ############################
    # Check input parameters   #
    ############################

    if len(sys.argv) < 5:
        print("Usage: python memsim.py inputfile numberframes replacementmode debugmode")
        return

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            trace_contents = file.readlines()  # This line is just to check if the file opens correctly
    except FileNotFoundError:
        print(f"Input file '{input_file}' could not be found.")
        print("Usage: python memsim.py inputfile numberframes replacementmode debugmode")
        return

    try:
        frames = int(sys.argv[2])
        if frames < 1:
            print("Frame number must be at least 1.")
            return
    except ValueError:
        print("Invalid number of frames. Must be an integer.")
        return

    replacement_mode = sys.argv[3].lower()

    # Setup MMU based on replacement mode
    if replacement_mode == "rand":
        mmu = RandMMU(frames)
    elif replacement_mode == "lru":
        mmu = LruMMU(frames)
    elif replacement_mode == "clock":
        mmu = ClockMMU(frames)
    else:
        print("Invalid replacement mode. Valid options are [rand, lru, clock]")
        return

    debug_mode = sys.argv[4].lower()

    # Set debug mode
    if debug_mode == "debug":
        mmu.set_debug()
    elif debug_mode == "quiet":
        mmu.reset_debug()
    else:
        print("Invalid debug mode. Valid options are [debug, quiet]")
        return

    ############################################################
    # Main Loop: Process the addresses from the trace file     #
    ############################################################

    no_events = 0

    with open(input_file, 'r', encoding='utf-8') as trace_file:
        for trace_line in trace_file:
            trace_cmd = trace_line.strip().split()

            # Check if the line is a summary line and skip it
            if "total memory frames" in trace_line or \
               "events in trace" in trace_line or \
               "total disk reads" in trace_line or \
               "total disk writes" in trace_line or \
               "page fault rate" in trace_line:
                continue  # Ignore these lines

            # Debug output to show line being processed
            #print(f"Processing line: {trace_line.strip()}")

            # Ensure the line has exactly two parts: address and mode
            if len(trace_cmd) != 2:
                print(f"Skipping invalid line (wrong format): {trace_line.strip()}")
                continue

            try:
                logical_address = int(trace_cmd[0], 16)
                page_number = logical_address >> PAGE_OFFSET

                # Process read or write
                if trace_cmd[1] == "R":
                    mmu.read_memory(page_number)
                elif trace_cmd[1] == "W":
                    mmu.write_memory(page_number)
                else:
                    print(f"Badly formatted operation on line {no_events + 1}: {trace_line.strip()}")
                    continue

                no_events += 1

            except ValueError as e:
                print(f"Error parsing line: {trace_line.strip()}")
                print(e)
                continue

    # Print the page table if in debug mode
    if debug_mode == "debug":
        mmu.print_page_table()

    # Output results
    print(f"total memory frames: {frames}")
    print(f"events in trace: {no_events}")
    print(f"total disk reads: {mmu.get_total_disk_reads()}")
    print(f"total disk writes: {mmu.get_total_disk_writes()}")
    if no_events > 0:
        print(f"page fault rate: {mmu.get_total_page_faults() / no_events:.4f}")
    else:
        print("page fault rate: N/A (no events processed)")

if __name__ == "__main__":
    main()
