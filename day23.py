import re

def read_file(filename):
    pair_list = []
    with open(filename) as f:
        for line in f:
            line =line.strip()
            if line:
                match = re.search(r'(..)-(..)', line)
                assert match, 'Unexpected line input'
                pair_list.append((match.group(1), match.group(2)))
    return pair_list
    
def test_read_file():
    pair_list = read_file('day23_sample.txt')
    assert len(pair_list) == 32
    assert pair_list[0] == ('kh', 'tc')
    assert pair_list[31] == ('td', 'yn')

def create_sets(pair_list):
    # return a list of fully-connected triplets that start with letter t
    
    # for a given node, node_dict contains set of all nodes connected directly 
    #  to that node.
    node_dict = {}

    for n1, n2 in pair_list:
        if n1 not in node_dict:
            node_dict[n1] = set()
        node_dict[n1].add(n2)
        if n2 not in node_dict:
            node_dict[n2] = set()
        node_dict[n2].add(n1)
    
    triad_set = set()
    for node, connected_nodes in node_dict.items():
        if not node.startswith('t'):
            continue
        while connected_nodes:
            next_node = connected_nodes.pop()
            common_nodes = connected_nodes.intersection(node_dict[next_node])
            for common_node in common_nodes:
                sorted_nodes = sorted([node, next_node, common_node])
                triad_set.add(",".join(sorted_nodes))
    return triad_set


if __name__ == '__main__':    
    print('Part 1')
    pair_list = read_file('day23_sample.txt')
    print('Sample : ', len(create_sets(pair_list)))
    pair_list = read_file('day23_input.txt')
    print('Input  : ', len(create_sets(pair_list)))