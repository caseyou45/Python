from operator import truediv
from random import randint
import pafy
import cv2
import FileHandler
from AnalysisClass import Analysis
from PIL import ImageChops
# from bs4 import BeautifulSoup
from urllib.request import urlopen


def getChoice():
    choice = -1

    while choice < 0:
        try:

            choice = int(
                input("\n1) Monterey Bay Jellyfish  \n2) Tokyo-Shinjuku Street  \n0) Quit \n\nChoose generation method: "))

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

    image = 0

    frameCount = int(input("How many frames of the video should we analyze? "))

    analyze = Analysis()

    FileHandler.createFolder()

    success = True

    capture = fetchCapture("https://www.youtube.com/watch?v=pT9_HJr-nso")

    while success and image < frameCount:

        success, frame = capture.read()

        xWidth = frame.shape[0]
        yHeight = frame.shape[1]

        count = 0
        section = 0

        for x in range(0, xWidth, 2):
            # This splits each picture in to 9 sections
            if count == 54:
                section += 1
                count = 0

            count += 1

            for y in range(0, yHeight, 2):
                # b = frame[x, y, 0]
                # g = frame[x, y, 1]
                r = frame[x, y, 2]

                # If there's enough red (jellyfish!), then this logic is applied:
                # 1) Create a decimal equivalent of the section we are in (8 = .8)
                # 2) Then add that value to how much red is in the pixel (32 / 255 == .125 / 10 = .0125)
                # 3) So the resulting number is based on where the jelly is and how red it appears (.8125)
                if r > 50:
                    frame[x, y, 0] = 255
                    frame[x, y, 1] = 255
                    frame[x, y, 2] = 255
                    n = (section / 10) + ((r / 255)/10)

                    analyze.addTrueRandomNumbers(n)
                    analyze.addPseudoRandomNumber(randint(0, 9))

        FileHandler.saveImage(frame, image)
        image += 1

    FileHandler.saveNumberFile(analyze.getTrueRandomNumbers())

    analyze.formatAnalysisDocument()


def liveCamGeneral(url):

    image = 0

    differenceAmount = .3

    frameCount = int(input("How many frames of the video should we analyze? "))

    analyze = Analysis()

    FileHandler.createFolder()

    success = True

    capture = fetchCapture(url)

    success, base = capture.read()

    while success and image < frameCount:

        count = 0
        section = 0

        success, frame = capture.read()

        alter = frame

        xWidth = frame.shape[0]
        yHeight = frame.shape[1]

        for x in range(0, xWidth, 2):
            # This splits each picture in to 9 sections
            if count == 54:
                section += 1
                count = 0

            count += 1
            for y in range(0, yHeight, 2):
                b = frame[x, y, 0]
                g = frame[x, y, 1]
                r = frame[x, y, 2]

                baseB = base[x, y, 0]
                baseG = base[x, y, 1]
                baseR = base[x, y, 2]

                if comapreTwoPixel(b, baseB) > differenceAmount:
                    alter[x, y, 0] = 255
                    n = (section / 10) + ((b / 255)/10)
                    analyze.addTrueRandomNumbers(n)
                    analyze.addPseudoRandomNumber(randint(0, 9))

                if comapreTwoPixel(g, baseG) > differenceAmount:
                    alter[x, y, 1] = 255
                    n = (section / 10) + ((g / 255)/10)
                    analyze.addTrueRandomNumbers(n)
                    analyze.addPseudoRandomNumber(randint(0, 9))

                if comapreTwoPixel(r, baseR) > differenceAmount:
                    alter[x, y, 2] = 255
                    n = (section / 10) + ((r / 255)/10)
                    analyze.addTrueRandomNumbers(n)
                    analyze.addPseudoRandomNumber(randint(0, 9))

        base = frame

        FileHandler.saveImage(alter, image)
        image += 1

    FileHandler.saveNumberFile(analyze.getTrueRandomNumbers())

    analyze.formatAnalysisDocument()


def comapreTwoPixel(base, next):
    difference = (base / 2) - (next / 2)
    return abs(difference) / (255 / 2)


def main():

    choice = getChoice()

    while choice != 0:

        if choice == 1:
            jellyFishMethod()

        if choice == 2:
            liveCamGeneral("https://www.youtube.com/watch?v=RQA5RcIZlAM")

        choice = getChoice()


main()
