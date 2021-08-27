import pdfminer
import os
import io
import nltk

"""
Lectures control one CSV file each and reads
the information from the file, stores it in a
dictionary which can then later be used by
the subject-class.
"""
class Lecture:
    num = 0
    def __init__(self, filename):
        self.subject = ""
        self.num = Lecture.num
        self.name = "No name."
        Lecture.num += 1
        self.word_list = []
        self.word_frequency = {}
        self.generateLists(filename)

    def getSubject(self):
        return self.subject

    def getName(self):
        return self.name

    def getNum(self):
        return self.num

    def getWordFrequency(self):
        return self.word_frequency

    # Gets the most common words from its own file.
    def getMostCommonWords(self, n):
        if len(self.word_frequency) == 0:
            print("Generate word frequency first.")
            return
        sort = {k: v for k, v in sorted(self.word_frequency.items(), key=lambda item: item[1], reverse=True)}
        tmp = {}
        for word, frequency in sort.items():
            tmp[word] = frequency
            n -= 1
            if n == 0:
                break
        return tmp

    """
    Reads the CSV file and generates lists from the information.
    """
    def generateLists(self, filename):
        file = open(filename, "r", encoding="UTF-8")
        lst = list(file)
        file.close()
        # First word in the file is the subject.
        self.subject = lst[0].split(",")[0]

        tmp = open("stopwords.txt", "r", encoding="UTF-8")
        stopwords = tmp.read().split()
        tmp.close()

        for line in lst:
            line = line.strip()
            if len(line.split(",")) != 2:
                continue
            word, frequency = line.split(",")
            if word not in stopwords:
                self.word_frequency[word] = int(frequency)