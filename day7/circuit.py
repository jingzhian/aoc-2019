## Amplification Circuit
# Configure a series of amplifiers installed on the ship
# 5 amplifiers connected in series, each on receives an input signal and produces an output signal
#     O-------O  O-------O  O-------O  O-------O  O-------O
# 0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
#     O-------O  O-------O  O-------O  O-------O  O-------O
# Input: Amplifier control software, that runs on Intcode computer
# Each amplifier will need to run a copy of the program

# Start: Program use an input instruction to ask the amplifier for its current phase setting
# Integer from 0 to 4; each used exactly once.

# Then: program will call another input instruction to get the amplifier's input signal, compute the correct output signal, and supply it back to the amplifier with an output instruction

from itertools import permutations 

# Define Intcode Program

class Amplifier:

    def __init__(self, program, inputs=[]):
        self.memory = program.copy()
        self.inputs = inputs
        self.outputs = []
        self.ip = 0
        
    def get_paramode(self, n):
        inst     = str(n)
        opcode   = int(inst[-2:])
        inst = "000" + inst
        paramode = inst[::-1][2:]
        paramode = [int(x) for x in str(inst[::-1][2:])] 
        return paramode, opcode

    def run(self):
        ip = self.ip #instruction pointer
        while ip <= len(self.memory):
            paramode, opcode = self.get_paramode(self.memory[ip]) #parameter mode - 0 for position, 1 for immediate
            if opcode == 1:
                input1 = self.memory[ip+1] if paramode[0] == 1 else self.memory[self.memory[ip+1]] 
                input2 = self.memory[ip+2] if paramode[1] == 1 else self.memory[self.memory[ip+2]]
                self.memory[self.memory[ip+3]] = input1 + input2
                ip = ip + 4
            if opcode == 2:
                input1 = self.memory[ip+1] if paramode[0] == 1 else self.memory[self.memory[ip+1]] 
                input2 = self.memory[ip+2] if paramode[1] == 1 else self.memory[self.memory[ip+2]]
                self.memory[self.memory[ip+3]] = input1*input2
                ip = ip + 4
            if opcode == 3:
                if len(self.inputs) == 0:
                    self.ip = ip
                    status = "wait"
                    break
                else:
                    self.memory[self.memory[ip+1]] = self.inputs.pop(0)
                    ip = ip + 2
            if opcode == 4:
                a = self.memory[ip+1] if paramode[0] == 1 else self.memory[self.memory[ip+1]]
                self.outputs.append(a)
                status = "output"
                ip = ip + 2
                self.ip = ip
                break
            if opcode == 5:
                input1 = self.memory[ip+1] if paramode[0] == 1 else self.memory[self.memory[ip+1]] 
                input2 = self.memory[ip+2] if paramode[1] == 1 else self.memory[self.memory[ip+2]] 
                ip = input2 if input1 != 0 else ip+3
            if opcode == 6:
                input1 = self.memory[ip+1] if paramode[0] == 1 else self.memory[self.memory[ip+1]] 
                input2 = self.memory[ip+2] if paramode[1] == 1 else self.memory[self.memory[ip+2]] 
                ip = input2 if input1 == 0 else ip+3
            if opcode == 7:
                input1 = self.memory[ip+1] if paramode[0] == 1 else self.memory[self.memory[ip+1]] 
                input2 = self.memory[ip+2] if paramode[1] == 1 else self.memory[self.memory[ip+2]] 
                self.memory[self.memory[ip+3]] = 1 if input1 < input2 else 0
                ip = ip + 4
            if opcode == 8:
                input1 = self.memory[ip+1] if paramode[0] == 1 else self.memory[self.memory[ip+1]] 
                input2 = self.memory[ip+2] if paramode[1] == 1 else self.memory[self.memory[ip+2]] 
                self.memory[self.memory[ip+3]] = 1 if input1 == input2 else 0
                ip = ip + 4
            if opcode == 99:
                self.ip = ip
                status = "halt"
                break
            #print(memory)
        return status

# Mission 1: Find the largest output signal that can be sent to the thrusters, by trying every possible combinationof phase settings

# For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which would mean setting amplifier A to phase setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. Then, you could determine the output signal that gets sent from amplifier E to the thrusters with the following steps:
# Start the copy of the amplifier controller software that will run on amplifier A. At its first input instruction, provide it the amplifier's phase setting, 3. At its second input instruction, provide it the input signal, 0. After some calculations, it will use an output instruction to indicate the amplifier's output signal.
# Start the software for amplifier B. Provide it the phase setting (1) and then whatever output signal was produced from amplifier A. It will then produce a new output signal destined for amplifier C.
# Start the software for amplifier C, provide the phase setting (2) and the value from amplifier B, then collect its output signal.
# Run amplifier D's software, provide the phase setting (4) and input value, and collect its output signal.
# Run amplifier E's software, provide the phase setting (0) and input value, and collect its output signal.

mission1 = True
mission2 = False

test = 3

if mission1: 
    # Get input
    if test == 1: # max thruster 43210 from phase sequence 4,3,2,1,0
        program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    elif test == 2: # Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4)
        program = [3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0]
    elif test == 3: # Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2)
        program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    else:
        with open("input.txt") as file:
            line = file.readline()
            program = [int(token) for token in line.split(",")]
    #print(program)

    # Create different combinations of phase inputs
    phases = list(permutations([0, 1, 2, 3, 4]))
    #phases = ([0, 1, 2, 3, 4], [1, 2, 3, 4, 0])

    # Call one program
    thruster = []

    for phase in phases:
        #print(phase)
        amps = [Amplifier(program, inputs = [phase[i]]) for i in range(5)]
        amps[0].inputs.append(0)
        for i in range(5):
            status = amps[i].run()
            if i < 4:
                amps[i+1].inputs.append(amps[i].outputs[-1])
        thruster.append(amps[-1].outputs[-1])
        '''
        '''
    print('Maximum thurster inputs: ', max(thruster))


# Mission 2

# New Configuration
#      O-------O  O-------O  O-------O  O-------O  O-------O
#0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
#   |  O-------O  O-------O  O-------O  O-------O  O-------O |
#   |                                                        |
#   '--------------------------------------------------------+
#                                                            |
#                                                            v
#                                                     (to thrusters)

# amplifiers need totally different phase settings: integers from 5 to 9, again each used exactly once

if mission2:
 
    if test == 1: # Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5)
        program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    elif test == 2: # Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6)
        program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    else:
        with open("input.txt") as file:
            line = file.readline()
            program = [int(token) for token in line.split(",")]

    if test:
        phases = ([5, 6, 7, 8, 9], [9, 8, 7, 6, 5])
    else:
        phases = list(permutations([5, 6, 7, 8, 9]))

    thruster = []

    for phase in phases:

        # Create the amplifers
        amps = [Amplifier(program, inputs = [phase[i]]) for i in range(5)]
        amps[0].inputs.append(0) # Amp A gets input signal 0

        # Run the amplifers until all are halted
        halted = [0] * 5
        while sum(halted) < len(halted): # not all has halted
            for i, amp in enumerate(amps):
                while True:
                    status = amps[i].run()
                    if status == "halt":
                        halted[i] = 1
                        break
                    if status == "output":
                        output_amp = amps[(i+1) % 5]
                        output_amp.inputs.append(amps[i].outputs[-1])
                        break
                    if status == "wait":
                        break
        #Postcondition, all amps are halted, get thruster output
        thruster.append(amps[-1].outputs[-1])
    print('Maximum thurster inputs: ', max(thruster))