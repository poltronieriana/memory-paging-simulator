class TableEntry:
    """Represents an entry in the page table"""
    def __init__(self, page_number):
        self.page_number = page_number
        self.frame_number = -1  # -1 indicates not in physical memory
        self.present = False    # Presence bit
    
    def __repr__(self):
        status = f"Frame {self.frame_number}" if self.present else "Not in memory"
        return f"Page {self.page_number}: {status}"


class PageTable:
    """Page table - maps virtual pages to physical frames"""
    def __init__(self, num_pages):
        lista = []
        for i in range(num_pages):
            lista.append(TableEntry(i))
            self.entries = lista
    
    def get_entry(self, page_number):
        """Returns the table entry for a specific page"""
        if 0 <= page_number < len(self.entries):
            return self.entries[page_number]
        return None
    
    def set_mapping(self, page_number, frame_number):
        """Sets the mapping page -> frame"""
        entry = self.get_entry(page_number)
        if entry:
            entry.frame_number = frame_number
            entry.present = True
    
    def remove_mapping(self, page_number):
        """Removes a page from physical memory"""
        entry = self.get_entry(page_number)
        if entry:
            entry.frame_number = -1
            entry.present = False
    
    def is_present(self, page_number):
        """Checks if the page is present in physical memory"""
        entry = self.get_entry(page_number)
        if entry:
            return entry.present
        else:
            return False
    
    def get_frame(self, page_number):
        """Returns the frame number where the page is located (or -1)"""
        entry = self.get_entry(page_number)
        if entry:
            return entry.frame_number
        else:
            return -1      
             
    def __str__(self):
        result = "Page Table:\n"
        result += "-" * 40 + "\n"
        for entry in self.entries:
            result += f"  {entry}\n"
        return result


class PhysicalMemory:
    """Physical memory - collection of frames"""
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = [-1] * num_frames  # -1 = empty frame
    
    def allocate_frame(self, frame_number, page_number):
        """Allocates a page to a specific frame"""
        if 0 <= frame_number < self.num_frames:
            self.frames[frame_number] = page_number
            return True
        return False
    
    def free_frame(self, frame_number):
        """Frees a frame"""
        if 0 <= frame_number < self.num_frames:
            self.frames[frame_number] = -1
    
    def get_page_in_frame(self, frame_number):
        """Returns which page is in a frame"""
        if 0 <= frame_number < self.num_frames:
            return self.frames[frame_number]
        return -1
    
    def __str__(self):
        result = "Physical Memory:\n"
        result += "-" * 40 + "\n"
        for i, page in enumerate(self.frames):
            status = f"Page {page}" if page != -1 else "Empty"
            result += f"  Frame {i}: {status}\n"
        return result