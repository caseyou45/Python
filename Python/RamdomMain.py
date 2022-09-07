from random import randint
import pafy
import cv2
import FileHandler
from AnalysisClass import Analysis
from PIL import Image
import requests
import math
from io import BytesIO
#from bs4 import BeautifulSoup
from urllib.request import urlopen


def getChoice():
    choice = -1

    while choice < 0:
        try:

            choice = int(
                input("\n1) Jellyfish Method \n0) Quit \n\nChoose generation method: "))

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


def lightningMethod():

    response = requests.get(
        "https://cdn.star.nesdis.noaa.gov/GOES16/GLM/CONUS/EXTENT3/1250x750.jpg")
    img = Image.open(BytesIO(response.content))
    pix = img.load()
    width = img.size[0] - 20
    height = img.size[1] - 20

    for x in range(0, width):
        for y in range(0, height):
            r, g, b = pix[x, y]

            if r > 200 and g < 70 and b < 70:
                createBlueBox(x, y, pix)


def createBlueBox(x, y, pix):
    for i in range(x - 5, x + 5):
        pix[i,  y + 5] = (0, 0, 255)
        pix[i,  y - 5] = (0, 0, 255)
    for i in range(y - 5, y + 5):
        pix[x + 5,  i] = (0, 0, 255)
        pix[x - 5,  i] = (0, 0, 255)


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
        yWidth = frame.shape[1]

        count = 0
        section = 0

        for x in range(0, xWidth, 2):
            # This splits each picture in to 9 sections
            if count == 54:
                section += 1
                count = 0

            count += 1

            for y in range(0, yWidth, 2):
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


def main():

    choice = getChoice()

    while choice != 0:

        if choice == 1:
            jellyFishMethod()

        choice = getChoice()


main()
