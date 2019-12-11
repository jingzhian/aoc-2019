import math

def print_interator(it):
    for x in it:
        print(x, end=' ')
    print('') # for new line

def getfuel4mass(it):
    fuel_4mass = 0
    for x in it:
        fuel_4mass += (math.floor(x/3)-2)
    print('Total fuel = ', fuel_4mass)

def getfuel(mass):
    fuel = max(0, (math.floor(mass/3)-2))
    return fuel

def gettotalfuel(it):
    totalfuel = 0
    for x in it:
        fuel_4mass = getfuel(x)
        total_modulefuel = fuel_4mass
        fuel_4fuel = fuel_4mass
        while fuel_4fuel > 0:
            fuel_4fuel = getfuel(fuel_4fuel)
            total_modulefuel += fuel_4fuel
        totalfuel += total_modulefuel
    print('Total final fuel = ', totalfuel)

with open("input.txt") as file:
    masses = list(map(int, file.readlines()))

print(type(masses))
print_interator(masses)
getfuel4mass(masses)
gettotalfuel(masses)
