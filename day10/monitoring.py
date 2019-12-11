## Monitoring Station
# Input is an asteroid map
# Each position is empty (.) or contains an asteroid (#)
# The asteroids can be described with X,Y coordinates 
# where X is the distance from the left edge and Y is the distance from the top edge 
# (so the top-left corner is 0,0 and the position immediately to its right is 1,0).

# Mission 1: which asteroid is the best place to build a new monitoring station
# A monitoring station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid exactly between them.
# This line of sight can be at any angle, not just lines aligned to the grid or diagonally.
# The best location is the asteroid that can detect the largest number of other asteroids.

import math
import sys

def get_direct(asteroid, asteroids):
    dists = []
    angles = []
    detected = []
    #for i, a in enumerate(asteroids):
    for a in asteroids:
        x_dist = a[0]-asteroid[0]
        y_dist = -a[1]+asteroid[1]
        dist = math.sqrt(y_dist**2 + x_dist**2)
        angle = math.atan2(y_dist, x_dist)*180/math.pi
        # print(angle, angles)
        #if i == 2:
        #    sys.exit(0)
        if angle in angles:
            if dist <= dists[angles.index(angle)]:
                dists[angles.index(angle)] = dist
                detected[angles.index(angle)] = a
        else:
            angles.append(angle)
            dists.append(dist)
            detected.append(a)
    return dists, angles, detected

def get_ordered(center, asteroids):
    dists = []
    angles = []
    vaporder = []
    asteroids.remove(center)
    # get all distances and angles
    for i, a in enumerate(asteroids):
        # Flip coordinate
        y_dist = a[0]-center[0]
        x_dist = -a[1]+center[1]
        dist = math.sqrt(y_dist**2 + x_dist**2)
        angle = round(math.atan2(y_dist, x_dist)*180/math.pi, 6)
        if angle<0:
            angle = 360 + angle
        else:
            angle = angle
    # order asteroids with the same angle
        while angle in angles:
            #print(angle)
            #print(angles)
            #print(dist)
            #print(dists)
            #print(angles.index(angle))
            #sys.exit(0)
            if dist < dists[angles.index(angle)]:
                angles[angles.index(angle)] = angles[angles.index(angle)] + 360
            else:
                angle = angle + 360
        angles.append(angle)
        dists.append(dist)
        vaporder.append(a)
    angles, vaporder = zip(*sorted(zip(angles, vaporder)))
    return angles, vaporder

## Mission 1 - find best asteroid

# Get input
filenames = ["test1.txt", "test2.txt", "test3.txt", "test4.txt", "input.txt"]
testsol= [(5,8,33), (1, 2, 35), (6, 3, 41), (11, 13, 210)]

for f, filename in enumerate(filenames):
    if f == 0:
        print('## MISSION 1')
    if filename == filenames[-1]:
        print('# Running Program')
    else:
        print('# Running Test: ', f+1)

    # Get input
    with open(filename) as file:
        lines = file.read().splitlines()

    # Get asteroids coordinates
    asteroids = [(x,y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == '#']
    detect_no = 0
    best_loc = 0
    for asteroid in asteroids:
        dists, angles, detected = get_direct(asteroid, asteroids)
        #print(asteroid, len(detected))
        if len(detected) > detect_no:
            best_loc = asteroid
            detect_no = len(detected)
    print('Best location is at ', best_loc, '; number detected is ', detect_no)

    if filename == filenames[-1]:
        print('Mission 1 completed :) \n')
    else:
        if testsol[f] == (best_loc[0], best_loc[1], detect_no):
            print('.......Test ', f, ' passed')
        else:
            print('.......Test ', f, ' failed')
            sys.exit(0)


## Mission 2 - find the 200th asteroid to be vaporized
filenames = ["test5.txt", "test4.txt", "input.txt"]
centers = [(8,3), (11, 13), (17, 23)]
vap_id = [1, 200, 200]
testsol = [(8, 1), (8, 2)]

for f, filename in enumerate(filenames):
    if f == 0:
        print('### MISSION 2 Launching')
    if filename == filenames[-1]:
        print('# Running Program')
    else:
        print('# Running Test: ', f+1)

    # Get input
    with open(filename) as file:
        lines = file.read().splitlines()

    # Get asteroids coordinates
    asteroids = [(x,y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == '#']
    angles, vaporder = get_ordered(centers[f], asteroids)
    #print(angles, vaporder)
    vapcoord = vaporder[vap_id[f]-1]
    print(vapcoord)
    if filename == filenames[-1]:
        print('Program comleted. Result is :', vapcoord[0]*100 + vapcoord[1])
    else:
        if testsol[f] == vapcoord:
            print('.......Test ', f, ' passed')
        else:
            print('...... Test ', f, ' failed')
            sys.exit(0)
