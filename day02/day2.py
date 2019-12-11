
#Intcode program is a list of integers separated by commas
# Opcode: 1 = add from 2 positions and store in a third
#         2 = multiplies from 2 positions and store in a third
#         99 = finished

import csv

def run(m):
    memory = m.copy()
    ip = 0 #instruction pointer
    while ip <= len(memory):
        x = memory[ip]
        if x == 1:
            memory[memory[ip+3]] = memory[memory[ip+1]] + memory[memory[ip+2]]
            ip = ip + 4
        elif x == 2:
            memory[memory[ip+3]] = memory[memory[ip+1]] * memory[memory[ip+2]]
            ip = ip + 4
        elif x == 99:
            break
    return memory

def searchnv(m):
    for x in range(0, 100):
        for y in range(0, 100):
            memory[1] = x  #noun
            memory[2] = y  #verb
            ans = run(memory)[0]
            if ans == 19690720:
                noun = x
                verb = y
                return noun,verb

# Test: should print [3500,9,10,70,2,3,11,0,99,30,40,50]
print(run([1,9,10,3,2,3,11,0,99,30,40,50]))

with open("input.txt") as file:
    # reader = csv.reader(file)
    # memory = list(reader)
    line = file.readline()
    memory = [int(token) for token in line.split(",")]

# Mission 1
memory[1] = 12  #noun
memory[2] = 2  #verb
ans = run(memory)[0]
print(ans)

# Mission 2
noun, verb = searchnv(memory)
sol = 100*noun + verb
print(sol)


