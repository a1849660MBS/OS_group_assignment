from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.page_table = {}
        self.frame_list = []
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
        if page_number not in self.page_table:
            self.page_faults += 1
            if len(self.frame_list) < self.frames:
                self.frame_list.append(page_number)
            else:
                victim = random.choice(self.frame_list)
                if self.page_table[victim] == 'dirty':
                    self.disk_writes += 1
                self.frame_list.remove(victim)
                self.frame_list.append(page_number)
                self.page_table.pop(victim)
            self.page_table[page_number] = 'clean'
            self.disk_reads += 1


    def write_memory(self, page_number):
       self.read_memory(page_number)
       self.page_table[page_number] = 'dirty'

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
