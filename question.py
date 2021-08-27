import copy
import random

"""
Question is what is used to create, ask
and retrieve answer of a question.
"""
class Question:
    def __init__(self, word, definition, subcat=None):
        self.word = word
        self.long_definition = definition
        # The first sentence of the definition is the "short" version.
        self.definition = definition.split(".")[0]
        self.sub_cat = subcat

    # Give a list of sub category (subjects)
    def set_subcat(self, s):
        self.sub_cat = s

    # Returns definition, set long to True to get the long version.
    def get_definition(self, long=True):
        if long:
            return self.long_definition
        return self.definition

    def get_word(self):
        return self.word

    """
    Asks multiple choice questions.
    """
    def multiple_choice(self, all_word_defs_global={}):
        print("\n--------------------------------------------------")
        print(f"What does {self.word} mean?")

        # make a copy of the original def dict
        all_word_defs = copy.deepcopy(all_word_defs_global)
        correct_answer = all_word_defs[self.word]

        # remove self.word from all_word_defs
        if self.word in all_word_defs:
            del all_word_defs[self.word]

        # get 2 words randomly from all_word_defs
        def_words = list(all_word_defs.keys())
        # shuffle word in the list randomly
        random.shuffle(def_words)

        # create a list of answers
        def_options = []
        def_options.append(all_word_defs[def_words[0]])
        def_options.append(all_word_defs[def_words[1]])
        def_options.append(correct_answer)
        random.shuffle(def_options)

        correct_answer_number = 0
        possible_answers = {}
        for i in range(3):
            possible_answers[i+1] = def_options[i]
            # set value of correct answer number
            if def_options[i] == correct_answer:
                correct_answer_number = i + 1

        print("Choose the correct answer (1 - 3): \n")
        for i in range(3):
            # possible_answers[i+1][:150] means : print only first 150 characters of the answer
            # you can remove that to print the whole definition
            print("Option {} : \n{}...\n".format(i+1, possible_answers[i+1][:150]))

        # take input until user chooses a valid option
        invalid_user_input = True
        while invalid_user_input:
            option_selected_by_user = input("Answer : ")
            if len(option_selected_by_user) == 0:
                return
            else:
                option_selected_by_user = int(option_selected_by_user)

            if (not (1 <= option_selected_by_user <= 3)):
                print("Please enter a valid option.")
            else:
                # user selected a valid option
                # set it to false so it breaks out of the while loop
                invalid_user_input = False
                if option_selected_by_user == correct_answer_number:
                    print("Correct answer!")
                else:
                    print("Incorrect answer.")
                    print("The correct answer was option: {}".format(correct_answer_number))

    # Guess the definiton of a word.
    def guess_definition(self):
        print("\n--------------------------------------------------")
        print(f"\nWhat is the definition of {self.word}?")
        answ = input("Your answer: ")
        print(f"The right answer is:\n{self.definition}")

    # Creates a list of subcategories, where you have
    # to choose the one that fits into the word the best.
    def guess_subjects(self, all_subjects):
        if len(self.sub_cat) < 0:
            print("Oops! This question only works if you have sub categories.")
            return
        if len(all_subjects) < 2:
            print("Ooops! Too few subjects.")
            return
        print("\n--------------------------------------------------")
        print(f"Which one of these are subcategories of {self.word}?")
        random.shuffle(all_subjects)
        random.shuffle(self.sub_cat)
        correct = self.sub_cat[0]
        options = [correct, all_subjects[0], all_subjects[1]]
        # checking if the answers are equal, and changing them.
        x = 0
        while options[0] == options[1]:
            options[1] = all_subjects[x]
            x += 1
        random.shuffle(options)
        for i in range(0, len(options)):
            print(i+1, options[i])

        answ = input("Answer: ")

        if int(answ) - 1 == options.index(correct):
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was {correct}")






