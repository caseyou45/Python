import cv2
import os
from typing import Any, List


def createFolder():
    try:
        if not os.path.exists('result'):
            os.makedirs('result')
    except:
        print("Error: Creating directory of 'result'")

    print("...Creating directory 'result' to store information")


def saveImage(frame: Any, frameCount: int):

    try:
        name = './result/dataframe' + str(frameCount) + '.jpg'
        print("...Saving image " + name + " (image used to create the numbers)")

        cv2.imwrite(name, frame)
    except:
        print("Error: Something happened making " + name)


def saveNumberFile(numbers: List[float]):
    print("...Saving txt file 'numbers,' which contains the result numbers")

    try:
        with open('result/numbers.txt', 'w') as f:
            for number in numbers:
                f.write(str(number) + "\n")

    except FileNotFoundError:
        print("The 'result' directory does not exist")


def saveTextFile(message: str):
    print("...Saving txt file 'analysis,' which explores the numbers generated")

    try:
        with open('result/analysis.txt', 'w') as f:
            f.write(message)

    except FileNotFoundError:
        print("The 'result' directory does not exist")
