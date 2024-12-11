

sample_list = [125, 17]
input_list = [6571, 0, 5851763, 526746, 23, 69822, 9, 989]

def next_step(in_list):
    out_list = []
    for num in in_list:
        numstr = str(num)
        if num == 0:
            out_list.append(1)
        elif len(numstr) % 2 == 0:
            midpoint = len(numstr) // 2
            a, b = numstr[:midpoint], numstr[midpoint:]
            out_list.append(int(a))
            out_list.append(int(b))
        else:
            out_list.append(num * 2024)

    return out_list

def count_stones(in_list, blinks):
    for blink in range(blinks):
        in_list = next_step(in_list)
        #print(blink, len(in_list))
    return len(in_list)

blink_mapper = {}

# return count of numbers generated after blinks blink starting from num
def num_blink(num, blinks):
    if blinks == 0:
        return 1
    if blink_mapper.get((num, blinks)):
        return blink_mapper[(num, blinks)]

    in_list = next_step([num])  
    count = 0
    for n in in_list:
        count += num_blink(n, blinks-1)
    blink_mapper[(num, blinks)] = count
    return count


def count_stones_v2(in_list, blinks):
    count = 0
        
    for num in in_list:
        count += num_blink(num, blinks)
    return count 


def test_next_step():
    a = next_step(sample_list)
    assert a == [253000, 1, 7]
    b = next_step(a)
    assert b == [253, 0, 2024, 14168]
    c = next_step(b)
    assert c == [512072, 1, 20, 24, 28676032]

def test_count_stones():
    assert count_stones(sample_list, 1) == 3
    assert count_stones(sample_list, 6) == 22
    assert count_stones(sample_list, 25) == 55312

def test_count_stones_v2():
    assert count_stones_v2(sample_list, 1) == 3
    assert count_stones_v2(sample_list, 6) == 22
    assert count_stones_v2(sample_list, 25) == 55312


if __name__ == '__main__':
    test_next_step()
    test_count_stones()
    test_count_stones_v2()
    print("Part1 = ", count_stones(input_list, 25))
    print("Part2 = ", count_stones_v2(input_list, 75))

