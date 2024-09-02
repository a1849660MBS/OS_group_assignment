from mmu import MMU
# test versin
class ClockMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.memory = {}
        self.clock_hand = 0
        self.reference_bits = {}
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
            self.reference_bits[page_number] = 1
            if self.debug:
                print(f"Read page {page_number} from memory.")
        else:
            self.page_faults += 1
            if len(self.memory) < self.frames:
                self.memory[page_number] = True
                self.reference_bits[page_number] = 1
            else:
                self._replace_page(page_number)
            self.disk_reads += 1
            if self.debug:
                print(f"Page fault occurred. Read page {page_number} from disk.")

    def write_memory(self, page_number):
        if page_number in self.memory:
            self.reference_bits[page_number] = 1
            if self.debug:
                print(f"Write to page {page_number} in memory.")
        else:
            self.page_faults += 1
            if len(self.memory) < self.frames:
                self.memory[page_number] = True
                self.reference_bits[page_number] = 1
            else:
                self._replace_page(page_number)
            self.disk_reads += 1
            self.disk_writes += 1
            if self.debug:
                print(f"Page fault occurred. Write to page {page_number} in disk.")

    def _replace_page(self, page_number):
        while True:
            current_page = list(self.memory.keys())[self.clock_hand]
            if self.reference_bits[current_page] == 0:
                del self.memory[current_page]
                del self.reference_bits[current_page]
                self.memory[page_number] = True
                self.reference_bits[page_number] = 1
                break
            else:
                self.reference_bits[current_page] = 0
            self.clock_hand = (self.clock_hand + 1) % self.frames

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
