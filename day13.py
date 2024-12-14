import re
from math import gcd

def read_file(filename):
    problem_set = []
    with open(filename, 'r') as f:
        while True:
            line1 = f.readline().strip()
            line2 = f.readline().strip()
            line3 = f.readline().strip()
            # Extract x and y from line with pattern "Button A: X+31, Y+83"
            match1 = re.search(r'Button A: X\+(\d+), Y\+(\d+)', line1)
            match2 = re.search(r'Button B: X\+(\d+), Y\+(\d+)', line2)
            match3 = re.search(r'Prize: X\=(\d+), Y\=(\d+)', line3)

            assert match1 and match2 and match3, 'Unexpected line input'
            move_a = (int(match1.group(1)), int(match1.group(2)))
            move_b = (int(match2.group(1)), int(match2.group(2)))
            target = (int(match3.group(1)), int(match3.group(2)))
            problem_set.append((move_a, move_b, target))

            empty_line = f.readline()
            if not empty_line:
                break
    return problem_set

def test_read_file():
    problem_set = read_file('day13_sample.txt')
    assert len(problem_set) == 4
    assert problem_set[0] == ((94, 34), (22, 67), (8400, 5400))
    assert problem_set[3] == ((69, 23), (27, 71), (18641, 10279))


def find_all_solutions(a, b, c):
    # Find all positive solutions for diophantine equation ax + by = c
    # returns a list of tuples (x, y)
    solutions = []
    for x in range(0, c//a + 1):
        y = (c - a*x) // b
        if a*x + b*y == c:
            solutions.append((x, y))
    return solutions

def solve_a_problem(cost_a, cost_b, move_a, move_b, target):
    # Returns the lowest cost to reach the target
    #  return 0 if the target is not reachable. 
    a_x, a_y = move_a
    b_x, b_y = move_b
    c_x, c_y = target
    x_solutions = find_all_solutions(a_x, b_x, c_x)
    y_solutions = find_all_solutions(a_y, b_y, c_y)

    min_cost = 999999999     # Assuming cost will always be less than 9999   
    for x, y in x_solutions:
        if (x,y) not in y_solutions:
            continue
        cost = cost_a * x + cost_b * y
        min_cost = min(min_cost, cost)

    if min_cost == 999999999:
        return 0
    return min_cost 


def test_solve_a_problem():
    problem_set = read_file('day13_sample.txt')
    cost_a, cost_b = 3, 1

    assert solve_a_problem(cost_a, cost_b, *problem_set[0]) == 280
    assert solve_a_problem(cost_a, cost_b, *problem_set[1]) == 0 
    assert solve_a_problem(cost_a, cost_b, *problem_set[2]) == 200 
    assert solve_a_problem(cost_a, cost_b, *problem_set[3]) == 0

def score_all_problems(filename):
    problem_set = read_file(filename)
    cost = 0
    for move_a, move_b, target in problem_set:
        cost += solve_a_problem(3, 1, move_a, move_b, target)
    return cost


def find_all_solutions(a, b, c):
    print("\nProcessing ", a, b, c)
    solutions = []
    if c % gcd(a, b) != 0:
        # No solutions exist if gcd(a, b) does not divide c
        return solutions

    # Reduce coefficients
    g = gcd(a, b)
    a, b, c = a // g, b // g, c // g
    print(f'a={a} b={b} c={c} gcd={g}') 

    # Find one particular solution using the Extended Euclidean Algorithm
    def extended_gcd(x, y):
        if y == 0:
            return 1, 0, x
        x1, y1, g = extended_gcd(y, x % y)
        return y1, x1 - (x // y) * y1, g

    # Baslien solution
    x0, y0, k = extended_gcd(a, b)
    x0, y0 = x0 * c, y0 * c
    #solutions.append((x0, y0))

    k_min = - (x0 // b)
    k_max = y0 // a
    print(f"x0={x0} y0={y0} k_min={k_min} k_max={k_max}")

    # Generate all positive integer solutions
    for k in range(k_min, k_max + 1):
        x = x0 + k * b
        y = y0 - k * a

        print("  Solution  = ", x, y) 
        if x >= 0 and y >= 0:
            solutions.append((x, y))

    return solutions

def test_find_all_solutions():
    solutions = find_all_solutions(3, 5, 11)
    #assert len(solutions) == 10

    solutions = find_all_solutions(4, 8, 32)

    solutions = find_all_solutions(86, 37, 6450)
    #assert len(solutions) == 10
    a, b, c = 86, 37, 6450  # solution is 38, 86

    
def score_all_problems2(filename):
    problem_set = read_file(filename)
    cost = 0
    for move_a, move_b, target in problem_set:
        x, y = target
        x = int('10000000000000' + str(x))
        y = int('10000000000000' + str(y))
        target = (x, y)
        cost += solve_a_problem(3, 1, move_a, move_b, target)
    return cost

if __name__ == '__main__':
    score_all_problems2('day13_sample.txt')
    #test_find_all_solutions()
    exit()

    print('Part 1')
    print('Sample :', score_all_problems('day13_sample.txt'))
    print('Input  :', score_all_problems('day13_input.txt'))
    print('Sample :', score_all_problems2('day13_sample.txt'))
    print('Input  :', score_all_problems2('day13_input.txt'))