# 
# Images are sent as a series of digits that each represent the color of a single pixel.
# The digits fill each row of the image left-to-right, then move downward to the next row, filling rows top-to-bottom until every pixel of the image is filled.
# Each image actually consists of a series of identically-sized layers that are filled in this way.

# Mission 1: find layer with least 0 digit - then what is the number of 1 digits multiplied by the number of 2 digits?

width = 25
height = 6
pixels = 25*6
print(pixels)

with open("input.txt") as file:
    line = file.read()
    data = [int(token) for token in line]

layers = [data[i:i+pixels] for i in range(0, len(data), pixels)]
layers_zero = [layer.count(0) for layer in layers]
layers_zero_min_ind = layers_zero.index(min(layers_zero))
layer_select = layers[layers_zero_min_ind]
result = layer_select.count(1) * layer_select.count(2)
print(result)

# Mission 2: Decode Image
# 0 is black, 
# 1 is white, and 
# 2 is transparent.

image = [2]*150
for layer in layers:
    for pixel in range(len(layer)):
        if image[pixel]==2:
            image[pixel] = layer[pixel]

for i in range(0, len(image),25):
    line = image[i:i+24]
    line = [' ' if x == 0 else str(x) for x in line ]
    print(line, '\n') 