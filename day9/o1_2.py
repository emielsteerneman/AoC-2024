def compact_whole_files(disk_map_str):
    # Parse the input into file and free segments
    digits = list(map(int, disk_map_str))
    
    file_lengths = []
    free_lengths = []
    
    for i, d in enumerate(digits):
        if i % 2 == 0:
            file_lengths.append(d)
        else:
            free_lengths.append(d)
    
    # Construct the initial disk layout
    layout = []
    for i, flen in enumerate(file_lengths):
        layout.extend([str(i)] * flen)
        if i < len(free_lengths):
            layout.extend(['.'] * free_lengths[i])
    
    # Helper function to find all runs of free space ('.') in the layout
    def find_free_spans():
        spans = []
        start = None
        for i, ch in enumerate(layout):
            if ch == '.':
                if start is None:
                    start = i
            else:
                if start is not None:
                    spans.append((start, i - 1))
                    start = None
        if start is not None:
            spans.append((start, len(layout) - 1))
        return spans
    
    # Helper to find file positions
    def find_file_positions(fid):
        # Return the start and end indices of the contiguous blocks that form this file
        # Assumption: Files are contiguous. If not, we must consider them as found in the layout.
        # The puzzle states files are initially laid out with free space in between, 
        # but each file segment should be contiguous to itself.
        # If not contiguous, we must treat them as a single block anyway? 
        # The problem states each file on disk also has an ID; presumably each file is in one contiguous region.
        
        positions = [i for i, ch in enumerate(layout) if ch == str(fid)]
        if not positions:
            return None
        return min(positions), max(positions)
    
    # Move files in order of decreasing file ID number
    for fid in range(len(file_lengths)-1, -1, -1):
        file_range = find_file_positions(fid)
        if file_range is None:
            # File not found? Possibly it was moved or something odd.
            continue
        file_start, file_end = file_range
        file_size = (file_end - file_start + 1)
        
        # Find a free span to the left of file_start that can hold file_size
        # The free span must be entirely to the left of file_start: 
        # meaning the free span's end < file_start.
        
        free_spans = find_free_spans()
        
        # Filter free spans that end before file_start (to the left of the file)
        # Actually, the puzzle states: "If there is no span of free space to the left of a file that 
        # is large enough to fit the file, the file does not move." 
        # This suggests the entire span must be to the left of the file start, 
        # so span_end < file_start.
        
        valid_spans = [(s, e) for (s, e) in free_spans if e < file_start and (e - s + 1) >= file_size]
        
        if not valid_spans:
            # No suitable span, do not move
            continue
        
        # Choose the leftmost suitable span (the one with the smallest start index)
        valid_spans.sort(key=lambda span: span[0])
        chosen_span = valid_spans[0]
        span_start, span_end = chosen_span
        
        # Move the file to the leftmost part of this chosen span
        # We'll occupy span_start to span_start + file_size - 1 with this file
        new_start = span_start
        new_end = span_start + file_size - 1
        
        # Clear old file positions (replace with '.')
        for pos in range(file_start, file_end + 1):
            layout[pos] = '.'
        
        # Place the file at the new location
        for pos in range(new_start, new_end + 1):
            layout[pos] = str(fid)
    
    # Compute checksum
    checksum = 0
    for pos, ch in enumerate(layout):
        if ch != '.':
            fid = int(ch)
            checksum += pos * fid
    
    return checksum

# Example usage:
# input_str = "2333133121414131402" # from the puzzle example for part 2 testing
# print(compact_whole_files(input_str)) # should produce 2858 for the example

# The function above can be used directly with the puzzle input for Part Two

# Given input
input_str = open("input.txt").read()
result = compact_whole_files(input_str)
print("Checksum:", result)