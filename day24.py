import re

def read_file(filename):
    var_value_dict = {}   # variable_name -> value 
    var_mapping_dict = {} # variable_name -> [index_of_operation]
    operator_list = []    # [ (op, left_var, left_val, right_var, right_val, output)]
    
    with open(filename) as f:
        for line in f:
            line =line.strip()
            if '->' in line:
                # Example pattern : "ntg XOR fgs -> mjb"
                match = re.search(r'(\S+)\s(\S+)\s(\S+)\s+->\s+(\S+)', line)
                assert match, f'Unexpected line input. Expected operation in {line}'
                left_var, op, right_var, output = match.group(1), match.group(2), match.group(3), match.group(4)
                idx = len(operator_list)    
                operator_list.append((op, left_var, None, right_var, None, output)) 
                if left_var not in var_mapping_dict:
                    var_mapping_dict[left_var] = []
                var_mapping_dict[left_var].append(idx)
                if right_var not in var_mapping_dict:
                    var_mapping_dict[right_var] = []
                var_mapping_dict[right_var].append(idx)
            elif ':' in line:
                # Example pattern: y30: 1
                match = re.search(r'(\S+)\:\s+(\S+)', line)
                assert match, f'Unexpected line input. Expected variable assignment in {line}'
                var_name, value = match.group(1), bool(int(match.group(2)))
                var_value_dict[var_name] = value
            # Skip non matching patterns
    return var_value_dict, var_mapping_dict, operator_list

def test_read_file():
    var_value_dict, var_mapping_dict, operator_list = read_file('day24_sample.txt')
    assert len(var_value_dict) == 10
    assert var_value_dict['x00'] == True
    assert var_value_dict['x04'] == False
    assert var_value_dict['y04'] == True

    assert len(operator_list) == 36
    assert operator_list[0] == ('XOR', 'ntg', None, 'fgs', None, 'mjb')
    assert operator_list[35] == ('OR', 'tnw', None, 'pbm', None, 'gnj')


def propagate_value(new_dict, var_mapping_dict, operator_list, idx, var, value):
    op, left_var, left_val, right_var, right_val, output_var = operator_list[idx]
    assert var in (left_var, right_var), f'Variable {var} not found in operation {op} {left_var} {right_var} -> {output_var}'
    
    if left_var == var:
        assert left_val == None, f'Variable {var} already has a value {left_val}'
        left_val = value
        operator_list[idx] = (op, left_var, left_val, right_var, right_val, output_var)
    if right_var == var:
        assert right_val == None, f'Variable {var} already has a value {right_val}'
        right_val = value
        operator_list[idx] = (op, left_var, left_val, right_var, right_val, output_var)

    if left_val != None and right_val != None:
        if op == 'AND':
            output_val = left_val and right_val
        elif op == 'OR':
            output_val = left_val or right_val
        elif op == 'XOR':
            output_val = left_val ^ right_val
        else:
            assert False, f'Unexpected operator {op}'

        assert output_var not in new_dict, f'Variable {output_var} already has a value {new_dict[output_var]}'
        new_dict[output_var] = output_val 
        if output_var not in var_mapping_dict:
            return
        for op_index in var_mapping_dict[output_var]:
            propagate_value(new_dict, var_mapping_dict, operator_list, op_index, output_var, output_val)

def solve_all_values(var_value_dict, var_mapping_dict, operator_list):
    new_dict = {}

    for var, value in var_value_dict.items():
        assert value != None, f'Variable {var} has no value'
        assert var in var_mapping_dict, f'Variable {var} has no mapping'
        for op_index in var_mapping_dict[var]:
            propagate_value(new_dict, var_mapping_dict, operator_list, op_index, var, value)
    return new_dict

def count_true_zvars(var_value_dict):
    zval = 0
    for var, value in sorted(var_value_dict.items()):
        if var.startswith('z'):
            match = re.search(r'z(\d+)', var)
            bit_pos = int(match.group(1))
            bit_val = 2**bit_pos
            if value:
                zval += 2**bit_pos
            #print(var, value, bit_pos, bit_val)
    return zval

# an attempt to draw the graph. Not very useful even for the simpler sample dataset.
def draw_graph():
    import networkx as nx
    import matplotlib.pyplot as plt

    var_value_dict, var_mapping_dict, operator_list = read_file('day24_sample.txt')
    G = nx.DiGraph()
    for op, left_var, left_val, right_var, right_val, output_var in operator_list:
        G.add_edge(left_var, output_var)
        G.add_edge(right_var, output_var)
    nx.draw(G, with_labels=True)
    plt.show()

def replace_vars(op_list, var_change_mapping):
    new_op_list = []
    for op, left_var, right_var, output_var in op_list:
        if left_var in var_change_mapping:
            left_var = var_change_mapping[left_var]
        if right_var in var_change_mapping:
            right_var = var_change_mapping[right_var]
        if left_var > right_var:
            left_var, right_var = right_var, left_var
        if output_var in var_change_mapping:
            output_var = var_change_mapping[output_var]
        new_op_list.append((op, left_var, right_var, output_var))
    return new_op_list

def print_output_order(op_list):
    output_var_mapper = {}
    max_z = 0
    for idx, (op, left_var, right_var, output_var) in enumerate(op_list):
        output_var_mapper[output_var] = idx
        if output_var.startswith('z'):
            z_val = int(output_var[1:])
            max_z = max(max_z, z_val)
    
    for i in range(max_z+1):
        for letter in ['a', 'b', 'z', 'd', 'c']:
            output_var = f'{letter}{i:02}'
            if output_var in output_var_mapper:
                idx = output_var_mapper[output_var]
                op, left_var, right_var, output_var = op_list[idx]
                print(f'{left_var} {op:.3s} {right_var} -> {output_var}')

    print(op_list)

def clean_operators(filename):
    var_value_dict, var_mapping_dict, operator_list = read_file(filename)
    # A typical operation set will have the following flows
    # 
    # x03 AND y03 -> a01     # change output var to a01
    # x03 XOR y03 -> b01     # change output var to b01
    # b01 XOR c00 -> z01     # don't change z var
    # b01 AND c00 -> d01     # change output var to d01
    # a01 OR d01 -> c01      # change carry var to c01. This is carry for next round
    #
    new_operator_list = []
    var_change_mapping = {}   
    for op, left_var, left_val, right_var, right_val, output_var in operator_list:
        if left_var > right_var:
            left_var, right_var = right_var, left_var
        new_operator_list.append((op, left_var, right_var, output_var))
        
        #'''
    for op, left_var, right_var, output_var in new_operator_list:
        if output_var.startswith('z'):
            continue
        if left_var == 'x00':
            new_output = 'c00'
            var_change_mapping[output_var] = new_output
            continue
            
        if left_var.startswith('x') and right_var.startswith('y'):
            var_suffix = left_var[1:]
            assert var_suffix == right_var[1:], f'Variable suffix mismatch {left_var} {right_var}'
            if op == 'AND':
                new_output = f'a{var_suffix}'
                var_change_mapping[output_var] = new_output
            elif op == 'XOR':
                new_output = f'b{var_suffix}'
                var_change_mapping[output_var] = new_output
    new_operator_list = replace_vars(new_operator_list, var_change_mapping)

    for op, left_var, right_var, output_var in new_operator_list:
        if output_var.startswith('z') or left_var.startswith('x'):
            continue
        if left_var.startswith('a') or left_var.startswith('b'):
            var_suffix = left_var[1:]
        else:
            print('Unexpected left var', left_var, right_var, output_var)

        if op == 'AND':
            new_output = f'd{var_suffix[1:]}'
            var_change_mapping[output_var] = new_output
        elif op == 'OR':
            new_output = f'c{var_suffix[1:]}'
            var_change_mapping[output_var] = new_output
    new_operator_list = replace_vars(new_operator_list, var_change_mapping)
    #'''
    print_output_order(new_operator_list)


if __name__ == '__main__':    
    print('Part 1')
    new_dict = solve_all_values(*read_file('day24_sample.txt'))
    print('Sample = ',count_true_zvars(new_dict))
    new_dict = solve_all_values(*read_file('day24_input.txt'))
    print('Input  = ',count_true_zvars(new_dict))
    
    print('Part 2')
    #draw_graph(operator_list)
    #print_neatly('day24_input.txt')
    clean_operators('day24_input.txt')
