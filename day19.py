import re
# Values for the grid 

def read_file(filename):
    patterns = []
    designs = []
    
    with open(filename, 'r') as f:
        pattern = f.readline().strip()
        patterns = [s.strip() for s in pattern.split(',')]
        for line in f:
            if line == '\n':
                continue
            designs.append(line.strip())

    return (patterns, designs)

def test_read_file():
    patterns, designs = read_file('day19_sample.txt')

    assert len(patterns) == 8
    assert patterns[0] == 'r'
    assert patterns[7] == 'br'
    assert len(designs) == 8
    assert designs[0] == 'brwrr'
    assert designs[7] == 'bbrgwb'


def is_possible(patterns, design, possible_designs):
    # Can we make the design using patterns 
    if design == '':
        return True
    
    if design in possible_designs:
        return possible_designs[design]
    
    for pattern in patterns:
        # if pattern matches start of the design, remove it and recusively check
        if design.startswith(pattern):
            new_design = design[len(pattern):]
            if is_possible(patterns, new_design, possible_designs):
                possible_designs[new_design] = True
                return True
            else:
                possible_designs[new_design] = False
    return False

def count_possible(patterns, designs):
    count = 0
    possible_designs = {}

    for design in designs:
        print('testing design:', design, end=' ')
        if is_possible(patterns, design, possible_designs):
            print('matches')
            count += 1
        else:
            print('no match')
    return count

def test_count_possible():
    patterns, designs = read_file('day19_sample.txt')
    assert count_possible(patterns, designs) == 6
 

if __name__ == '__main__':
    print('Main')
    patterns, designs = read_file('day19_input.txt')
    print('Part1 = ', count_possible(patterns, designs))