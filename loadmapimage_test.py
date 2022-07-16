import numpy as np
import PIL.Image


def arrayEqual(array1, array2):
    if len(array1) != len(array2):
        return False
    else:
        for k in range(len(array1)):
            if array1[k] != array2[k]:
                return False #when at least one element is different, return False
    return True #this happens only when every element is the same


def findColorInImage(color, image):
    colorIndices = []
    for i in range(len(image)):
        for j in range(len(image[i])):
            if arrayEqual(color, image[i][j]):
                colorIndices.append([j, i])
    return colorIndices


def findObjectTypeInImage(object_type, color1, color2, image):
    #how does this function work for objects that are slim? (1 m = 1 pixel wide/long)
    color1Indices = findColorInImage(color1, image)
##    print(f'color1Indices: {color1Indices}')
    lenx, leny = 1, 1
    objects = []
    if 'fence' in object_type:
        for index in color1Indices:
            deltai, deltaj = 0, 0
##            print(f'index: {index}')
            i, j = index[0], index[1]
            if arrayEqual(color2, image[j][i+1]) and arrayEqual(color2, image[j][i-1]):
##                print('direction i', i, j)
                i1, i2 = i - 1, i + 1
                while arrayEqual(color2, image[j][i1]) == True and i1 >= 1:
                    i1 -= 1
                while arrayEqual(color2, image[j][i2]) == True and i2 <= len(image[i]):
                    i2 += 1
##                print(f'i2, i1: {i2, i1}')
                deltai = i2 - i1 - 1
                deltaj = 1
            elif arrayEqual(color2, image[j+1][i]) and arrayEqual(color2, image[j-1][i]):
##                print('direction j', i, j)
                j1, j2 = j - 1, j + 1
                while arrayEqual(color2, image[j1][i]) == True and j1 >= 1:
                    j1 -= 1
                while arrayEqual(color2, image[j2][i]) == True and j2 <= len(image[j]):
                    j2 += 1
##                print(f'j2, j1: {j2, j1}')
                deltai = 1
                deltaj = j2 - j1 - 1
##            print(f'deltai, deltaj: {deltai, deltaj}')
            if deltai > 1 and deltaj > 1:
                objects.append([index[0], index[1], deltai, deltaj])
    else:
        for index in color1Indices:
            deltai, deltaj = 0, 0
##            print(index)
##            print('direction j')
            i, j = index[0], index[1]
            while arrayEqual(color2, image[j][i]) == False and i >= 1:
                i -= 1
            j1, j2 = j, j
            while arrayEqual(color2, image[j1][i]) == True and j1 >= 1 and arrayEqual(color2, image[j1][i+1]) == False:
                j1 -= 1
            while arrayEqual(color2, image[j2][i]) == True and j2 <= len(image[j]) and arrayEqual(color2, image[j2][i+1]) == False:
                j2 += 1
            deltaj = j2 - j1 + 1
##            print('direction i')
            i, j = index[0], index[1]
            while arrayEqual(color2, image[j][i]) == False and j >= 1:
                j -= 1
            i1, i2 = i, i
            while arrayEqual(color2, image[j][i1]) == True and i1 >= 1 and arrayEqual(color2, image[j+1][i1]) == False:
                i1 -= 1
            while arrayEqual(color2, image[j][i2]) == True and i2 <= len(image[i]) and arrayEqual(color2, image[j+1][i2]) == False:
                i2 += 1
            deltai = i2 - i1 + 1

            if deltai > 1 and deltaj > 1:
                objects.append([index[0], index[1], deltai, deltaj])
    return objects


def findObjectsInImage2(image, colors, object_color_codes):
    objects = {}
    for name, color_code in object_color_codes.items():
        result = findObjectTypeInImage(name, colors[color_code[0]], colors[color_code[1]], image)
        objects[name] = result
    return objects


def checkForFrame(image, center_i, center_j, frame_color):
    #check dimension i in decreasing direction
    i, j = center_i, center_j
    m, n, o = image.shape
    while arrayEqual(frame_color, image[j][i]) == False and i >= 1:
        i -= 1
    j1, j2 = j, j
    while arrayEqual(frame_color, image[j1][i]) == True and j1 >= 1 and arrayEqual(frame_color, image[j1][i+1]) == False:
        j1 -= 1
    while arrayEqual(frame_color, image[j2][i]) == True and j2 < m - 1 and arrayEqual(frame_color, image[j2][i+1]) == False:
        j2 += 1
##    print(f'j2, j1: {j2, j1}')
    deltaj = j2 - j1 + 1
    #check dimension j in decreasing direction
    i, j = center_i, center_j
    while arrayEqual(frame_color, image[j][i]) == False and j >= 1:
        j -= 1
    i1, i2 = i, i
    while arrayEqual(frame_color, image[j][i1]) == True and i1 >= 1 and arrayEqual(frame_color, image[j+1][i1]) == False:
        i1 -= 1
    while arrayEqual(frame_color, image[j][i2]) == True and i2 < n - 1 and arrayEqual(frame_color, image[j+1][i2]) == False:
        i2 += 1
##    print(f'i2, i1: {i2, i1}')
    deltai = i2 - i1 + 1
    return deltai, deltaj


def checkForFrameFence(image, center_i, center_j, frame_color):
##    print(f'center_i, center_j: {center_i, center_j}')
    i, j = center_i, center_j
    m, n, o = image.shape
    if arrayEqual(frame_color, image[j][i+1]) and arrayEqual(frame_color, image[j][i-1]):
        i1, i2 = i - 1, i + 1
        while arrayEqual(frame_color, image[j][i1]) == True and i1 >= 1:
            i1 -= 1
        while arrayEqual(frame_color, image[j][i2]) == True and i2 < n - 1: #and (limit) i or j???
            i2 += 1
        deltai = i2 - i1 - 1
        deltaj = 1
    elif arrayEqual(frame_color, image[j+1][i]) and arrayEqual(frame_color, image[j-1][i]):
        j1, j2 = j - 1, j + 1
        while arrayEqual(frame_color, image[j1][i]) == True and j1 >= 1:
            j1 -= 1
        while arrayEqual(frame_color, image[j2][i]) == True and j2 < m - 1: #and (limit) i or j???
            j2 += 1
        deltai = 1
        deltaj = j2 - j1 - 1
    return deltai, deltaj


def findObjectsInImage(image, object_definitions):
    #objects_definitions = { object_type : [center_color, frame_color], ...}
    center_colors = { object_type : colors[0] for object_type, colors in object_definitions.items()}
    frame_colors = { object_type : colors[1] for object_type, colors in object_definitions.items()}
    objects = {}
    for i in range(len(image)):
        for j in range(len(image[i])):
            for object_type, center_color in center_colors.items():
                if arrayEqual(center_color, image[i][j]):
##                    print(object_type, j, i)
                    frame_color = frame_colors[object_type]
                    if 'fence' in object_type:
                        length_i, length_j = checkForFrameFence(image, j, i, frame_color)
                    else:
                        length_i, length_j = checkForFrame(image, j, i, frame_color)
                    if 'tree' in object_type or 'box' in object_type:
                        length_i -= 1
                        length_j -= 1
##                    print(length_i, length_j)
                    if object_type not in objects.keys():
                        objects[object_type] = []
                        objects[object_type].append([j, i, length_i, length_j])
                    else:
                        objects[object_type].append([j, i, length_i, length_j])
                    continue
    return objects


def findStart(image, start_color):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if arrayEqual(start_color, image[i][j]):
                return j, i
    return None


#RGBA values for basic colors in Paint
colors = {}
colors['black'] = np.array([0, 0, 0, 255])
colors['grey'] = np.array([127, 127, 127, 255])
colors['crimson'] = np.array([136, 0, 21, 255])
colors['red'] = np.array([237, 28, 36, 255])
colors['orange'] = np.array([255, 127, 39, 255])
colors['yellow'] = np.array([255, 242, 0, 255])
colors['green'] = np.array([34, 177, 76, 255])
colors['turquoise'] = np.array([0, 162, 232, 255])
colors['blue'] = np.array([63, 72, 204, 255])
colors['violet'] = np.array([163, 73, 164, 255])
colors['white'] = np.array([255, 255, 255, 255])
colors['lightgrey'] = np.array([195, 195, 195, 255])
colors['brown'] = np.array([185, 122, 87, 255])
colors['rose'] = np.array([255, 174, 201, 255])
colors['gold'] = np.array([255, 201, 14, 255])
colors['lightyellow'] = np.array([239, 228, 176, 255])
colors['lightgreen'] = np.array([181, 230, 29, 255])
colors['lightturquoise'] = np.array([153, 217, 234, 255])
colors['bluegrey'] = np.array([112, 146, 190, 255])
colors['lavender'] = np.array([200, 191, 231, 255])
colors['lightgrey1'] = np.array([232, 232, 232, 255]) #navMesh start_pos, end_pos
colors['pink'] = np.array([255, 0, 255, 255]) #player start position

colors['black1'] = np.array([1, 1, 1, 255])
colors['black2'] = np.array([2, 2, 2, 255])
colors['black3'] = np.array([3, 3, 3, 255])
colors['black4'] = np.array([4, 4, 4, 255])
colors['black5'] = np.array([5, 5, 5, 255])
colors['black6'] = np.array([6, 6, 6, 255])
colors['black7'] = np.array([7, 7, 7, 255])
colors['black8'] = np.array([8, 8, 8, 255])
colors['black9'] = np.array([9, 9, 9, 255])
colors['black10'] = np.array([10, 10, 10, 255])
colors['black11'] = np.array([11, 11, 11, 255])
colors['black12'] = np.array([12, 12, 12, 255])
colors['black13'] = np.array([13, 13, 13, 255])
colors['black14'] = np.array([14, 14, 14, 255])
colors['black15'] = np.array([15, 15, 15, 255])
colors['black16'] = np.array([16, 16, 16, 255])
colors['black17'] = np.array([17, 17, 17, 255])
colors['black18'] = np.array([18, 18, 18, 255])

object_definitions = {}
object_definitions['house1'] = [ colors['black1'], colors['red'] ]
object_definitions['house2'] = [ colors['black2'], colors['crimson'] ]
object_definitions['tree1'] = [ colors['black3'], colors['green'] ]
object_definitions['fence1'] = [ colors['black4'], colors['lavender'] ]
object_definitions['road1'] = [ colors['black5'], colors['grey'] ]
object_definitions['road2'] = [ colors['black6'], colors['lightgrey'] ]
object_definitions['road3'] = [ colors['black7'], colors['lightyellow'] ]
object_definitions['water1'] = [ colors['black8'], colors['blue'] ]
object_definitions['box1'] = [ colors['black9'], colors['brown'] ]
object_definitions['shop1'] = [ colors['black11'], colors['orange'] ]
object_definitions['post1'] = [ colors['black12'], colors['gold'] ]
object_definitions['church1'] = [ colors['black13'], colors['bluegrey'] ]
object_definitions['school1'] = [ colors['black14'], colors['rose'] ]

object_definitions['car_blue'] = [ colors['black15'], colors['turquoise'] ]
object_definitions['truck_red'] = [ colors['black16'], colors['red'] ]

object_definitions['field1'] = [ colors['black17'], colors['yellow'] ]
##object_definitions[''] = [ colors[''], colors[''] ]


if __name__ == '__main__':
##    image = PIL.Image.open('colors.png')
##    image = np.array(image)
##    print(image)
##    for row in image:
##        for el in row:
##            for key, value in colors.items():
##                if arrayEqual(value, el):
##                    print(key)

    
    image = PIL.Image.open('world_test222.png')
    image = np.array(image)
##    print(image[8])

##    colorIndices = findColorInImage(colors['black'], image)
##    print(len(colorIndices))
##    print(colorIndices)
##
##    objects = findObjectTypeInImage(colors['black'], colors['grey'], image)
##    print(objects)

    objects = findObjectsInImage2(image, colors, object_color_codes)
    print(objects)
