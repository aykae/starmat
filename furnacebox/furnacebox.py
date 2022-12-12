import time, random, math
import json

################
#MATRIX VARS
################
SIM = False

#DIM OF MATRIX
WIDTH = 32
HEIGHT = 32

#
REFRESH = 20

# FILES
FURNACE_FILE = "furnace.txt"
FIRE_FILE = "fire.txt"

#
fireshape = []

firePalette = []
fire = {}

furnacePalette = []
furnace = {}

#list of frame dictionaries mapping pixels to colors
ani = []

#list of smoke objects: [position, color]
smoke = []
SMOKE_COLOR = (50, 50, 50)

#line in the ani file where pixel map begins
pixelStart = 0

#current line in ani file
currLine = 0

if SIM:
    import pygame
    from matsim import MatrixSim
    matrix = MatrixSim(WIDTH, HEIGHT)
else:
    import hub75
    matrix = hub75.Hub75(WIDTH, HEIGHT)

def generateSmoke():
    global smoke
    #dict of gray smoke pixels that quickly float upward
    #randomly generate a couple particles every couple frames

    if random.randint(0, 10) == 5:
        smoke.append([random.randint(5, 31), 16], SMOKE_COLOR)

def drawSmoke():
    global smoke
    #move smoke upwards and variably to the left and right by 1 pixel
    #delete from smoke dict once out of sight

    for s in smoke:
        matrix.set_rgb(s[0][0], s[0][1], 0, 0, 0)

        s[0][1] -= 2

        if s[0][1] > HEIGHT - 1 or s[0][1] < 0:
            smoke.remove(s)
        else:
            matrix.set_rgb(s[0][0], s[0][1], s[1][0], s[1][1], s[1][2])
    
def loadFurnace(filename):
    global furnace, furnacePalette
    
    currLine = 0
    with open(filename, "r") as file:
        lines = file.readlines()
        line = lines[currLine].strip()
        while line != "P":
            # print(line)
            data = [int(i) for i in line.split(" ")]
            color = (data[0], data[1], data[2])
            furnacePalette.append(color)

            currLine += 1
            line = lines[currLine].strip()

        currLine += 1
        line = lines[currLine].strip()
        while currLine != "":
            x = int(line)
            y = -1
            
            currLine += 1
            line = lines[currLine].strip()
            while line != "X":
                line = line.split(' ')
                y = int(line[0])
                c = int(line[1])

                #store pixel
                fkey = str(x) + " " + str(y)
                furnace[fkey] = c

                #increment line
                currLine += 1
                line = lines[currLine].strip()

            currLine += 1
            line = lines[currLine].strip()

def drawFurnace():
    global furnace, furnaePalette

    if len(furnace) <= 0:
        return

    for pixel in furnace.keys():
        cindex = furnace[pixel]
        c = furnacePalette[cindex]
        x, y = pixel.strip().split(" ")
        matrix.set_rgb(x, y, c[0], c[1], c[2])
    

def setup():
    global ani, currLine, pixelStart
    #loads color palette and frame count from file
    loadFurnace(FURNACE_FILE)
    #loadFire(FIRE_FILE)

def drawFrame(flines):
    global palette, frame, frameCount, currLine, pixelStart

    #reset animation
    if frame == 0:
        currLine = pixelStart

    line = flines[currLine].strip()
    while line != "F":
        x = int(line)
        y = -1
        
        currLine += 1
        line = flines[currLine].strip()
        while line != "X":
            line = line.split(' ')
            y = int(line[0])
            c = palette[int(line[1])]

            #draw pixel
            matrix.set_rgb(x, y, c[0], c[1], c[2])

            #increment line
            currLine += 1
            line = flines[currLine].strip()

        currLine += 1
        line = flines[currLine].strip()

    currLine += 1
    frame = (frame + 1) % frameCount




##############
# MAIN LOOP
##############
matrix.start()

setup()
while True:
    drawFurnace()
    matrix.flip()
    #time.sleep(REFRESH / 1000.0)