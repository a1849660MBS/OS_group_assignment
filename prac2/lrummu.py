from mmu import MMU
from collections import OrderedDict

class LruMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.memory = OrderedDict()
        self.page_faults = 0
        self.disk_reads = 0
        self.disk_writes = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
        if page_number in self.memory:
            self.memory.move_to_end(page_number)
            if self.debug:
                print(f"Read page {page_number} from memory.")
        else:
            self.page_faults += 1
            if len(self.memory) >= self.frames:
                self.memory.popitem(last=False)
            self.memory[page_number] = True
            self.disk_reads += 1
            if self.debug:
                print(f"Page fault occurred. Read page {page_number} from disk.")

    def write_memory(self, page_number):
        if page_number in self.memory:
            self.memory.move_to_end(page_number)
            if self.debug:
                print(f"Write to page {page_number} in memory.")
        else:
            self.page_faults += 1
            if len(self.memory) >= self.frames:
                self.memory.popitem(last=False)
            self.memory[page_number] = True
            self.disk_reads += 1
            self.disk_writes += 1
            if self.debug:
                print(f"Page fault occurred. Write to page {page_number} in disk.")

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
