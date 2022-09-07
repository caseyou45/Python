from math import floor
from random import randint
from FileHandler import saveTextFile


class Analysis:
    def __init__(self, pseudoRandomNumbers=[], trueRandomNumbers=[],
                 trueRandomDict={0: 0, 1: 0, 2: 0, 3: 0,
                                 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
                 pseudoRandomDict={0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}):

        self.setPseudoRandomNumbers(pseudoRandomNumbers)
        self.setTrueRandomNumbers(trueRandomNumbers)
        self.setTrueRandomDict(trueRandomDict)
        self.setPseudoRandomDict(pseudoRandomDict)
        self._error = ""

    def addPseudoRandomNumber(self, number):
        self._pseudoRandomNumbers.append(number)

    def setPseudoRandomNumbers(self, numbers):
        self._pseudoRandomNumbers = numbers

    def addTrueRandomNumbers(self, number):
        self._trueRandomNumbers.append(number)

    def setTrueRandomNumbers(self, numbers):
        self._trueRandomNumbers = numbers

    def getTrueRandomNumbers(self):
        return self._trueRandomNumbers

    def modifyTrueRandomDict(self):
        for i in range(0, len(self._trueRandomNumbers)):
            n = floor(self._trueRandomNumbers[i] * 10)
            self._trueRandomDict[n] += 1

    def setTrueRandomDict(self, dict):
        self._trueRandomDict = dict

    def modifyPseudoRandomDict(self):
        for i in range(0, len(self._pseudoRandomNumbers)):
            self._pseudoRandomDict[self._pseudoRandomNumbers[i]] += 1

    def setPseudoRandomDict(self, dict):
        self._pseudoRandomDict = dict

    def getTrueRandomAverage(self):
        return sum(self._trueRandomNumbers) / len(self._trueRandomNumbers)

    def getPseudoRandomAverage(self):
        return sum(self._pseudoRandomNumbers) / len(self._pseudoRandomNumbers)

    def formatAnalysisDocument(self):
        self.modifyPseudoRandomDict()
        self.modifyTrueRandomDict()
        message = "Analysis was successful. The process created " + \
            str(len(self._trueRandomNumbers)) + \
            " random numbers with this distrubution:\n"

        message += "\nRandom Number (rounded) : Amount\n"
        for i in range(10):
            message += str(i) + " : " + str(self._trueRandomDict[i]) + "\n"

        message += "\n\nThis can be comapred with Python's pseudo randint function. For the same amount of numbers,\n it created numbers with this distribution: \n"

        message += "\nRandint : Amount\n"
        for i in range(10):
            message += str(i) + " : " + str(self._pseudoRandomDict[i]) + "\n"

        saveTextFile(message)
