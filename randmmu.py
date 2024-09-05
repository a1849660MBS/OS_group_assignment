
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


import random
from mmu import MMU

class RandMMU(MMU):
    # Initializes the random MMU with the given number of frames
    def __init__(self, frames):
        self.frames = frames
        self.page_table = {}
        self.frame_list = []
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False
    
    #these two fucntions check if debug mode is true or not by default is false
    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False
     
    # Handles a memory read
    def read_memory(self, page_number):
        #handles a page fault like all the other mmu modules
        if page_number not in self.page_table:
            self.page_faults += 1

            #if the length of the frame list is les than the nyumber of frames then appened the page to the frame list
            if len(self.frame_list) < self.frames:
                self.frame_list.append(page_number)
            else:

                #else choose at random a page to evict from emeor
                victim = random.choice(self.frame_list)
                if self.page_table[victim] == 'dirty':
                    self.disk_writes += 1
                self.frame_list.remove(victim)
                self.frame_list.append(page_number)
                self.page_table.pop(victim)
            self.page_table[page_number] = 'clean'
            self.disk_reads += 1

    #functon that writes to memory
    def write_memory(self, page_number):
        self.read_memory(page_number)
        self.page_table[page_number] = 'dirty'

    #These three functions are easy enough to understand, retursn the total number of disk reads, writes and page faults
    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
