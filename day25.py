
def read_file(filename):

    locks = []
    keys = []

    with open(filename) as f:
        while True:
            grid = []
            for i in range(7):
                line = f.readline().strip()
                grid.append([c for c in line])
            
            is_key = True
            end_char = '#'
            if grid[0][0] == '#':
                is_key = False
                end_char = '.'

            pin_heights = []
            for col in range(5):
                for row in range(1,7):
                    if grid[row][col] == end_char:
                        if is_key:
                            pin_heights.append(5 - row + 1)
                        else:
                            pin_heights.append(row - 1)
                        break
            if is_key:
                keys.append(pin_heights)
            else:   
                locks.append(pin_heights)

            line = f.readline()
            if not line:
                break
    return locks, keys

def test_read_file():
    locks, keys = read_file('day25_sample.txt')
    assert locks[0] == [0,5,3,4,3]
    assert locks[1] == [1,2,0,5,3]
    assert keys[0] == [5,0,2,1,3]
    assert keys[1] == [4,3,4,0,2]
    assert keys[2] == [3,0,2,0,1]

def match_lock_key(lock, key):
    for i in range(5):
        if lock[i] + key[i] > 5:
            return 0
    return 1

def find_matches(locks, keys):
    count = 0
    for lock in locks:
        for key in keys:
            count += match_lock_key(lock, key)
    return count
        

if __name__ == '__main__':    
    print('Part 1')
    print(find_matches(*read_file('day25_sample.txt')))
    print(find_matches(*read_file('day25_input.txt')))