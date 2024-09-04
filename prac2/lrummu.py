from mmu import MMU
from collections import OrderedDict

class LruMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.page_table = OrderedDict()  # The page table to track pages
        self.page_faults = 0
        self.disk_reads = 0
        self.disk_writes = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
        if page_number not in self.page_table:
            self.page_faults +=1
            if len(self.page_table) < self.frames:
                self.page_table[page_number] = 'clean'
            else:
                victim, status = self.page_table.popitem(last=False)
                if status == 'dirty':
                    slef.disk_writes += 1
                self.page_table[page_number] = 'clean'
            self.disk_reads += 1
        else:
            self.page_table.move_to_end(page_number, last=True)

    def write_memory(self, page_number):
        self.read_memory(page_number)
        self.page_table[page_number] = 'dirty'

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
