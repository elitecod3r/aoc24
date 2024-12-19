
def simulate_program(program, A, B, C):
    def get_combo_value(operand):
        if operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        elif 0 <= operand <= 3:
            return operand
        else:
            raise ValueError("Invalid combo operand")

    ip = 0
    output = []
    while ip+1 < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:  # adv
            A = A // (2 ** get_combo_value(operand))
        elif opcode == 1:  # bxl
            B = B ^ operand
        elif opcode == 2:  # bst
            B = get_combo_value(operand) % 8
        elif opcode == 3:  # jnz
            if A != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            B = B ^ C
        elif opcode == 5:  # out
            output.append(get_combo_value(operand) % 8)
        elif opcode == 6:  # bdv
            B = A // (2 ** get_combo_value(operand))
        elif opcode == 7:  # cdv
            C = A // (2 ** get_combo_value(operand))
        else:
            raise ValueError("Invalid opcode")

        ip += 2

    return output

def test_simulate_program():
    program = [0, 1, 5, 4, 3, 0]
    assert simulate_program(program, A=729, B=0, C=0) == [4,6,3,5,6,3,5,2,1,0]


# How to find value of A to print a given output? 
# Let's solve it only for the given program. I am not sure if there is a 
# general solution for this.
# Given program 2,4,  1,5,  7,5,  0,3,  4,0,  1,6,  5,5,  3,0
# B = 0
# C = 0
#  B = A % 8            # 2,4
#  B = B ^ 5            # 1,5
#  C = A // 2**B        # 7,5
#  A = A // 2**3        # 0,3
#  B = B ^ C            # 4,0
#  B = B ^ 6            # 1,6
#  output B % 8         # 5,5
# if A != 0: jump to 0  # 3,0 
#

# while A != 0:
#    Use A to produce an output
#    Remove last 3 bits of A 
#
# The last output printed will depend only on the first 3 MSB (bits)  of A. 
#   the next output will depend on the first 6 MSB of A and so on.
#  
def find_reg_A(program, B, C, A=0, num_octets=0):
    output = simulate_program(program, A, B, C)
    if output == program:
        return A
    
    if output == program[-num_octets:] or num_octets == 0:
        for n in range(8):
            match = find_reg_A(program, B, C, 8 * A + n, num_octets + 1)
            if match:
                return match
    return None


if __name__ == '__main__':
    program = [2,4,1,5,7,5,0,3,4,0,1,6,5,5,3,0]
    result = simulate_program(program, A=46187030, B=0, C=0)
    print("Part1:", ','.join(map(str, result)))

    regA = find_reg_A(program, B=0, C=0)
    print("Part2:", regA)   
