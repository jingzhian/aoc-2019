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

test = 0
part2 = 1

if test:
    range0 = 234400
    range1 = 234500
else:
    range0 = 278384
    range1 = 824795

# Part 1
counter = 0
for i in range(range0, range1+1):

    i = [int(x) for x in str(i)] 
    decrease_ind = np.where(np.subtract(i[1:], i[:-1])< 0)[0] #number of digits decrease
    same_ind = np.where(np.subtract(i[1:], i[:-1])== 0)[0] #duplicate is present
    if len(decrease_ind) == 0 and len(same_ind) >= 1:
        if part2:
            if len(same_ind) == 1:
                counter+=1
                #print(same_ind)
            elif len(np.where(np.subtract(same_ind[1:], same_ind[:-1])>1)[0])>0:
                if len(same_ind) <= 3:
                    counter +=1
                elif sum(same_ind) !=8:
                    counter+=1
        else:
            counter +=1
print('Number of possible passwords: ', counter)


