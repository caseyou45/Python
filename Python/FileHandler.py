import cv2
import os


def createFolder():
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except:
        print('Error: Creating directory of data')

    print("Folder Created")


def saveImage(frame, frameCount):

    name = './data/frame' + str(frameCount) + '.jpg'
    print('Creating...' + name)

    cv2.imwrite(name, frame)


def saveNumberFile(numbers):
    try:
        with open('data/numbers.txt', 'w') as f:
            for number in numbers:
                f.write(str(number) + "\n")

    except FileNotFoundError:
        print("The 'data' directory does not exist")
