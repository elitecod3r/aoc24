# See https://adventofcode.com/2024/day/1 
# Given two lists, find the pairwise difference between the two list after sorting them. 

from collections import Counter

def find_distance(l1, l2):
    l1.sort()
    l2.sort()
    
    out = 0
    for a,b in zip(l1, l2):
        #print(abs(a-b))
        out += abs(a-b)
    return out

def find_similarity(l1, l2):
    c2 = Counter(l2)

    score = 0
    for a in l1:
        #print(a*c2[a])
        score += a*c2[a]
    return score  


# test case 
def test1():
    l1 = [3,4,2,1,3,3]
    l2 = [4,3,5,3,9,3]
    out = find_distance(l1, l2)
    print(f'distance = {out}')
    score = find_similarity(l1, l2)
    print(f'similary = {score}')
    

#test1()

# read until end of file
def read_input():
    l1 = []
    l2 = []
    while True:
        try:
            line = input()
            a, b = line.split()
            a, b = int(a), int(b)
            l1.append(a)
            l2.append(b)
        except EOFError:
            break
    return l1, l2

l1, l2 = read_input()
print(f'Distance = {find_distance(l1, l2)}')
print(f'Score = {find_similarity(l1, l2)}')