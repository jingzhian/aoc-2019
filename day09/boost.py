## Sensor Boost
# Needs to support in relative mode i.e. parameter in mode 2
# 

class Amplifier:

    def __init__(self, program, inputs=[]):
        self.memory = program.copy()
        self.inputs = inputs
        self.outputs = []
        self.relativebase = 0
        self.ip = 0

    def get_paramode(self, n):
        inst     = str(n)
        opcode   = int(inst[-2:])
        inst     = "000" + inst
        paramode = inst[::-1][2:]
        paramode = [int(x) for x in str(inst[::-1][2:])] 
        return paramode, opcode

    def get_input(self, ip, paramode):
        if paramode == 1: #immediate mode
            index = ip
        elif paramode == 2: #relative mode
            index = self.memory[ip] + self.relativebase
        else: #position mode
            index = self.memory[ip]
        index = self.grow_memory(index)
        value = self.memory[index]
        return value

    def get_writeindex(self, ip, paramode):
        if paramode == 2:
            index = self.memory[ip] + self.relativebase
            #print(self.relativebase)
            #print(len(self.memory))
        else:
            index = self.memory[ip]
        index = self.grow_memory(index)
        return index

    def grow_memory(self, index):
        if index >= len(self.memory):
            self.memory = self.memory + ([0]*(index-len(self.memory)+1))
        return index

    def run(self):
        ip = self.ip #instruction pointer
        #counter = 1
        while ip <= len(self.memory): #and counter <10:
            paramode, opcode = self.get_paramode(self.memory[ip]) #parameter mode - 0 for position, 1 for immediate
            #print(ip, paramode, opcode, self.relativebase)
            #counter +=1
            if opcode == 1:
                input1 = self.get_input(ip+1, paramode[0])
                input2 = self.get_input(ip+2, paramode[1])
                output_index = self.get_writeindex(ip+3, paramode[2])
                self.memory[output_index] = input1 + input2
                ip = ip + 4
            if opcode == 2:
                input1 = self.get_input(ip+1, paramode[0])
                input2 = self.get_input(ip+2, paramode[1])
                output_index = self.get_writeindex(ip+3, paramode[2])
                self.memory[output_index] = input1*input2
                ip = ip + 4
            if opcode == 3:
                #if len(self.inputs) == 0:
                #    self.ip = ip
                #    status = "wait"
                #else:
                output_index = self.get_writeindex(ip+1, paramode[0])
                self.memory[output_index] = self.inputs.pop(0)
                ip = ip + 2
            if opcode == 4:
                a = self.get_input(ip+1, paramode[0])
                self.outputs.append(a)
                status = "output"
                ip = ip + 2
            if opcode == 5:
                input1 = self.get_input(ip+1, paramode[0])
                input2 = self.get_input(ip+2, paramode[1])
                ip = input2 if input1 != 0 else ip+3
            if opcode == 6:
                input1 = self.get_input(ip+1, paramode[0])
                input2 = self.get_input(ip+2, paramode[1]) 
                ip = input2 if input1 == 0 else ip+3
            if opcode == 7:
                input1 = self.get_input(ip+1, paramode[0])
                input2 = self.get_input(ip+2, paramode[1])
                output_index = self.get_writeindex(ip+3, paramode[2])
                self.memory[output_index] = 1 if input1 < input2 else 0
                ip = ip + 4
            if opcode == 8:
                input1 = self.get_input(ip+1, paramode[0])
                input2 = self.get_input(ip+2, paramode[1])
                output_index = self.get_writeindex(ip+3, paramode[2])
                self.memory[output_index] = 1 if input1 == input2 else 0
                ip = ip + 4
            if opcode == 9:
                self.relativebase = self.relativebase + self.get_input(ip+1, paramode[0])
                ip = ip + 2
            if opcode == 99:
                self.ip = ip
                status = "halt"
                break
            #print(memory)
        return status


mission1 = True
mission2 = False

test = 4

if mission1: 
    # Get input
    if test == 1: # produce a copy of itself as output
        program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    elif test == 2: # output a 16-digit number
        program = [1102,34915192,34915192,7,4,7,99,0]
    elif test == 3: # output the large number in the middle
        program = [104,1125899906842624,99]
    else:
        with open("input.txt") as file:
            line = file.readline()
            program = [int(token) for token in line.split(",")]

    amp = Amplifier(program, inputs=[2])
    status = amp.run()
    print(amp.outputs)
