

def read_file(filename):
    num_list = []
    with open(filename) as f:
        for line in f:
            n = int(line.strip())
            num_list.append(n)
    return num_list

def test_read_file():
    numlist = read_file('day22_sample.txt')
    assert len(numlist) == 4
    assert numlist[0] == 1 
    assert numlist[3] == 2024

def mix_prune(num1, num2):
    num1 = num1 ^ num2
    num1 = num1 % 16777216
    return num1

def one_step(number):
    number = mix_prune(number, number * 64)
    number = mix_prune(number, int(number / 32))
    number = mix_prune(number, number * 2048)
    return number
    
def find_next_value(number, iterations):
    for _ in range(iterations):
        number = one_step(number)
    return number 

def test_find_next_value():
    assert find_next_value(123, 1) == 15887950
    assert find_next_value(123, 10) == 5908254

def find_answer(numlist, iterations):
    total = 0
    for num in numlist:
        x = find_next_value(num, iterations)
        total += x
    return total

def seq_to_string(seq):
    b4 = (seq & 0xFF) - 20
    seq = seq >> 8
    b3 = (seq & 0xFF) - 20
    seq = seq >> 8
    b2 = (seq & 0xFF) - 20
    seq = seq >> 8
    b1 = (seq & 0xFF) - 20
    return " ".join([str(b1), str(b2), str(b3), str(b4)])
    
def part2(numlist, iterations):
    # We store number of bananas for a sequence mask for all price-chains
    seq_count_dict = {}
    max_bananas = 0
    max_seq = 0

    for num in numlist:
        #number = one_step(number)
        # seq_mask contains the last 4 values in each of the 4 bytes
        seq_mask = 0
        for i in range(3):
            prev_num = num
            num = one_step(num)
            # delta would be in range -18 to +18. We normalize by adding 20 so
            #  the number would be in range 2 to 38
            delta = num % 10 - prev_num % 10 + 20
            seq_mask = seq_mask << 8 | delta
            #print(f'*{i:2d} = {num:8d} {delta-20}, seq_mask = {seq_to_string(seq_mask)}')

        # We process a seq_mask for a price-chain only once. We will use this set to 
        #  track if we have seen the seq_mask before 
        seq_mask_set = set()

        for i in range(3, iterations):
            prev_num = num
            num = one_step(num)
            delta = num % 10 - prev_num % 10 + 20
            seq_mask = (seq_mask << 8 | delta) & 0xFFFFFFFF 
            #print(f'{i:2d} = {num:8d} {delta-20}, seq_mask = {seq_to_string(seq_mask)}')
            if seq_mask in seq_mask_set:
                continue
            seq_mask_set.add(seq_mask)

            if seq_mask in seq_count_dict:
                seq_count_dict[seq_mask] += num % 10
            else:
                seq_count_dict[seq_mask] = num % 10

            if seq_count_dict[seq_mask] > max_bananas:
                max_bananas = seq_count_dict[seq_mask]
                max_seq = seq_mask

    return max_bananas


if __name__ == '__main__':    
    print('Part 1')
    print('Sample = ', find_answer([1, 10, 100, 2024], 2000))
    print('Input  = ', find_answer(read_file('day22_input.txt'), 2000))

    print('Part 2')
    print('Sample = ', part2([1, 2, 3, 2024], 2000))
    print('Input  = ', part2(read_file('day22_input.txt'), 2000))