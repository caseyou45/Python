from math import floor
from random import randint
from typing import Dict, List
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

    def fullResetOfValues(self):
        '''Reset everything to init values'''
        self._trueRandomDict = self._trueRandomDict.fromkeys(
            self._trueRandomDict, 0)
        self._pseudoRandomDict = self._pseudoRandomDict.fromkeys(
            self._pseudoRandomDict, 0)
        self._pseudoRandomNumbers.clear()
        self._trueRandomNumbers.clear()

    def addPseudoRandomNumber(self, number: int):
        self._pseudoRandomNumbers.append(number)

    def setPseudoRandomNumbers(self, numbers: List[int]):
        self._pseudoRandomNumbers = numbers

    def addTrueRandomNumbers(self, number: int):
        self._trueRandomNumbers.append(number)

    def setTrueRandomNumbers(self, numbers: List[float]):
        self._trueRandomNumbers = numbers

    def getTrueRandomNumbers(self) -> List[float]:
        return self._trueRandomNumbers

    def tabulateTrueRandomDict(self):
        for i in range(0, len(self._trueRandomNumbers)):
            n = floor(self._trueRandomNumbers[i] * 10)
            self._trueRandomDict[n] += 1

    def setTrueRandomDict(self, dict: Dict[int, int]):
        self._trueRandomDict = dict

    def tabulatePseudoRandomDict(self):
        for i in range(0, len(self._pseudoRandomNumbers)):
            self._pseudoRandomDict[self._pseudoRandomNumbers[i]] += 1

    def setPseudoRandomDict(self, dict: Dict[int, int]):
        self._pseudoRandomDict = dict

    def getTrueRandomAverage(self) -> float:
        return sum(self._trueRandomNumbers) / len(self._trueRandomNumbers)

    def getPseudoRandomAverage(self) -> float:
        return sum(self._pseudoRandomNumbers) / len(self._pseudoRandomNumbers)

    def formatAnalysisDocument(self):
        self.tabulatePseudoRandomDict()
        self.tabulateTrueRandomDict()
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
