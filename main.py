from subject import Subject
from lecture import Lecture
from PDFWriter import PDFWriter
from DBPediaQuery import DBPediaQuery
from question import Question
from os import path
import glob
import rdflib

"""
Parses lecture PDFs, finds every word and their frequency.
    - Writes this information to a CSV file.
    - This only has to be done once for every PDF file, afterwards the program
    - will simply read that same CSV file.
    - The assignment is delivered with already processed PDFs, and their
      matching CSV files. But feel free to add more.
"""

def parsePDF():
    writer = PDFWriter()
    parsePDF = input("Do you want to parse new PDFs to files (y/n)? ")

    while parsePDF.lower() == "y":
        subject_code = input("Subject code: ")
        possible_files = glob.glob('**/*.pdf', recursive=True)
        print("Possible PDF files to read from: ")
        done = False
        while done == False:
            for i, file in enumerate(possible_files):
                print(i, " -- ", file)
            chosen = input("Choose file to read to " + subject_code + " (enter to quit): ")
            if chosen == "":
                done = True
                break
            file = possible_files.pop(int(chosen))
            writer.generate(file, subject_code)
        parsePDF = input("Add PDFs to another subject (y/n)? ")

if __name__ == "__main__":
    parsePDF()

    # freq files are all the CSV files that exist in the folder.
    freq_files = glob.glob('**/*.txt', recursive=True)

    # For now, these are the only subjects added.
    info216 = Subject("Knowledge Graphs", "INFO216")
    info135 = Subject("Advanced Programming", "INFO135")

    # Creating lectures and adding them to the appropriate subjects.
    for file in freq_files:
        lec = Lecture(file)
        if lec.getSubject() == "INFO216":
            info216.addLecture(lec)
        if lec.getSubject() == "INFO135":
            info135.addLecture(lec)

    # Generating the most common words in each subject.
    subjects = [info216, info135]
    for subject in subjects:
        subject.generateWordFrequency()

    print("Which subject do you want to train on?")
    i = 1
    for subject in subjects:
        print(i, subject.getCode())
        i += 1
    answ = int(input("Choose (1-2): "))
    if answ <= len(subjects):
        chosen_subject = subjects[answ-1]
    else:
        print("Wrong input.")

    # Gets the most common words from the chosen subject.
    # These are used to generate questions later.
    input_list = []
    words = chosen_subject.getMostCommonWords(10)
    for word in words:
        input_list.append(word)

    # Taking the words from the subject and querying DBPedia.
    # We get definitions, subjects etc. More explanation in the class.
    print("Querying DBPedia, please hold... ")
    db = DBPediaQuery()
    db.spotlight_annotate(input_list)
    db.generate_definitions()
    db.generate_subcategories()
    subcategories = db.get_subcagetories()
    definitions = db.get_definitions()

    # Generating questions.
    questions = []
    for word, definition in definitions.items():
        questions.append(Question(word, definition))
    for q in questions:
        q.set_subcat(subcategories[q.word])

    answ = "..."
    while answ != "":
        print()
        print("What type of questions do you want? Press enter to quit.")
        print("1. Multiple Choice.")
        print("2. Definitions.")
        print("3. Sub-category guessing.")
        answ = input("Answer (1-3): ")
        if answ == "":
            print("Thanks for now!")
        else:
            answ = int(answ)

        if answ == 1:
            for q in questions:
                q.multiple_choice(all_word_defs_global=definitions)
        elif answ == 2:
            for q in questions:
                q.guess_definition()
        elif answ == 3:
            for q in questions:
                q.guess_subjects(list(subcategories))
        elif answ == "":
            break
        else:
            print("You did not choose one of the options.")