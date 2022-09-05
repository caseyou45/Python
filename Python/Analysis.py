from math import floor
from random import randint
from FileHandler import saveTextFile


trueRandomDict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
                  5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
pseudoRandomDict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
                    5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

pseudoRandomNumbers = []
trueRandomNumbers = []


def analyze(numbers):
    for i in range(0, len(numbers)):
        n = floor(numbers[i] * 10)
        trueRandomDict[n] += 1

        pr = randint(0, 9)
        pseudoRandomNumbers.append(pr)
        pseudoRandomDict[pr] += 1

    findAverage(numbers)


def findAverage(numbers):
    return sum(numbers) / len(numbers)


def formatAnalysisDocument(numbers):
    message = "Analysis was successful. The process created " + \
        str(len(numbers)) + " random numbers with this distrubution:\n"

    message += "\nRandom Number (rounded) : Amount\n"
    for i in range(len(trueRandomNumbers)):
        message += str(i) + " : " + str(trueRandomNumbers[i]) + "\n"

    message += "\n\nThis can be comapred with Python's pseudo randint function. For the same amount of numbers,\n it created numbers with this distribution: \n"

    message += "\nRandint : Amount\n"
    for i in range(len(trueRandomNumbers)):
        message += str(i) + " : " + str(trueRandomNumbers[i]) + "\n"

    saveTextFile(message)
