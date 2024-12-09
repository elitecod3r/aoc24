
def compute_checksum_p1(num_string):
    # Make string even length to simplify logic 
    if len(num_string) % 2 == 1:   # 
        num_string += '0'

    left_index = -1
    right_index = len(num_string) 
    block_index = 0        # tracks location in expanded string
    checksum = 0
    left_free = 0
    right_file = 0
    
    while True:
        if left_free > 0 and right_file > 0:
            file_index = right_index // 2
            while left_free > 0 and right_file > 0:
                checksum += block_index * file_index
                block_index += 1
                left_free -= 1
                right_file -= 1

        # We always try to move the left index first
        # 
        if right_index - left_index < 2:
            break

        if left_free == 0:
            # Prcoess all the file blocks
            left_index += 1
            file_blocks = int(num_string[left_index])
            file_index = left_index // 2    
            for i in range(file_blocks):
                checksum += block_index * file_index
                block_index += 1
            
            # Set the variables to process empty block
            left_index += 1
            left_free = int(num_string[left_index])
            # We may crossover if we increment left_index and decrement right_index
            #   in the same iteration. Let's go back up and check
            continue

        if right_file == 0:
            assert right_index % 2 == 0
            right_index -= 2
            right_file = int(num_string[right_index])

    assert right_index - left_index == 1

    if right_file > 0: 
        file_index = right_index // 2
        while right_file > 0:
            checksum += block_index * file_index
            block_index += 1
            right_file -= 1

    #print(f'block index at the end is {block_index}')
    return checksum

def compute_checksum_p2(num_string):

    # gap_list contains list of free blocks as tuples (index, length) 
    gap_list = []   
    # num_list contains list of file blocks as tuples (index, length) 
    num_list = []
    # block_list contains the list of file blocks. Free blocks are '.', full blocks have numbers
    #  from 0-N. 
    block_list = []   

    #print("Processing ", num_string)
    for idx, num in enumerate(num_string):
        num = int(num)
        if idx % 2 == 0:   # File blocks
            file_id = idx // 2
            num_list.append((file_id, len(block_list), num))
            for i in range(num):
                block_list.append(file_id)
        else:        # Free blocks
            gap_list.append((len(block_list), num))
            for i in range(num):
                block_list.append('.')

    #print(''.join([str(i) for i in block_list]))
    #print(gap_list)
    for file_id, file_idx, file_length in reversed(num_list):
        #print(f'  file_id = {file_id} idx = {file_idx}, length = {file_length}')
        for i in range(len(gap_list)):
            gap_index, gap_length = gap_list[i]
            #print(f'    gap_index = {gap_index} gap_length = {gap_length}')
            if gap_index >= file_idx:
                break
            if gap_length >= file_length:
                #print(f'    Moving file {file_id} into gap {i}')
                # we will move the file into the gap. 
                for j in range(file_idx, file_idx + file_length):
                    block_list[j] = '.'
                for j in range(gap_index, gap_index + file_length):
                    assert block_list[j] == '.'
                    block_list[j] = file_id
                gap_list[i] = (gap_index + file_length, gap_length - file_length)
                break
        #print(''.join([str(i) for i in block_list]))
        #print(gap_list)
    
    checksum = 0
    for block_idx, block in enumerate(block_list):
        if block != '.':
            checksum += block_idx * block
    
    #print(''.join([str(i) for i in block_list]))
    # 9166126041090 is too high
    # 6311837662089
    return checksum

def read_file(filename):
    with open(filename, 'r') as f:
        return f.readline().strip()

def test_compute_checksum_p1():
    assert compute_checksum_p1('9') == 0
    assert compute_checksum_p1('1234') == 6
    assert compute_checksum_p1('12345') == 60
    assert compute_checksum_p1('123456') == 60
    assert compute_checksum_p1('2333133121414131402') == 1928
    assert compute_checksum_p1(read_file('day9_sample.txt')) == 1928

def test_compute_checksum_p2():
    assert compute_checksum_p2('9') == 0
    assert compute_checksum_p2('1234') == 12
    assert compute_checksum_p2('1434') == 6
    assert compute_checksum_p2('2333133121414131402') == 2858


if __name__ == '__main__':
    print('Part1')
    print('Sample = ', compute_checksum_p1(read_file('day9_sample.txt')))
    print('Input = ', compute_checksum_p1(read_file('day9_input.txt')))
    print('')

    print('Part2')
    print('Sample = ', compute_checksum_p2('2333133121414131402') )
    print('Input = ', compute_checksum_p2(read_file('day9_input.txt')))