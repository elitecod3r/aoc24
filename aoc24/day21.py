

import itertools
import pprint 
pp = pprint.PrettyPrinter(indent=4)


def find_key(keypad, key):
    for row_index, row in enumerate(keypad):
        for col_index, cell in enumerate(row):
            if cell == key:
                return row_index, col_index
    return None, None

direction_keypad = [ 
    [' ', '^', 'A'],
    ['<', 'v', '>']
]
numeric_keypad = [ 
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [' ', '0', 'A']
]

direction_key_dict ={}
for key in [' ', '^', 'v', '<', '>', 'A']:
    row, col = find_key(direction_keypad, key)
    direction_key_dict[key] = (row, col)

numeric_keys = [' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A']
for key in [' ', '^', 'v', '<', '>', 'A']:
    pass

# This part is for testing and kicks. 
# We will output the robots movement, given a set of input keys
def handle_keypad(keypad, input_keys, row, col):    
    output_keys = []
    for key in input_keys:
        if key == '^':
            row -= 1
        elif key == 'v':
            row += 1
        elif key == '<':
            col -= 1
        elif key == '>':
            col += 1

        if row < 0 or row >= len(keypad) or \
           col < 0 or col >= len(keypad[0]) or\
           (keypad[row][col] == ' '):
            assert False, f'Invalid row, col : {row}, {col}'
        if key == 'A':
            output_keys.append(keypad[row][col])
    
    return ''.join(output_keys)


def handle_direction(input_keys):
    return handle_keypad(direction_keypad, input_keys, 0, 2)

def handle_numeric(input_keys):
    return handle_keypad(numeric_keypad, input_keys, 3, 2)

def full_keypad_sequence(input_keys):
    return handle_numeric(handle_direction(handle_direction(input_keys)))

def test_keypads():
    s1 = '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'
    s2 = 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A'
    s3 = '<A^A>^^AvvvA'
    s4 = '029A'
    assert handle_direction(s1) == s2
    assert handle_direction(s2) == s3
    assert handle_numeric(s3) == s4

    assert full_keypad_sequence(s1) == '029A'
    assert '980A' == full_keypad_sequence('<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A') 



def remove_bad_paths(keypad, path_list, start_row, start_col):
    new_path_set = set()

    for path in path_list:
        row, col = start_row, start_col
        good_path = True 
        for move in path:
            if move == '^':
                row -= 1
            elif move == 'v':
                row += 1
            elif move == '<':
                col -= 1
            elif move == '>':
                col += 1
            if keypad[row][col] == ' ':
                good_path = False
                break
        if good_path:
            new_path_set.add(path)

    return list(new_path_set)


def find_all_raw_paths(keypad):
    # We will find all directional movements needed to press dest key, when 
    #  the robot hand is at src key. 
    #  So a move from 7 to 9 would be ('>', '>', 'A'). We will find all possible 
    #  valid paths for all src, dest pairs and sore it as 
    #   (src, dest) -> [list of paths]  where each path is a tuple of moves.
    #

    raw_mapper = {}
    max_row = len(keypad)
    max_col = len(keypad[0])
    for row1 in range(max_row):
        for col1 in range(max_col):
            for row2 in range(max_row):
                for col2 in range(max_col):
                    if keypad[row1][col1] == ' ' or keypad[row2][col2] == ' ':
                        continue
                    
                    if row1 == row2 and col1 == col2:
                        raw_mapper[(keypad[row1][col1], keypad[row2][col2])] = [('A',)] 
                    move_list = []
                    row_moves = row2 - row1
                    if row_moves < 0:
                        move_list.extend(['^'] * abs(row_moves) ) 
                    else:
                        move_list.extend(['v'] * row_moves)
                    col_moves = col2 - col1
                    if col_moves < 0:
                        move_list.extend(['<'] * abs(col_moves))
                    else:   
                        move_list.extend(['>'] * col_moves)

                    #all_moves_list = list(itertools.permutations(move_list))
                    #  add 'A' to every sequence. 
                    all_moves_list = [tuple(list(x)+['A']) for x in itertools.permutations(move_list)]
                    all_moves_list = remove_bad_paths(keypad, all_moves_list, row1, col1)
                    raw_mapper[(keypad[row1][col1], keypad[row2][col2])] = all_moves_list
    return raw_mapper

def test_find_all_raw_paths():

    dir_mapper = find_all_raw_paths(direction_keypad)
    pp.pprint(dir_mapper)

    #dir_mapper = find_all_raw_paths(numeric_keypad)
    #pp.pprint(dir_mapper)


def find_shortest_mapping(keypad, prev_mapper):
    next_mapper = {}
    # Get paths for all (src,dest) pair in the keypad
    raw_paths = find_all_raw_paths(keypad)
    for src_dest, raw_path_list in raw_paths.items():
        src, dest = src_dest
        best_path = [' '] * 1000    # really long path 
        for raw_path in raw_path_list:
            mapped_path = []
            prev_key = 'A'
            for key in raw_path:
                mapped_path.extend(prev_mapper[(prev_key, key)])
                prev_key = key
            assert len(mapped_path) > 0
            if len(mapped_path) < len(best_path):
                best_path = mapped_path
        next_mapper[src_dest] = best_path
    return next_mapper


# We will use a dictionary to store shortest set of moves to 
#  go from a src to dest. 
#  (src, dest) -> [sequence of moves]
#  We will initilaize for the first level. 
move_mapper_1 = {}
for key in direction_key_dict.keys():
    for key2 in direction_key_dict.keys():
        move_mapper_1[(key, key2)] = [key2]
        
move_mapper_2 = find_shortest_mapping(direction_keypad, move_mapper_1)
move_mapper_3 = find_shortest_mapping(direction_keypad, move_mapper_2)
move_mapper_4 = find_shortest_mapping(numeric_keypad, move_mapper_3)

def get_move_string(key_str, move_mapper):
    curr_key = 'A'
    move_str = ''
    for key in key_str:
        move_str += "".join(move_mapper[(curr_key, key)])
    return move_str

if __name__ == '__main__':
    #test_keypads()
    #test_find_all_raw_paths()
    #pp.pprint(move_mapper_4)
    move_str = get_move_string('029A', move_mapper_4)
    print(move_str)
    print(handle_direction(move_str))
    print(handle_direction(handle_direction(move_str)))
    print(handle_numeric(handle_direction(handle_direction(move_str))))
    #print('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A')