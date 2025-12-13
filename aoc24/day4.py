from collections import Counter
from io import StringIO
import sys


def make_array(input):
    array = []
    for line in input.split('\n'):
        if line:
            list_line = list(line)
            array.append(list_line)
    return array


# read until end of file
def read_stdin():
    input = ''
    for line in sys.stdin:
        input += line
    return input

def get_sample():
    test_input = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
    return test_input

def test_make_array():
    test_input = get_sample()
    array = make_array(test_input)
    print(array)
    assert len(array) == 10
    assert len(array[0]) == 10
    assert array[0][0] == 'M'
    assert array[9][9] == 'X'


def find_word(array, word, row_index, col_index, row_delta, col_delta):
    for i in range(len(word)):
        if row_index < 0 or row_index >= len(array):
            return False
        if col_index < 0 or col_index >= len(array[0]):
            return False
        if array[row_index][col_index] != word[i]:
            return False
        row_index += row_delta
        col_index += col_delta
    return True

def test_find_word():
    array = make_array(get_sample())
    assert find_word(array, 'XMAS', 0, 4, 0, 1) == False
    assert find_word(array, 'XMAS', 0, 5, 0, 1) == True
    assert find_word(array, 'XMAS', 0, 4, 1, 1) == True
    assert find_word(array, 'XMAS', 0, 4, -1, 0) == False  # going out of bounds

def count_xmax(array, word):
    count = 0
    for row_index in range(len(array)):
        for col_index in range(len(array[0])):
            for row_delta in range(-1, 2):
                for col_delta in range(-1, 2):
                    if row_delta == 0 and col_delta == 0:
                        continue
                    if find_word(array, word, row_index, col_index, row_delta, col_delta):
                        count += 1
    return count

def test_count_xmax():
    array = make_array(get_sample())
    assert count_xmax(array, 'XMAS') == 18


def get_value(array, row, col):
    # return space if the row, col are outside the bounds
    if row < 0 or row >= len(array):
        return ' '
    if col < 0 or col >= len(array[0]):
        return ' '
    return array[row][col]

def count_x_max(array):
    count = 0
    for row_index in range(len(array)): 
        for col_index in range(len(array[0])):
            if array[row_index][col_index] != 'A':
                continue
            left_top = get_value(array, row_index - 1, col_index - 1)
            left_bot = get_value(array, row_index + 1, col_index - 1)
            right_top = get_value(array, row_index - 1, col_index + 1)
            right_bot = get_value(array, row_index + 1, col_index + 1)
            if (left_top == 'M' and right_bot == 'S') or \
               (left_top == 'S' and right_bot == 'M'):
                if (right_top == 'M' and left_bot == 'S') or \
                   (right_top == 'S' and left_bot == 'M'):
                    count += 1
    return count

def test_count_x_max():
    array = make_array(get_sample())
    assert count_x_max(array) == 9


if __name__ == '__main__':
    array = make_array(read_stdin())
    print(f"xmax count  = {count_xmax(array, 'XMAS')}")
    print(f"x-max count = {count_x_max(array)}")