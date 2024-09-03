class Page:
    def __init__(self, page_number):
        self.page_number = page_number
        self.reference_bit = 0

class ClockReplacement:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = []
        self.clock_hand = 0

    def page_fault_occurred(self, page_number):
        for page in self.frames:
            if page.page_number == page_number:
                page.reference_bit = 1
                return False
        return True

    def replace_page(self, page_number):
        while True:
            current_page = self.frames[self.clock_hand]
            if current_page.reference_bit == 0:
                print(f"Replacing page {current_page.page_number} with page {page_number}")
                self.frames[self.clock_hand] = Page(page_number)
                self.clock_hand = (self.clock_hand + 1) % self.num_frames
                break
            else:
                current_page.reference_bit = 0
                self.clock_hand = (self.clock_hand + 1) % self.num_frames

    def process_page(self, page_number):
        if self.page_fault_occurred(page_number):
            print(f"Page fault occurred for page {page_number}")
            if len(self.frames) < self.num_frames:
                print(f"Adding page {page_number} to memory")
                self.frames.append(Page(page_number))
            else:
                self.replace_page(page_number)
        else:
            print(f"Page {page_number} found in memory")

def main():
    clock_replacement = ClockReplacement(num_frames=3)

    page_references = [1, 2, 3, 2, 4, 1, 5, 2, 4, 6]
    
    for page_number in page_references:
        clock_replacement.process_page(page_number)

if __name__ == "__main__":
    main()
