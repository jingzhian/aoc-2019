# Universal Orbit Map
# When object BBB orbits around object AAA, it is writen as AAA)BBB - get centers and orbits
# When A orbits B and B orbits C, A indirectly orbits C - some form of recursion / register is needed
# Every object in space orbit around exactly one other object - orbiting is a unique list

#def count_orbit(planet, centers, orbiting):

# missions 1 functions
def get_indirect(i, orbiting, centers, orbit_no):
    if centers[i] in orbiting:
        return get_indirect(orbiting.index(centers[i]), orbiting, centers, orbit_no+1)
    else:
        return orbit_no

def get_orbits(tokens):
    centers   = [token.split(")")[0] for token in tokens]
    orbiting  = [token.split(")")[1] for token in tokens]
    total_no = sum([get_indirect(i, orbiting, centers, 1) for i in range(len(centers))])
    return total_no

# mission 2 functions
def get_path(orbit_path, orbiting, centers):
    if orbit_path[-1] in orbiting:
        orbit_path.append(centers[orbiting.index(orbit_path[-1])])
        return get_path(orbit_path, orbiting, centers)
    else:
        return orbit_path

def get_orbitaltrans(tokens, startpt, endpt):
    centers  = [token.split(")")[0] for token in tokens]
    orbiting = [token.split(")")[1] for token in tokens]
    path1 = get_path(startpt, orbiting, centers)
    path2 = get_path(endpt, orbiting, centers)
    transpath1 = set(path1) - set(path2)
    transpath2 = set(path2) - set(path1)
    pathlength = len(transpath1) + len(transpath2) - 2
    return pathlength

## Set parameters
test = 0
run_mission1 = False
run_mission2 = True

## Get data
if test == 1: # should return 42
    with open("orbitmap-test.txt") as file:
        tokens = file.read().splitlines()
        print(tokens)
elif test == 2:
    with open("orbitmap-test2.txt") as file:
        tokens = file.read().splitlines()
        print(tokens)
else:
    with open("orbitmap.txt") as file:
        tokens = file.read().splitlines()

## Mission 1 - Find total number of direct and indirect orbits
if run_mission1:
    orbit_no = get_orbits(tokens)
    print('total orbits: ', orbit_no)

## Mission 2 - Find number of Orbital Transfers
if run_mission2:
    startpt = ['YOU']
    endpt = ['SAN']
    pathlength = get_orbitaltrans(tokens, startpt, endpt) 
    print('orbital transfers :', pathlength)
    