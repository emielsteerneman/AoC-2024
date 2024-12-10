from bisect import bisect_left

def part2_compact(disk_map_str):
    digits = list(map(int, disk_map_str))
    files = digits[::2]
    space = digits[1::2] + [0] if len(space := digits[1::2]) < len(files) else space
    
    n = len(files)

    # Build the initial segments
    # segments[i] = [fid, fs, s, start_pos]
    segments = []
    pos = 0
    for fid, (fs, s) in enumerate(zip(files, space)):
        segments.append([fid, fs, s, pos])
        pos += fs + s

    # Map fid to index
    # Initially, fid i is at segments[i]
    fid_to_index = list(range(n))

    # Build free segments from `segments`
    free_segments = []
    for fid, fs, s, start in segments:
        if s > 0:
            free_start = start + fs
            free_segments.append((free_start, s))

    free_segments.sort()  # by start

    # Helper: Insert a free segment and merge if adjacent
    def insert_free_segment(start, length):
        i = bisect_left(free_segments, (start, length))
        
        # Merge with left?
        if i > 0:
            left_start, left_len = free_segments[i-1]
            if left_start + left_len == start:
                # Merge with left
                start = left_start
                length = left_len + length
                free_segments[i-1] = (start, length)
                # Merge with right?
                if i < len(free_segments):
                    right_start, right_len = free_segments[i]
                    if right_start == start + length:
                        # Merge left+right
                        free_segments[i-1] = (start, length + right_len)
                        del free_segments[i]
                return

        # Merge with right?
        if i < len(free_segments):
            right_start, right_len = free_segments[i]
            if right_start == start + length:
                # Merge with right
                free_segments[i] = (start, length + right_len)
                return

        # No merge
        free_segments.insert(i, (start, length))

    # Helper: consume 'amount' from the start of free_segments[idx]
    def consume_free_segment(idx, amount):
        fstart, flen = free_segments[idx]
        if flen == amount:
            del free_segments[idx]
        else:
            # shrink from left
            free_segments[idx] = (fstart + amount, flen - amount)

    # Find a suitable free span to the left of file_start that can hold fs
    def find_free_span(file_start, fs):
        # We want a free segment that ends before file_start and length >= fs
        # Condition: start + length <= file_start
        # We'll linearly check from the left side using binary search to find candidates.
        # Since segments are sorted by start, we find the position where file_start would be inserted.
        
        # All free segments with free_start+free_len <= file_start are candidates
        # We'll binary search on free_segments by start to find the largest start < file_start.
        
        # But we must also check that start+length <= file_start.
        # We'll just do a binary search for first segment that starts >= file_start, 
        # then check all segments before it:
        
        i = bisect_left(free_segments, (file_start, 0))
        # segments at index < i have start < file_start, but we must also ensure they end before file_start
        for j in range(i):
            st, ln = free_segments[j]
            if st + ln <= file_start and ln >= fs:
                return j
        # also check segments at positions before that if needed
        # Actually, since we must pick the leftmost suitable, we should check from left to right:
        # If performance is critical, we might store free segments in a segment tree.
        
        # But let's trust merging keeps free_segments relatively small.
        for j in range(i-1, -1, -1):
            st, ln = free_segments[j]
            if st + ln <= file_start and ln >= fs:
                return j
        
        return None

    # Move files in order of descending fid
    # After moving a file:
    # - The old file position becomes free space.
    # - The chosen free segment shrinks.
    # - Insert the file at the new location with fs and s=0.
    # - Update segments and fid_to_index.
    
    # IMPORTANT: After moving a file, its position changes relative to others.
    # We'll represent the moved file as a new "segment" by modifying its [start_pos].
    # The old location becomes a free segment. 
    # The file effectively "jumps" to the free location without re-sorting the entire array.
    # We must keep segments sorted by start_pos. Since we move files to the left, this can reorder segments.
    # We'll handle this by directly adjusting segments and resorting them once at the end if needed.
    #
    # However, sorting after every move would be expensive. Instead, we can:
    # - Collect moves and do a single final resort if needed.
    #
    # But the problem states we must consider the final checksum after all moves.
    #
    # We'll do this approach:
    # - Keep track of moved files in a separate array.
    # - After all moves, reconstruct final order and compute checksum.
    
    moved_segments = [False]*n

    for current_fid in range(n-1, -1, -1):
        seg_idx = fid_to_index[current_fid]
        fid, fs, s, start = segments[seg_idx]
        
        if fs == 0:
            # File doesn't exist or zero-length file
            continue

        # Find free span to the left
        idx = find_free_span(start, fs)
        if idx is None:
            # can't move
            continue

        # Move the file
        fstart, flen = free_segments[idx]
        # consume fs from this free segment
        consume_free_segment(idx, fs)
        
        new_file_start = fstart
        old_file_start = start
        old_length = fs + s  # old file + following free space now becomes free

        # The file moves to new_file_start with fs size and 0 free after it
        segments[seg_idx][3] = new_file_start  # update start_pos
        segments[seg_idx][2] = 0               # no free space after moving
        moved_segments[seg_idx] = True
        
        # old file location becomes free
        insert_free_segment(old_file_start, old_length)

    # After all moves, we must compute the checksum
    # First, we must have segments sorted by start_pos
    segments.sort(key=lambda x: x[3])

    # Recompute fid_to_index just in case (not strictly needed for checksum)
    # Compute checksum:
    # sum(pos * fid for each file block)
    # With segments sorted by start_pos, position increments by fs+s for each segment.
    
    checksum = 0
    for fid, fs, s, start in segments:
        # file occupies [start..start+fs-1]
        # sum positions = fs*start + (fs*(fs-1))//2
        # multiplied by fid:
        if fs > 0:
            block_sum = fs*start + (fs*(fs-1))//2
            checksum += fid * block_sum

    return checksum

if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().strip()
    print("Answer 2:", part2_compact(data))
