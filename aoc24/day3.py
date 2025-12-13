import sys
import re


def add_mul_part2(input):
    process_flag = True
    total = 0 
    
    pattern = re.compile(r'(do\(\))|(don\'t\(\))|(mul\((\d{1,3}),(\d{1,3})\))')
    for match in re.finditer(pattern, input):
        if match.group(1):  # do 
            process_flag = True
        if match.group(2):  # do 
            process_flag = False
        if match.group(3):
            a, b = int(match.group(4)), int(match.group(5))
            if process_flag:
                #print(f"Multiplying {a} and {b} gives {a * b}")
                total += a * b
            #else:
                #print(f"Skipping {a} and {b}")

    return total

def add_mul(input):
    # iterate through every pattern in input that mataches mul(\d,\d)
    pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    matches = pattern.findall(input)
    total = 0
    for match in matches:
        a, b = map(int, match)
        #print(f"Multiplying {a} and {b} gives {a * b}")
        total += a * b
    return total



def read_input():
    input = ''
    for line in sys.stdin:
        input += line.strip()
    return input

# pyttest day3.py  -- to run unit tests
def test_sample():
    assert 0 == add_mul('mul(4*, mul(6,9!, ?(12,34)')
    assert 0 == add_mul('mul ( 2 , 4 )') == 0
    assert 161 == add_mul('xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))')


def test_sample_2():
    assert 48 == add_mul_part2("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")


if __name__ == '__main__':
    input = read_input()
    print(f'Part1 = {add_mul(input)}')
    print(f'Part2 = {add_mul_part2(input)}')
