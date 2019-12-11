# Part 1
# a few key facts about the password:

# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

# Other than the range rule, the following are true:

#111111 meets these criteria (double 11, never decreases).
#223450 does not meet these criteria (decreasing pair of digits 50).
#123789 does not meet these criteria (no double).


# Part 2
# the two adjacent matching digits are not part of a larger group of matching digits
# 112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
# 123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
# 111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

import numpy as np
from collections import Counter

test = 0
part2 = 1

if test:
    lower = 234400
    upper = 234500
else:
    lower = 278384
    upper = 824795

def isvalid1(i):
    i = [int(x) for x in str(i)] 
    decrease_ind = np.where(np.subtract(i[1:], i[:-1])< 0)[0] #number of digits decrease
    same_ind = np.where(np.subtract(i[1:], i[:-1])== 0)[0] #duplicate is present
    return len(decrease_ind) == 0 and len(same_ind) >= 1

def isvalid2(i):
    i = [int(x) for x in str(i)]
    decrease_ind = np.where(np.subtract(i[1:], i[:-1])< 0)[0] #number of digits decrease
    double_ind = any(count == 2 for count in Counter(i).values())
    return len(decrease_ind) == 0 and double_ind

# Part 1
print('Part 1 no. of passwords: ', sum(1 for i in range(lower, upper+1) if isvalid1(i)))
print('Part 2 no. of passwords: ', sum(1 for i in range(lower, upper+1) if isvalid2(i)))
