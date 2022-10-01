from random import randint
import pafy
import cv2
import FileHandler
from AnalysisClass import Analysis


def getChoice():
    """Prompts users to choose an options and returns that numerical value"""
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
    """Uses pafy to obtain the video from the URL. Then uses OpenCV to capture it."""

    video = pafy.new(url)
    best = video.getbest(preftype="mp4")

    capture = cv2.VideoCapture(best.url)

    return capture


def jellyFishMethod():
    """Actually performs the analysis of the video to create the package for the users.
    It calls all neccesary functions."""

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

        count, section = 0, 0

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
                # 1) Create a decimal equivalent of the section we are in (example: 8 = .8)
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
    """A more general apporach to create random numbers from different videos. This simply compares
    two seperate frames."""

    image = 0

    differenceAmount = .3

    frameCount = int(input("How many frames of the video should we analyze? "))
    differenceAmount = getDesiredSensitivity()

    analyze = Analysis()

    FileHandler.createFolder()

    success = True

    capture = fetchCapture(url)

    success, base = capture.read()

    while success and image < frameCount:

        count, section = 0, 0

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

                # These three if statements determine how much each pixel varies between two frames.
                # If the variance is great enough, basically, the difference is saved.
                if comapreTwoPixel(b, baseB) > differenceAmount:
                    # Alter the pixel to denote difference was found
                    alter[x, y, 0] = 255
                    # Create number by adding our section number to the % of the pixels b, g, or r value
                    #Sample : .9       +   (220/255) /10
                    # This would be .9  +   .0852
                    # The result is .9852
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


def getDesiredSensitivity():
    differenceAmount = -1

    while differenceAmount < 0 or differenceAmount > 1:
        differenceAmount = float(input(
            "Enter a decimal value to determine sensitivty: .1 = a little difference would create a number, .8 = a lot of difference would be need to create a number: "))

    return differenceAmount


def comapreTwoPixel(base, next):
    """Returns the difference between two values (0-255). Because of how the number is 
    stored, the value is halved."""
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


if __name__ == "__main__":
    main()
