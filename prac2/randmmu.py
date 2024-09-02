from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.memory = {}
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
            if self.debug:
                print(f"Read page {page_number} from memory.")
        else:
            self.page_faults += 1
            if len(self.memory) < self.frames:
                self.memory[page_number] = True
            else:
                self._replace_page(page_number)
            self.disk_reads += 1
            if self.debug:
                print(f"Page fault occurred. Read page {page_number} from disk.")

    def write_memory(self, page_number):
        if page_number in self.memory:
            if self.debug:
                print(f"Write to page {page_number} in memory.")
        else:
            self.page_faults += 1
            if len(self.memory) < self.frames:
                self.memory[page_number] = True
            else:
                self._replace_page(page_number)
            self.disk_reads += 1
            self.disk_writes += 1
            if self.debug:
                print(f"Page fault occurred. Write to page {page_number} in disk.")

    def _replace_page(self, page_number):
        random_page = random.choice(list(self.memory.keys()))
        del self.memory[random_page]
        self.disk_writes += 1  # Increment disk writes when replacing a page
        self.memory[page_number] = True

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
