from random import randint
from types import NoneType
import pafy
import cv2
import FileHandler
from AnalysisClass import Analysis
from typing import Any


def getChoice() -> int:
    """Prompts users to choose an options and returns that numerical value. """
    choice = -1

    while choice < 0:
        try:

            choice = int(
                input("\n1) Monterey Bay Jellyfish  \n2) Tokyo-Shinjuku Street  \n3) Enter URL \n4) Reset Saved Numbers\n0) Quit \n\nChoose generation method: "))

            if choice < 0:
                print("Not a valid choice")

        except ValueError:
            print("Illegal Input: Numbers only")

    return choice


def fetchCapture(url: str):
    """Uses pafy to obtain the video from the URL. Then uses OpenCV to capture it."""

    try:
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")

        capture = cv2.VideoCapture(best.url)

    except:
        return NoneType

    return capture


def jellyFishMethod(analyze: Analysis):
    """Actually performs the analysis of the video to create the package for the users.
    It calls all neccesary functions."""

    frameCount = int(input("How many frames of the video should we analyze? "))
    imageCount = 0

    success = True

    capture = fetchCapture("https://www.youtube.com/watch?v=pT9_HJr-nso")

    createNumberTool = memoCreateRamdomNumber(createRandomNumber)

    FileHandler.createFolder()

    if capture == NoneType:
        success = False
        print("\nSomething went wrong with the video...\n")

    while success and imageCount < frameCount:

        success, frame = capture.read()

        if success == False:
            print("\nSomething went wrong with the captrue...\n")

        else:

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

                        n = createNumberTool(section, r)

                        analyze.addTrueRandomNumbers(n)
                        analyze.addPseudoRandomNumber(randint(0, 9))

            FileHandler.saveImage(frame, imageCount)
            imageCount += 1

    if success:
        FileHandler.saveNumberFile(analyze.getTrueRandomNumbers())
        analyze.formatAnalysisDocument()


def liveCamGeneral(url: str, analyze: Analysis):
    """A more general apporach to create random numbers from different videos. This simply compares
    two seperate frames. Randomness, then, is driven by how much the frames have changed."""

    differenceAmount = .3
    imageCount = 0

    frameCount = int(input("How many frames of the video should we analyze? "))
    differenceAmount = getDesiredSensitivity()

    FileHandler.createFolder()

    success = True

    capture = fetchCapture(url)

    # Sets up the memoization for methods
    comaparisonTool = memoCompareTwoPixels(comapreTwoPixels)
    createNumberTool = memoCreateRamdomNumber(createRandomNumber)

    if capture == NoneType:
        success = False
        print("\nSomething went wrong with the video...\n")

    else:
        # Since this works by comparing frames. This sets up the "base" frame to start the comparison
        success, base = capture.read()

    while success and imageCount < frameCount:

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
                if comaparisonTool(b, baseB) > differenceAmount:
                    # Alter the pixel to denote difference was found
                    alter[x, y, 0] = 255
                    # Create number by adding our section number to the % of the pixels b, g, or r value
                    # Sample : .9       +   (220/255) /10
                    # This would be .9  +   .0852
                    # The result is .9852
                    n = createNumberTool(section, b)
                    analyze.addTrueRandomNumbers(n)
                    analyze.addPseudoRandomNumber(randint(0, 9))

                if comaparisonTool(g, baseG) > differenceAmount:
                    alter[x, y, 1] = 255

                    n = createNumberTool(section, g)
                    analyze.addTrueRandomNumbers(n)
                    analyze.addPseudoRandomNumber(randint(0, 9))

                if comaparisonTool(r, baseR) > differenceAmount:
                    alter[x, y, 2] = 255

                    n = createNumberTool(section, r)
                    analyze.addTrueRandomNumbers(n)
                    analyze.addPseudoRandomNumber(randint(0, 9))

        base = frame

        FileHandler.saveImage(alter, imageCount)
        imageCount += 1

    if success:
        FileHandler.saveNumberFile(analyze.getTrueRandomNumbers())
        analyze.formatAnalysisDocument()


def memoCreateRamdomNumber(f: Any) -> Any:
    """Implements memoization for the random number function"""

    memo = {}

    def helper(section, rgbValue):

        strOfInputs = str(section) + str(rgbValue)

        if strOfInputs not in memo:
            memo[strOfInputs] = f(section, rgbValue)

        return memo[strOfInputs]

    return helper


def createRandomNumber(section: int, rgbValue: int) -> float:
    """Adds the section to the rgb value as a percentage"""
    return (section / 10) + ((rgbValue / 255)/10)


def getDesiredSensitivity() -> float:
    differenceAmount = -1

    while differenceAmount < 0 or differenceAmount > 1:
        differenceAmount = float(input(
            "Enter a decimal value to determine sensitivty: .1 = a little difference would create a number, .8 = a lot of difference would be need to create a number: "))

    return differenceAmount


def memoCompareTwoPixels(f: Any) -> Any:
    """Implements memoization for the pixel comparision function"""
    memo = {}

    def helper(base, next):

        strOfInputs = str(base) + str(next)

        if strOfInputs not in memo:
            memo[strOfInputs] = f(base, next)

        return memo[strOfInputs]

    return helper


def comapreTwoPixels(base: int, next: int) -> float:
    """Returns the difference between two values (0-255). Because of how the number is 
    stored, the value is halved."""

    difference = (base / 2) - (next / 2)
    num = abs(difference) / (255 / 2)

    return num


def getURLIDFromUser() -> str:
    url = input(
        "Enter ID of Youtube URL of livestream for analysis: ")
    return url


def main():
    """Main method to handle choices. Analysis object is created to be passed to methods."""
    analyze = Analysis()

    # Counter for number of images analyzed
    choice = getChoice()

    while choice != 0:

        if choice == 1:
            jellyFishMethod(analyze)

        if choice == 2:
            liveCamGeneral(
                "https://www.youtube.com/watch?v=RQA5RcIZlAM", analyze)

        if choice == 3:
            urlIDFromUser = getURLIDFromUser()
            urlIDFromUser = "https://www.youtube.com/watch?v=" + urlIDFromUser
            liveCamGeneral(urlIDFromUser, analyze)

        if choice == 4:
            analyze.fullResetOfValues()

        choice = getChoice()


if __name__ == "__main__":
    main()
