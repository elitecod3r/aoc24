
def compute_checksum(num_string):

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

    return checksum



def read_file(filename):
    with open(filename, 'r') as f:
        return f.readline().strip()

def test_compute_checksum():
    assert compute_checksum('9') == 0
    assert compute_checksum('1234') == 6
    assert compute_checksum('12345') == 60
    assert compute_checksum('123456') == 60
    assert compute_checksum('2333133121414131402') == 1928
    assert compute_checksum(read_file('day9_sample.txt')) == 1928

if __name__ == '__main__':
    print('Sample = ', compute_checksum(read_file('day9_sample.txt')))
    print('Input = ', compute_checksum(read_file('day9_input.txt')))