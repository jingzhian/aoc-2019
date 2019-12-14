## Create Registration Identifier

# Build a new emergency hull painting robot
# - Move around a grid of square panels onn the side of the ship
# - Detect color of its current panel
# - Paint its current panel black or white
# All panels start with black

# Intecode program as puzzle input
# - Uses input instruction to acces the robot's camera
#   - Provide 0 if robot is over a black panel
#   - Provide 1 if robot is over a white panel
# - Output two values
#   - 0 /1 indicates the color to paint the panel the robot is over: 0 is black, 1 is white
#   - 0/ 1 indicates the direction the robot should turn, 0 is left 90 degrees and 1 is right 90 degrees
# After the robot turns, it should always move forward exactly one panel, robot starts facing up 

## Mission 1: Track number of panels painted at least once

from intcode import Computer


class Robot:
    def __init__(self, program):
        self.x = 0
        self.y = 0
        self.computer = Computer(program)
        self.direction = 0 # N is 0, E is 1, S is 2, W is 3
        self.dxdy = {0:(0, 1), 1:(1, 0), 2:(0, -1), 3:(-1, 0)}

    def move(self):
        dx, dy = self.dxdy[self.direction]
        self.x += dx
        self.y += dy

    def turnleft(self):
        self.direction = (self.direction-1) %4

    def turnright(self):
        self.direction = (self.direction+1) %4

with open('input.txt') as file:
    line = file.read()
    program = list(map(int, line.split(',')))

robot = Robot(program)
colors = {(0,0):1}

while robot.computer.status != 'halt':

    color = colors.get((robot.x, robot.y), 0) # get color under robot
    robot.computer.inputs.append(color)
    robot.computer.run()
    paint_color, direction = robot.computer.outputs[-2:]
    colors[(robot.x, robot.y)] = paint_color
    if direction == 0:
        robot.turnleft()
    else: 
        robot.turnright()
    robot.move()

print('Panels painted: ', len(colors))

# Mission 2

from matplotlib import pyplot as plt

white = [coord for coord, color in colors.items() if color == 1]
x, y = zip(*white)

plt.plot(x, y, 'ko')
plt.show()