import argparse
import time
from PIL import Image
import string
import random
import os

parser = argparse.ArgumentParser(description="Create matrix styled effect with an use of a image mask")
parser.add_argument('-mask', metavar='m', help="Path of an image mask")
parser.add_argument('--x', metavar='x', type=int, help="x size of the final output", default=-1)
parser.add_argument('--y', metavar='y', type=int, help="y size of the finak output", default=-1)
parser.add_argument('--iterations', metavar='i', type=int, help="how many iterations should the animation go trough, 0 for infinite", default=0)
parser.add_argument('--delay', metavar='d', type=float, help="how many seconds to wait after each iteration", default=1)

args = parser.parse_args()

if args.iterations < 0:
    raise Exception("Please enter a positive number for iterations")

sizeResult = os.popen("stty size", 'r').read().split()

windowX = 0
windowY = 0

if sizeResult.__len__() != 0:
    windowY, windowX = sizeResult
    windowX = int(windowX)
    windowY = int(windowY)

infinite = args.iterations == 0
imagePath = args.mask
resultWidth = args.x
resultHeight = args.y
delay = args.delay

im = Image.open(imagePath)
pixels = im.load()
width, height = im.size

if resultWidth == -1:
    resultWidth = width

if resultHeight == -1:
    resultHeight = height

widthStep = width / resultWidth
heightStep = height / resultHeight

offsetX = int((windowX - resultWidth) / 2)
offsetY = int((windowY - resultHeight) / 2)

print(offsetX, offsetY)

symbolPool = string.ascii_letters + string.digits + "`-=[]\'\\/.,<;~!@#$%^&*()_+}{|\":?>"

while True:

    render = ""

    for y in range(resultHeight):

        for i in range(int(offsetX)):
            render += " "

        for x in range(resultWidth):
            imgX = int(x * widthStep)
            imgY = int(y * heightStep)
            pix = pixels[imgX, imgY]

            if pix == 1:
                render += random.choice(symbolPool)
            else:
                render += " "

        render += "\n"

    for i in range(int(offsetY)):
        render += "\n"

    print(render, end="")

    time.sleep(delay)
