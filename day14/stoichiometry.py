import math
from collections import defaultdict

## Stoichiometry
# List of reastions it can perform : puzzle input
# - Every reaction turns some quantities of specific input chemicals into some quantity of an output chemical
# - Almost every chemical is produced by exactly one reaction;
# - the only exception, ORE, is the raw material input to the entire process and is not produced by a reaction.

# Integer multiples of chemicals must be used
# It is ok to have left over chemicals


def get_reactions(filename):
    # INPUT: "1 A, 2 B => 3 C"
    # OUTPUT: recipes["C"] = (3, {"A": 1, "B": 2})
    # USAGE: product_count, reactants = recipes['product_label']
    with open(filename) as file:
        lines  = file.read().splitlines()
    
    reactions = {}
    for line in lines:
        reactants, product = line.split(' => ')
        # Only 1 product in each reaction
        product_no, product = product.split(' ')
        product_no = int(product_no)
        # break down the reactants
        tokens = reactants.split(', ')
        reactants = {}
        for token in tokens:
            reactant_no, reactant = token.split(' ')
            reactant_no = int(reactant_no)
            reactants[reactant] = reactant_no
        reactions[product] = (product_no, reactants)
    return reactions

def check_ismissing(missing):
    missing_no = 0
    for chem, demand_no in missing.items():
        if chem !='ORE' and demand_no > 0:
            missing_no += demand_no
    if missing_no == 0:
        return False
    else:
        return True

def update_missing(missing, reactions):
    newmissing = missing.copy()
    for chem, demand_no in missing.items():           # for each item in missing
        if chem != 'ORE' and demand_no > 0:           # if chemical is not ORE and we need more of it
            multiplier, reactants = reactions[chem]   # get the multiplier for reactions and reactants        
            rxn_no = math.ceil(demand_no/multiplier)        # how many reaction is required to produce at least the desired amount of a product
            for reactant, reactant_no in reactants.items(): # for every reactan required, log the demand
                if reactant in newmissing:          # if the reactant is already present
                    newmissing[reactant] += reactant_no * rxn_no # add the new requirement to existing demand
                else:
                    newmissing[reactant] = reactant_no * rxn_no # if not just add new requirement
            pdt_no = rxn_no * multiplier # compute all the product produced
            newmissing[chem] -= pdt_no # record the product
    return newmissing

def get_required_ore(reactions, fuel_no=1):
    # Cannot change the length of a list while looping over it
    # missing: positive indicates missing, negative indicates surplus
    missing = defaultdict(int, {"FUEL": fuel_no})
    while check_ismissing(missing):
            missing = update_missing(missing, reactions)
    ore_no = missing["ORE"]
    #print(missing)
    #print(ore_no)
    return ore_no


def part1(filename):
    ## Mission 1: what is the minimum amount of ORE required to create one fuel
    reactions = get_reactions(filename)
    #print(len(reactions))
    return get_required_ore(reactions)


def part2(filename, budget):
    ## Mission 2: find maximum amount of fuel you can make given an ORE budget
    reactions = get_reactions(filename)
    # If surplus from formation of 1 fuel does not contribute to the formation of another fuel - more ore is required per fuel:
    fuel_lb = budget // get_required_ore(reactions, 1) 
    # Find an upper bound - coarse search
    ore_lb = get_required_ore(reactions, fuel_lb)
    ore = ore_lb
    multiplier = 1
    while ore < budget:
        multiplier +=1
        ore = get_required_ore(reactions, fuel_lb*multiplier)
    fuel_ub = fuel_lb*multiplier # a upper bound
    ore_ub = ore
    ore_ub_new = 0
    ore_lb_new = 0
    while ore_ub_new != ore_ub or ore_lb_new != ore_lb:
        ore_lb_new = ore_lb
        ore_ub_new = ore_ub
        fuel = int(0.5*(fuel_ub - fuel_lb) + fuel_lb)
        ore = get_required_ore(reactions, fuel)
        print(budget, fuel, ore, ore_lb, ore_ub)
        # if ore_ub is lower than the budget, we need to half it
        if ore < budget:
            fuel_lb = fuel
            ore_lb = ore
        elif ore > budget: 
            fuel_ub = fuel
            ore_ub = ore
        else:
            pass
    print(budget, fuel, ore, ore_lb, ore_ub)

    if ore_ub > budget:
        fuel = fuel_lb
        
    else:
        fuel = fuel_ub
    return fuel


if __name__ == "__main__":
    assert part1("test1.txt") == 31
    assert part1("test2.txt") == 165
    assert part1("test3.txt") == 13312
    assert part1("test4.txt") == 180697
    assert part1("test5.txt") == 2210736

    print(part1("input.txt"))
    print(part2("input.txt", budget=10 ** 12))

