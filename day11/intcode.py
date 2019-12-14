class Computer:

    def __init__(self, program, inputs = []):
        self.memory = program.copy()
        self.inputs = inputs
        self.outputs = []
        self.relativebase = 0
        self.ip = 0
        self.status = 'ok'

    def get_paramode(self, n):
        inst     = str(n)
        opcode   = int(inst[-2:])
        inst     = "0000" + inst
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

    def grow_memory(self, index):
        if index >= len(self.memory):
            self.memory = self.memory + ([0]*(index-len(self.memory)+1))
        return index

    def get_writeindex(self, ip, paramode):
        if paramode == 2:
            index = self.memory[ip] + self.relativebase
            #print(self.relativebase)
            #print(len(self.memory))
        else:
            index = self.memory[ip]
        index = self.grow_memory(index)
        return index

    def step(self): # only execute 1 instruction
        ip = self.ip
        paramode, opcode = self.get_paramode(self.memory[ip]) #parameter mode - 0 for position, 1 for immediate
        #print(self.memory[ip], paramode, opcode)
        status = 'ok'
        if opcode == 1: # add
            input1 = self.get_input(ip+1, paramode[0])
            input2 = self.get_input(ip+2, paramode[1])
            output_index = self.get_writeindex(ip+3, paramode[2])
            self.memory[output_index] = input1 + input2
            ip = ip + 4
        if opcode == 2: # multiply
            input1 = self.get_input(ip+1, paramode[0])
            input2 = self.get_input(ip+2, paramode[1])
            output_index = self.get_writeindex(ip+3, paramode[2])
            self.memory[output_index] = input1*input2
            ip = ip + 4
        if opcode == 3: # get input
            if len(self.inputs) == 0:
                #self.ip = ip
                status = "wait"
            else:
                output_index = self.get_writeindex(ip+1, paramode[0])
                self.memory[output_index] = self.inputs.pop(0)
                ip = ip + 2
        if opcode == 4: # send output
            a = self.get_input(ip+1, paramode[0])
            self.outputs.append(a)
            ip = ip + 2
        if opcode == 5: # jump if not zero
            input1 = self.get_input(ip+1, paramode[0])
            input2 = self.get_input(ip+2, paramode[1])
            ip = input2 if input1 != 0 else ip+3
        if opcode == 6: # jump if zero
            input1 = self.get_input(ip+1, paramode[0])
            input2 = self.get_input(ip+2, paramode[1]) 
            ip = input2 if input1 == 0 else ip+3
        if opcode == 7: # less than
            input1 = self.get_input(ip+1, paramode[0])
            input2 = self.get_input(ip+2, paramode[1])
            output_index = self.get_writeindex(ip+3, paramode[2])
            self.memory[output_index] = 1 if input1 < input2 else 0
            ip = ip + 4
        if opcode == 8: # equals
            input1 = self.get_input(ip+1, paramode[0])
            input2 = self.get_input(ip+2, paramode[1])
            output_index = self.get_writeindex(ip+3, paramode[2])
            self.memory[output_index] = 1 if input1 == input2 else 0
            ip = ip + 4
        if opcode == 9: # update relative base
            self.relativebase = self.relativebase + self.get_input(ip+1, paramode[0])
            ip = ip + 2
        if opcode == 99: # halt
            status = 'halt'
        self.ip = ip
        return status

    def run(self):
        while True:
            self.status = self.step()
            if self.status == 'wait' or self.status == 'halt':
                break