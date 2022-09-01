from inspect import currentframe
from msvcrt import getch
import pafy
import cv2
import os
from PIL import Image
from io import BytesIO
import numpy as np
from FileHandler import *

frameCount = 0


def getChoice():
    choice = -1

    while choice < 0:
        try:

            choice = int(
                input("Choose generation method: 1) Jellyfish Percentage 0) Quit : "))

            if choice < 0:
                print("Not a valid choice")

        except ValueError:
            print("Illegal Input: Numbers only")

    return choice


def fetchCapture(url):

    video = pafy.new(url)
    best = video.getbest(preftype="mp4")

    capture = cv2.VideoCapture(best.url)

    return capture


def youtubeCapture():
    global frameCount

    randomNumbers = []

    success = True

    capture = fetchCapture("https://www.youtube.com/watch?v=pT9_HJr-nso")

    while success and frameCount < 1:

        success, frame = capture.read()

        xWidth = frame.shape[0]
        yWidth = frame.shape[1]

        for x in range(0, xWidth, 2):
            redCount = 0
            blueCount = 0

            for y in range(0, yWidth, 2):
                b = frame[x, y, 0]
                g = frame[x, y, 1]
                r = frame[x, y, 2]

                # if it's somewhat red (jellyfish!), increment redCount and re-color jelly for display purposes
                if r > 50:
                    redCount += 1
                    frame[x, y, 0] = 255
                    frame[x, y, 1] = 255
                    frame[x, y, 2] = 255
                # if it is not somewhat red, then it's likely water or not-as-red jellyfish parts, so increment blue
                elif b > 50:
                    blueCount += 1

            if redCount > 0:
                randomNumbers.append(sanitizeResult(redCount, yWidth/2))
            else:
                randomNumbers.append(sanitizeResult(blueCount, yWidth/2))

        saveImage(frame, frameCount)

        frameCount += 1

        saveNumberFile(randomNumbers)


def sanitizeResult(count, width):
    num = count / width

    while num < 1:
        num *= 10

    if num > 0:
        num /= 10

    if num != 0 and num != 0.1:
        return num


def main():

    global frameCount

    createFolder()

    choice = getChoice()
    while choice != 0:

        if choice == 1:
            youtubeCapture()

        choice = getChoice()


main()
