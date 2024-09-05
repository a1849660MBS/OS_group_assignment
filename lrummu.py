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
from collections import OrderedDict

class LruMMU(MMU):
    #again this is the constructorm creates the LRU with the set amount of frames and page table etc
    def __init__(self, frames):
        self.frames = frames
        self.page_table = OrderedDict()
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False

    #these two fucntions check if debug mode is true or not by default is false
    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    #functions that reads the memory
    def read_memory(self, page_number):
         # If the page is not in memory, handle page fault
        if page_number not in self.page_table:
            self.page_faults += 1
            if len(self.page_table) < self.frames:
                # If there is space, simply add the page
                self.page_table[page_number] = 'clean'
            else:
                # Otherwise, evict the least recently used page
                victim, status = self.page_table.popitem(last=False)
                if status == 'dirty':
                    self.disk_writes += 1
                self.page_table[page_number] = 'clean'
            self.disk_reads += 1
        else:
            # Update the LRU tracker for the page
            self.page_table.move_to_end(page_number, last=True)

    # fucntion that writes to memory
    def write_memory(self, page_number):
         # Perform a read operation and mark the page as dirty
        self.read_memory(page_number)
        self.page_table[page_number] = 'dirty'

    
    
    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
