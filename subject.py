import os
import io

"""
This class keeps controll of all the lectures.
It can iterate over lectures and count their words
to get the total sum of all words in the subject.
"""

class Subject:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.lectures = []
        self.word_frequency = {}

    def getName(self):
        return self.name

    def getLectures(self):
        return self.lectures

    def getCode(self):
        return self.code

    # Adds lecture to its own list of lectures.
    def addLecture(self, lecture):
        self.lectures.append(lecture)

    def getWordFrequency(self):
        return self.word_frequency

    def showLectures(self):
        for lecture in self.lectures:
            print("ID", lecture.getNum(), lecture.getName())

    # get the N most common words.
    # returns a dict with key=word, value=freq
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
    Loops through all the lectures store in its list.
    Counts every word from the lectures into one big list
    that contains the total sum of all words in the subject.
    """
    def generateWordFrequency(self):
        tmp = {}
        if len(self.lectures) == 0:
            print("No lectures to generate frequencies from.")
        for lecture in self.lectures:
            lectures_words = lecture.getWordFrequency()
            for keyword in lectures_words:
                if keyword not in tmp:
                    tmp[keyword] = lectures_words[keyword]
                else:
                    tmp[keyword] += lectures_words[keyword]
        self.word_frequency = tmp

