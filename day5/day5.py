
#Intcode program is a list of integers separated by commas
# Opcode: 1 = add from 2 positions and store in a third
#         2 = multiplies from 2 positions and store in a third
#         3 = 
#         4 =
#         99 = finished

# Parameter modes are stored in the same value as the instruction's opcode. 
# The opcode is a two-digit number based only on the ones and tens digit of the value, 
# that is, the opcode is the rightmost two digits of the first value in an instruction. 
# Parameter modes are single digits, one per parameter, read right-to-left from the opcode: 
# the first parameter's mode is in the hundreds digit, 
# the second parameter's mode is in the thousands digit, 
# the third parameter's mode is in the ten-thousands digit, and so on. 
# Any missing modes are 0.

#Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
#Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
#Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.

import csv

def get_paramode(n):
    inst     = str(n)
    opcode   = int(inst[-2:])
    inst = "000" + inst
    paramode = inst[::-1][2:]
    paramode = [int(x) for x in str(inst[::-1][2:])] 
    return paramode, opcode

def run(m, info_i):
    memory = m.copy()
    ip = 0 #instruction pointer
    info_out = []
    while ip <= len(memory):
        paramode, opcode = get_paramode(memory[ip]) #parameter mode - 0 for position, 1 for immediate
        print('Pointer: ', ip)
        print('Paramode: ', paramode)
        print('Instruction:', inst)
        if opcode == 1:
            print(paramode)
            input1 = memory[ip+1] if paramode[0] == 1 else memory[memory[ip+1]] 
            input2 = memory[ip+2] if paramode[1] == 1 else memory[memory[ip+2]]
            memory[memory[ip+3]] = input1+input2
            ip = ip + 4
        if opcode == 2:
            input1 = memory[ip+1] if paramode[0] == 1 else memory[memory[ip+1]] 
            input2 = memory[ip+2] if paramode[1] == 1 else memory[memory[ip+2]]
            memory[memory[ip+3]] = input1*input2
            ip = ip + 4
        if opcode == 3:
            memory[memory[ip+1]] = info_i
            ip = ip + 2
        if opcode == 4:
            a = memory[ip+1] if paramode[0] == 1 else memory[memory[ip+1]]
            info_out.append(a)
            ip = ip + 2
        if opcode == 5:
            input1 = memory[ip+1] if paramode[0] == 1 else memory[memory[ip+1]] 
            input2 = memory[ip+2] if paramode[1] == 1 else memory[memory[ip+2]] 
            ip = input2 if input1 != 0 else ip+3
        if opcode == 6:
            input1 = memory[ip+1] if paramode[0] == 1 else memory[memory[ip+1]] 
            input2 = memory[ip+2] if paramode[1] == 1 else memory[memory[ip+2]] 
            ip = input2 if input1 == 0 else ip+3
        if opcode == 7:
            input1 = memory[ip+1] if paramode[0] == 1 else memory[memory[ip+1]] 
            input2 = memory[ip+2] if paramode[1] == 1 else memory[memory[ip+2]] 
            memory[memory[ip+3]] = 1 if input1 < input2 else 0
            ip = ip + 4
        if opcode == 8:
            input1 = memory[ip+1] if paramode[0] == 1 else memory[memory[ip+1]] 
            input2 = memory[ip+2] if paramode[1] == 1 else memory[memory[ip+2]] 
            memory[memory[ip+3]] = 1 if input1 == input2 else 0
            ip = ip + 4
        if opcode == 99:
            break
    return memory, info_out


# Test: get_paramode
paramode, inst = get_paramode(3)
print(paramode)
print(inst)

# Test: output 5
print(run([3,0,4,0,99], 5))

# Test: 1002,4,3,4,99
print(run([1002,4,3,4,33], 0))

# Test: 1101,100,-1,4,99
print(run([1101,100,-1,4,0], 0))

# Mission 1
with open("input.txt") as file:
    line = file.readline()
    memory = [int(token) for token in line.split(",")]
ans, output = run(memory, 1)
print(output)

# Test: Output 1 if input is 8; output 0 otherwise in position mode
program = [3,9,8,9,10,9,4,9,99,-1,8]
print(run(program,9))

# Test: Output 1 if input is less than 8; output 0 otherwise in position mode
program = [3,9,7,9,10,9,4,9,99,-1,8]
print(run(program,7))

# Test: Output 1 if input is 8; output 0 otherwise in immediate mode
program = [3,3,1108,-1,8,3,4,3,99]
print(run(program,8))

# Test: Output 1 if input is less than 8; output 0 otherwise in immediate mode
program = [3,3,1107,-1,8,3,4,3,99]
print(run(program,7))

# Test Output 0 if the input was zero; otherwise 1 in position mode
program = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
print(run(program,0))

# Test Output 0 if the input was zero; otherwise 1 in immediate mode
program = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
print(run(program,2))

# Test larger example: output 999 if input is below 8, 
# output 1000 if input is 8, 
# output 1001 if input is greater than 8
program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
print(run(program,8))

ans, output = run(memory, 5)
print(output)