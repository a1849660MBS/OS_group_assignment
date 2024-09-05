"""
This is the group work of:

Marwan Salih      a1849660
Leon Xie          a1854587
Jiahui Huang      a1896716

This code is protected by the intellectual property rights of our group. 
Do not copy, distribute, or use any part of this code without explicit permission 
from the group members. Unauthorized use or plagiarism of this code will be reported 
to the University of Adelaide and dealt with according to the university's policies on academic integrity.
"""


from mmu import MMU

class ClockMMU(MMU):
    # Initializes the Clock MMU with the given number of frames frame lists etc
    def __init__(self, frames):
        self.frames = frames
        self.frame_list = [None] * frames
        self.use_bits = [0] * frames
        self.page_table = {}
        self.clock_hand = 0
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0

    #this finction goes to the specfic page number and reads from ut
    def read_memory(self, page_number):
        # If the page is not in memory (page table), a page fault occurs else the page is in memebry
        if page_number not in self.page_table:
            self.page_faults += 1
            self.disk_reads += 1
            self._replace_page(page_number, write=False)
        else:
            # If the page is already in memory, update the use bit
            frame_index = self.page_table[page_number]
            self.use_bits[frame_index] = 1

    #this function writes to the memery
    def write_memory(self, page_number):
        # Same as read_memory but also sets the dirty bit (indicating a write)
        if page_number not in self.page_table:
            self.page_faults += 1
            self.disk_reads += 1
            self._replace_page(page_number, write=True)
        else:
            # If the page is already in memory, update the use and dirty bit
            frame_index = self.page_table[page_number]
            self.use_bits[frame_index] = 1
            self.frame_list[frame_index] = (page_number, True)  # Mark as dirty


    # This function Replaces a page using the clock algorithm
    def _replace_page(self, page_number, write):
        while True:
            if self.use_bits[self.clock_hand] == 0:
                # Replace the page at the clock hand position
                if self.frame_list[self.clock_hand] is not None:
                    old_page, is_dirty = self.frame_list[self.clock_hand]
                    if is_dirty:
                        # If the page is dirty, write it to disk
                        self.disk_writes += 1
                    del self.page_table[old_page]

                # # Insert the new page into the clock hand position
                self.frame_list[self.clock_hand] = (page_number, write)
                self.page_table[page_number] = self.clock_hand
                self.use_bits[self.clock_hand] = 1
                # Move the clock hand to the next position
                self.clock_hand = (self.clock_hand + 1) % self.frames
                break
            else:
                # Reset the use bit and advance the clock hand
                self.use_bits[self.clock_hand] = 0
                self.clock_hand = (self.clock_hand + 1) % self.frames

    #Thsi function Prints the current state of the page table, use bits, and other stats
    def print_page_table(self):
        print("Frame list:", self.frame_list)
        print("Use bits:", self.use_bits)
        print("Clock hand position:", self.clock_hand)
        print("Page table:", self.page_table)
        print("Disk reads:", self.disk_reads)
        print("Disk writes:", self.disk_writes)
        print("Page faults:", self.page_faults)

    #These three functions are easy enough to understand, retursn the total number of disk reads, writes and page faults
    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
