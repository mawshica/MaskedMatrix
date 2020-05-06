#!/usr/bin/env python3

import argparse
import time
from PIL import Image
import string
import random
import os

parser = argparse.ArgumentParser(description="Create matrix styled effect with an use of a image mask")
parser.add_argument('--mask', '-m', required=True, help="Path of an image mask")
parser.add_argument('--threshold', '-t', help="Compared with pixels, if pixel is brighter than threshold, it will get "
                                              "drawn", default=5)
parser.add_argument('--x', '-x', type=int, help="x size of the final output")
parser.add_argument('--y', '-y', type=int, help="y size of the finak output")
parser.add_argument('--delay', '-d', type=float, help="how many seconds to wait after each iteration", default=1)

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

imagePath = args.mask
resultWidth = args.x
resultHeight = args.y
delay = args.delay
threshold = int(args.threshold)

im = Image.open(imagePath)
pixels = im.load()
width, height = im.size

if resultWidth is None:
    resultWidth = windowX

if resultHeight is None:
    resultHeight = windowY

widthStep = width / resultWidth
heightStep = height / resultHeight

offsetX = int((windowX - resultWidth) / 2)
offsetY = int((windowY - resultHeight) / 2)

symbolPool = string.ascii_letters + string.digits + "`-=[]\'\\/.,<;~!@#$%^&*()_+}{|\":?>"

while True:

    for y in range(resultHeight):

        for i in range(int(offsetX)):
            print(" ", end="", flush=False)

        for x in range(resultWidth):
            imgX = int(x * widthStep)
            imgY = int(y * heightStep)
            pix = pixels[imgX, imgY]
            s = sum(list(pix))

            if s > threshold:
                print(random.choice(symbolPool), end="", flush=False)
            else:
                print(" ", end="", flush=False)

        print("", flush=False)

    for i in range(int(offsetY)):
        print("", flush=False)

    print("", end="", flush=True)

    time.sleep(delay)
