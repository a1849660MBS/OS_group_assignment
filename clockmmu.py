from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.frame_list = [None] * frames
        self.use_bits = [0] * frames
        self.page_table = {}
        self.clock_hand = 0
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0

    def read_memory(self, page_number):
        if page_number not in self.page_table:
            self.page_faults += 1
            self.disk_reads += 1
            self._replace_page(page_number, write=False)
        else:
            # If the page is already in memory, update the use bit
            frame_index = self.page_table[page_number]
            self.use_bits[frame_index] = 1

    def write_memory(self, page_number):
        if page_number not in self.page_table:
            self.page_faults += 1
            self.disk_reads += 1
            self._replace_page(page_number, write=True)
        else:
            # If the page is already in memory, update the use and dirty bit
            frame_index = self.page_table[page_number]
            self.use_bits[frame_index] = 1
            self.frame_list[frame_index] = (page_number, True)  # Mark as dirty

    def _replace_page(self, page_number, write):
        while True:
            if self.use_bits[self.clock_hand] == 0:
                # Replace the page at the clock hand position
                if self.frame_list[self.clock_hand] is not None:
                    old_page, is_dirty = self.frame_list[self.clock_hand]
                    if is_dirty:
                        self.disk_writes += 1
                    del self.page_table[old_page]

                # Insert the new page
                self.frame_list[self.clock_hand] = (page_number, write)
                self.page_table[page_number] = self.clock_hand
                self.use_bits[self.clock_hand] = 1
                self.clock_hand = (self.clock_hand + 1) % self.frames
                break
            else:
                # Reset the use bit and advance the clock hand
                self.use_bits[self.clock_hand] = 0
                self.clock_hand = (self.clock_hand + 1) % self.frames

    def print_page_table(self):
        print("Frame list:", self.frame_list)
        print("Use bits:", self.use_bits)
        print("Clock hand position:", self.clock_hand)
        print("Page table:", self.page_table)
        print("Disk reads:", self.disk_reads)
        print("Disk writes:", self.disk_writes)
        print("Page faults:", self.page_faults)

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
