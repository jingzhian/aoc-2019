## A New Game

# Arcade Cabinet runs Intcode software - the input
# - Primitive screen capable of drawing square tiles on a grid
# - Software draws tiles to the screen with output instructions
# - Every three output instructions specify the x position (from left), y position (from top), and tile id

# Tile ID
# 0 is a empty tile: no game object
# 1 is a wall tile: indestructible barriers
# 2 is a block tile: broken by ball
# 3 is a horizontal paddle: indestructible
# 4 is a ball tile: move diagonally and bounces off objects

from intcode import Computer
import numpy as np
import time

with open('input.txt') as file:
    tokens = file.read().split(",")

def print_game(game):
    x, y = zip(*game.keys())
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    for row in range(ymax - ymin + 1):
        for col in range(xmax - xmin + 1):
            x = col + xmin
            y = row + ymin
            tile = game.get((x,y), 0)
            ch = ' '
            if tile == 1:
                ch = '▇'
            elif tile == 2:
                ch = '#'
            elif tile == 3:
                ch = '-'
            elif tile == 4:
                ch = 'o'
            print(ch, end='')
        print('\n', end='')


# Mission 1: Get block tiles when game exits

intcode = [int(token) for token in tokens]
arcade = Computer(intcode)
game = {}
status = 'ok'
while status != 'halt':
    status = arcade.step()
    if len(arcade.outputs) == 3:
        game[(arcade.outputs[0], arcade.outputs[1])] = arcade.outputs[2]
        arcade.outputs = []
print(sum(tiles == 2 for coord, tiles in game.items()))
print_game(game)

# Mission 2: Find score after breaking the last block
# Game did not run because I didn't put in any quarters - Set memory address 0 to 2 to play for free

# Input instruction to joy stick
# - neutral position, provide 0
# - tilted to the left provide -1
# - tilted to the right provide 1

# Segment display single number for player's current score
# When three outputs specify X = -1, Y =0, the third instruction is a new score

intcode[0] = 2
arcade2 = Computer(intcode)
game2 = {}
status = 'ok'
while status != 'halt':
    status = arcade2.step()
    if len(arcade2.outputs) == 3:
        x, y, value = arcade2.outputs
        game2[(x, y)] = value
        arcade2.outputs = []
        if x == -1:
            score = value
        if value == 3:
            joystick_x = x
        if value == 4: 
            ball_x = x
    if status == 'wait':
        arcade2.inputs.append(np.sign(ball_x - joystick_x))
        # print(arcade2.inputs)
        print(f"SCORE: {score}")
        print_game(game2)
        time.sleep(0.1)
print(score)