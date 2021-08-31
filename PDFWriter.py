import pdfminer
import os
import io
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import nltk

# Classe som leser PDF filer, parser innholdet
# og lagrer det på en ny fil med frekvensen av hvert
# ord i pdf filen.

"""
This class parses PDF files.
It then cleans the words, and counts how many
times the words was encountered (frequency.)
Writes the word and the frequency to a CSV file.
"""

class PDFWriter:
    def __init__(self):
        self.word_list = []
        self.word_frequency = {}

    def generate(self, filename, subject):
        self._generate_list_from(filename)
        self._generate_word_frequency()
        self.writeFrequencyToFile(subject)

    """
    Reads the PDF file and sets self.word to a
    list of all the cleaned words in the pdf
    """
    def _generate_list_from(self, filename):
        tmp = self._parse_pdf(filename)
        words = set(nltk.corpus.words.words())
        tmp =  " ".join(w for w in nltk.wordpunct_tokenize(tmp) if w.lower() in words or w.isalpha())
        tmp = list(tmp.split("\n"))
        self.word_list = tmp

    """
    Counts the words of self.word_list and adds them
    to a dictionary, where the key is the word
    and the value is the frequency.
    """
    def _generate_word_frequency(self):
        if len(self.word_list) == 0:
            print("No word list to generate from.")
            print("Generate word list first.")
        else:
            freq = {}
            for line in self.word_list:
                words = line.split(" ")
                for word in words:
                    if len(word) == 1:
                        continue
                    word = word.lower()
                    freq[word] = 1 if word not in freq else freq[word]+1
            self.word_frequency = freq

    """
    Code from the PDFMiner documentation.
    Reads the PDF and returns the content as a string.
    """
    def _parse_pdf(self, filename):
        output_string = StringIO()
        with open(filename, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
        return output_string.getvalue()

    """
    Reads the created dictionary into a CSV file.
    """
    def writeFrequencyToFile(self, subject):
        lecture_name = input("Lecture name (can be anything): ")
        directory = "freq " + subject + "/"
        filename = "lecture" + lecture_name + " freq.txt"
        path = directory + filename
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = io.open(path, "w", encoding="UTF-8")
        # første ordene i filen er emnet og navnet.
        file.write(subject + "," + lecture_name + "\n")
        for word, frequency in self.word_frequency.items():
            file.write(word + ", " + str(frequency) + "\n")

        file.close()