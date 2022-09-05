from random import randint
import pafy
import cv2
import FileHandler
from AnalysisClass import Analysis

frameCount = 0


def getChoice():
    choice = -1

    while choice < 0:
        try:

            choice = int(
                input("\n1) Jellyfish Percentage \n0) Quit \n\nChoose generation method:"))

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


def jellyFishMethod():
    global frameCount
    analyze = Analysis()

    FileHandler.createFolder()

    success = True

    capture = fetchCapture("https://www.youtube.com/watch?v=pT9_HJr-nso")

    while success and frameCount < 1:

        success, frame = capture.read()

        xWidth = frame.shape[0]
        yWidth = frame.shape[1]

        for x in range(0, xWidth, 2):
            redCount = 0

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
            if redCount > 0:
                analyze.addTrueRandomNumbers(
                    sanitizeResult(redCount, yWidth/2))
                analyze.addPseudoRandomNumber(randint(0, 9))

        FileHandler.saveImage(frame, frameCount)

        frameCount += 1

        FileHandler.saveNumberFile(analyze.getTrueRandomNumbers())

        analyze.formatAnalysisDocument()


def sanitizeResult(count, width):
    num = count / width

    while num < 1:
        num *= 10

    if num > 0:
        num /= 10

    return num


def main():

    global frameCount

    choice = getChoice()

    while choice != 0:

        if choice == 1:
            jellyFishMethod()

        choice = getChoice()


main()
