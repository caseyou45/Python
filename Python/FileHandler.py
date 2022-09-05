import cv2
import os


def createFolder():
    try:
        if not os.path.exists('random'):
            os.makedirs('random')
    except:
        print("Error: Creating directory of 'random'")

    print("...Creating directory 'random' to store information")


def saveImage(frame, frameCount):

    try:
        name = './random/dataframe' + str(frameCount) + '.jpg'
        print("...Saving image " + name + " (image used to create the numbers)")

        cv2.imwrite(name, frame)
    except:
        print("Error: Something happened making " + name)


def saveNumberFile(numbers):
    print("...Saving txt file 'numbers,' which contains the random numbers")

    try:
        with open('random/numbers.txt', 'w') as f:
            for number in numbers:
                f.write(str(number) + "\n")

    except FileNotFoundError:
        print("The 'random' directory does not exist")


def saveTextFile(message):
    print("...Saving txt file 'analysis,' which explores the numbers generated")

    try:
        with open('random/analysis.txt', 'w') as f:
            f.write(message)

    except FileNotFoundError:
        print("The 'random' directory does not exist")
