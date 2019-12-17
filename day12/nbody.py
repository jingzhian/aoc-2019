## N-Body Problem

# tracking the four largest moons of Jupiter: Io, Europa, Ganymede, and Callisto.
# - after a brief scan
# - calculate the position of each moon (puzzle input)
# - simulate motion to avoid them
# - compute total energy in the system: potential + kinetic

# About the moons:
# - 3-dimensional position: x, y, z
# - 3-dimensional velocity: x, y, z
# - Velocity of each moon starts at 0

# Simulate in time steps
# 1. Update the velocity of every moon by applying gravity
#    - consider every pair of moons
#    - on each axis (x, y, z) the velocity of each moon changes by exactly +1 or -1 to pull the moons together
# 2. Update position of every moon by applying velocity
# 3. Time progresses by 1 step once all positions are updated

# Definition of energies
# - Potential: sum of absolute values of x, y, z coordinates
# - Kinetic: sum of absolute values of velocity coordinates

## Mission 1: Get the total energy after simulating moons for 1000 steps
## Mission 2: Number of steps until all moon positions and velocities match a previous point in time
# - Each direction operates independent of each other
# - The initial step must be part of the loop because the stepping is reversible

from functools import reduce
from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)

def lcms(*numbers):
    return reduce(lcm, numbers)


class Moon:
    def __init__(self, scan):
        self.x, self.y, self.z = self.decode_scan(scan)
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def save_init(self):
        self.initx = self.x
        self.inity = self.y
        self.initz = self.z
        self.initvx = self.vx
        self.initvy = self.vy
        self.initvz = self.vz

    def get_energies(self): 
        pe = abs(self.x) + abs(self.y) + abs(self.z)
        ke = abs(self.vx) + abs(self.vy) + abs(self.vz)
        te = ke * pe
        print('pot = ' , pe, ', kin = ', ke, ', tot =', te)
        return te

    def decode_scan(self, scan):
        x = int(scan[(scan.find('x')+2) : (scan.find(', y'))])
        y = int(scan[(scan.find('y')+2) : (scan.find(', z'))])
        z = int(scan[(scan.find('z')+2) : (scan.find('>'))])
        return x, y, z

    def show(self):
        print('pos=<x =', self.x, ', y =', self.y, ', z=', self.z, '>, vel=< x =', self.vx, ', y =', self.vy, ', z =', self.vz, '>')

    def update_pos(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.z = self.z + self.vz

def update_vel(moon1, moon2): # update the velocity of the moons
    
    dvx1, dvx2 = compare_pos(moon1.x, moon2.x)
    moon1.vx += dvx1
    moon2.vx += dvx2
    
    dvy1, dvy2 = compare_pos(moon1.y, moon2.y)
    moon1.vy += dvy1
    moon2.vy += dvy2
    
    dvz1, dvz2 = compare_pos(moon1.z, moon2.z)
    moon1.vz += dvz1
    moon2.vz += dvz2
    
    return moon1, moon2

def compare_pos(pos1, pos2):
    if pos1 < pos2:
        dv1 = 1
        dv2 = -1
    elif pos1 > pos2:
        dv1 =-1
        dv2 =1
    else:
        dv1 = 0
        dv2 = 0
    return dv1, dv2

def check_repeat(moons, step, repeat_step):
    if repeat_step[0] == 0: #check x coordinate
        pos_x_repeat = [moons[i].x == moons[i].initx for i in range(4)]
        pos_vx_repeat = [moons[i].vx == moons[i].initvx for i in range(4)]
        if sum([*pos_x_repeat, *pos_vx_repeat]) == 8:
            repeat_step[0] = step
        else:
            repeat_step[0] = 0
    if repeat_step[1] == 0: #check y coordinate
        pos_y_repeat = [moons[i].y == moons[i].inity for i in range(4)]
        pos_vy_repeat = [moons[i].vy == moons[i].initvy for i in range(4)]
        if sum([*pos_y_repeat, *pos_vy_repeat]) == 8:
            repeat_step[1] = step
        else:
            repeat_step[1] = 0
    if repeat_step[2] == 0: #check z coordinate
        pos_z_repeat = [moons[i].z == moons[i].initz for i in range(4)]
        pos_vz_repeat = [moons[i].vz == moons[i].initvz for i in range(4)]
        if sum([*pos_z_repeat, *pos_vz_repeat]) == 8:
            repeat_step[2] = step
        else:
            repeat_step[2] = 0
    return repeat_step
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${fileDirname}",
        }
    ]
}
# Get input
with open('test2.txt') as file:
    scans = file.read().splitlines()

steps = 1000
step = 00

moons = [Moon(scans[i]) for i in range(4)]

for step in range(steps):

    # Update veocity of the moons 
    for i in range(4):
        for j in range(i+1, 4):
            moons[i], moons[j] = update_vel(moons[i], moons[j])

    # Update positions of the moons
    [moons[i].update_pos() for i in range(4)]
    
    ## Show new steps
    #print('After ', step+1, 'steps:')
    #[moons[i].show() for i in range(4)]

# Compute total energy
print('Get energies:')
total_energy = sum([moons[i].get_energies() for i in range(4)])
print('Sum of total energy: ', total_energy)


newmoons = [Moon(scans[i]) for i in range(4)]
[newmoons[i].save_init()for i in range(4)]

repeat_step = [0]*3 # for each coordinate
step = 0

while sum(i == 0 for i in repeat_step) > 0:
    
    # Update veocity of the moons 
    for i in range(4):
        for j in range(i+1, 4):
            newmoons[i], newmoons[j] = update_vel(newmoons[i], newmoons[j])

    # Update positions of the moons
    [newmoons[i].update_pos() for i in range(4)]
    
    # Increment step
    step +=1

    # Check if any coordinate has repeated
    repeat_step = check_repeat(newmoons, step, repeat_step)

print(repeat_step)
repeat_no = lcms(*repeat_step)
print('The universe repeats after ', repeat_no, ' steps')