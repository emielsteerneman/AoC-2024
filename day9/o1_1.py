def simulate_compaction(disk_map_str):
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
    
    # Simulate the compaction step-by-step.
    # While there's a '.' that is not at the trailing end (i.e., a '.' that occurs before any file block to the right):
    # We move one block from the rightmost file block to fill that '.'.
    
    while True:
        # Find the leftmost '.' that occurs before the last file block
        # Essentially, we want to know if there's a '.' anywhere that is not at the extreme right after all files.
        # More specifically, we need to check if there exists a '.' before the rightmost file character.
        
        # Locate the rightmost file block position
        rightmost_file_pos = None
        for i in range(len(layout)-1, -1, -1):
            if layout[i] != '.':
                rightmost_file_pos = i
                break
        
        if rightmost_file_pos is None:
            # No files at all, just free space
            break
        
        # Find a '.' that is to the left of this rightmost file block position
        dot_pos = None
        for i in range(rightmost_file_pos):
            if layout[i] == '.':
                dot_pos = i
                break
        
        if dot_pos is None:
            # No '.' before the last file block, so we are fully compacted
            break
        
        # Move one block from the rightmost file block to this dot
        # Find the rightmost file block (it's at rightmost_file_pos we found)
        # We take that block and place it into dot_pos, and replace that block's old position with '.'
        
        block_to_move = layout[rightmost_file_pos]
        layout[dot_pos] = block_to_move
        layout[rightmost_file_pos] = '.'
    
    # Compute the checksum
    checksum = 0
    for pos, ch in enumerate(layout):
        if ch != '.':
            fid = int(ch)
            checksum += pos * fid
    
    return checksum

# Given input
input_str = open("input.txt").read()
result = simulate_compaction(input_str)
print("Checksum:", result)
