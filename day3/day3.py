#--- Day 3: Crossed Wires ---
# Two wires are connected to a central port and extend outward on a grid. 
# You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

# Find the intersection point closest to the central port
# Use Manhattan distance for this measurement. 
# While the wires do technically cross right at the central port where they both start, this point does not count, 
# nor does a wire count as crossing with itself.

import matplotlib
matplotlib.use('Agg') 
from matplotlib import pyplot as plt

def get_wiremap(wire):
    tokens = wire.split(",")
    wire_coords=[(0,0)]
    for token in tokens:
        wire_dir = token[0]
        wire_val = int(token[1:])
        if wire_dir == 'R':
            new_wire_coords = [(wire_coords[-1][0] + x, wire_coords[-1][1]) for x in range(1, wire_val+1)]
        if wire_dir == 'L':
            new_wire_coords = [(wire_coords[-1][0] - x, wire_coords[-1][1]) for x in range(1, wire_val+1)]
        if wire_dir == 'U':
            new_wire_coords = [(wire_coords[-1][0] , wire_coords[-1][1] + y) for y in range(1, wire_val+1)]
        if wire_dir == 'D':
            new_wire_coords = [(wire_coords[-1][0] , wire_coords[-1][1] - y) for y in range(1, wire_val+1)]
        wire_coords = wire_coords + new_wire_coords
    return wire_coords

test = 0
if test == 1:
    # Example 1 - should return 159
    wire1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    wire2 = 'U62,R66,U55,R34,D71,R55,D58,R83'

if test == 2:
    # Example 2 - should return 135
    wire1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    wire2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'

if test == 3:
    # Example 3
    wire1 = 'R8,U5,L5,D3'
    wire2 = 'U7,R6,D4,L4'

if test == 0:
    with open("wire1.txt") as file1:
        wire1 = file1.readline()
    with open("wire2.txt") as file2:
        wire2 = file2.readline()

# Get Wire Map
wire1_map  = get_wiremap(wire1)
wire2_map  = get_wiremap(wire2)

# Get Intersection of Wire
wire_meet = set(wire1_map) & set(wire2_map)
wire_meet.remove((0,0))
wire_meet = list(wire_meet)
print(wire_meet)

# Get Manhattan Distance and Find the Minimum
meet_dist = [abs(x) + abs(y) for x, y in wire_meet]
meet_mindist = min(meet_dist)
meet_mindistind = meet_dist.index(meet_mindist)
print('Distances of intersections: ', meet_dist)
print('Minimum intersection: ', meet_mindist)

# Plot the Wires
x, y = zip(*wire1_map)
x2, y2 = zip(*wire2_map)
x3, y3 = zip(*wire_meet)
plt.plot(x, y)
plt.plot(x2, y2)
plt.plot(x3, y3, 'x')
plt.plot(wire_meet[meet_mindistind][0], wire_meet[meet_mindistind][1], 'x')
plt.savefig('plot.png')


# Get the length of wires at intersections
wire_len = [wire1_map.index(point) + wire2_map.index(point) for point in wire_meet]
wire_len_min = min(wire_len)
print('Minimum wire len :', wire_len_min)