import random
import string
import argparse

GREEN = '\U0001F7E9'
YELLOW = '\U0001F7E8'
GREY = '\U00002B1B'

# TODO accept arguments


class Guess(object):
    def __init__(self, answer, transparent, validGuesses, validAnswers):
        # self.transparent = transparent

        self.guess = self.requestGuess(validGuesses)
        self.code = self.encode(answer)

        self.remainWords = validGuesses
        self.remainAnswers = validAnswers
        self.filterGuesses()
        self.filterAnswers()
        self.remainWordsLen = len(validGuesses)
        self.remainAnswersLen = len(validAnswers)

    def __str__(self):
        """String representation of Guess"""
        return f"{self.code} {self.guess}"

    def requestGuess(self, validGuesses):
        """Request and filter a guess from the user"""
        while True:
            try:
                guess = input("Please make a guess: ").upper()
            except:
                print("I have no idea what you just tried to type.")
                continue

            # Exit option
            if guess == 'QUIT':
                quit()

            if len(guess) != 5:
                print("Guess was not five letters, please guess again.")
                continue
            if not set(guess).issubset(string.ascii_uppercase):
                print("Guess must contain only letters, please guess again.")
                continue
            if guess not in validGuesses:
                print("Not a valid word, please guess again.")
                continue

            return guess

    def encode(self, answer):
        # Generates guess code from word
        code = ''

        for i in range(5):
            if self.guess[i] == answer[i]:
                code += GREEN
            elif self.guess[i] in answer:
                code += YELLOW
            else:
                code += GREY

        return code

    def filterGuesses(self):
        """Return words that give the same code for guess that 'answer' would"""

        for word in self.remainWords.copy():
            if encode(word, self.guess) != self.code:
                self.remainWords.remove(word)

        self.remainWordsLen = len(self.remainWords)

    def filterAnswers(self):
        """Return answers that give the same code for guess that 'answer' would"""

        for word in self.remainAnswers.copy():
            if encode(word, self.guess) != self.code:
                self.remainAnswers.remove(word)

        self.remainAnswersLen = len(self.remainAnswers)


class Inst(object):
    def __init__(self, definedAnswer, transparent=False, showWords=False, hardMode = True):
        self.transparent = transparent
        self.showWords = showWords
        self.hardmode = hardMode

        self.validGuessMaster = self.getValidGuesses()
        self.validAnswerMaster = self.getValidAnswers()
        self.possibleGuess = self.validGuessMaster
        self.possibleAnswer = self.validAnswerMaster

        self.definedAnswer = definedAnswer
        self.answer = self.getAnswer()
        self.guesses = []
        self.board = ""

        self.remainingGuesses = 6
        self.letters = {'unusedLetters': [n for n in string.ascii_uppercase],
                        'greenLetters': [],
                        'yellowLetters': [],
                        'greyLetters': []}

    def __str__(self):
        """String Representation of Inst"""
        return self.board

    def encode(self):
        """Generate and save code, modify and return letters dict"""
        for (i, c) in enumerate(self.guesses[-1].guess):

            if c in self.letters['unusedLetters']:
                self.letters['unusedLetters'].remove(c)

            if c == self.answer[i]:
                # outputString = outputString + '\U0001F7E9'
                self.letters['greenLetters'].append(c)
            elif c in self.answer:
                # outputString = outputString + '\U0001F7E8'
                self.letters['yellowLetters'].append(c)
            else:
                # outputString = outputString + '\U00002B1B'
                self.letters['greyLetters'].append(c)

        # Clean up the letters after updating
        self.cleanLetters()

    def getGuess(self):
        """Create a Guess object and append to self.guesses, decrement remainingGuesses"""
        if self.hardmode:
            self.guesses.append(Guess(self.answer, self.transparent, self.possibleGuess, self.possibleAnswer))
        else:
            self.guesses.append(Guess(self.answer, self.transparent, self.possibleGuess.copy(), self.possibleAnswer.copy()))

        # Update the board and decrement the remaining guesses
        self.remainingGuesses = self.remainingGuesses - 1
        self.updateBoard()

    def updateBoard(self):
        """Update the board that is printed to the player, depends on transparency and hardmode"""
        tempBoard = f"Nieuwordhout {6 - self.remainingGuesses}/6\n"

        if self.transparent:
            # Add guesses
            for g in self.guesses:
                tempBoard += f"{g.__str__()} {str(g.remainWordsLen).rjust(4)} {str(g.remainAnswersLen).rjust(4)}\n"

            # Add letters
            self.encode()
            tempBoard += "\n" + \
                         f'Available Letters:\t {" ".join(self.letters["unusedLetters"])}\n' + \
                         f'Green Letters:\t\t {" ".join(self.letters["greenLetters"])}\n' + \
                         f'Yellow Letters:\t\t {" ".join(self.letters["yellowLetters"])}\n' + \
                         f'Incorrect Letters:\t {" ".join(self.letters["greyLetters"])}\n'

            # If hardmode and showWords are also enabled then print the words left
            if self.hardmode and self.showWords:
                def printWords(wordSet):
                    """Local function to generate pretty word list"""
                    wordStr = ""

                    for word in sorted(list(wordSet)):
                        wordStr += f"{word}, "

                    wordStr += "\b\b"
                    return wordStr

                tempBoard += printWords(self.guesses[-1].remainWords) + '\n'
                tempBoard += printWords(self.guesses[-1].remainAnswers)

        else:
            for g in self.guesses:
                tempBoard += g.__str__() + "\n"

        self.board = tempBoard

    def checkWin(self):
        """Check if the player has won or has run out of guesses, if either, print final board"""
        if self.guesses[-1].guess == self.answer:

            tempBoard = f"Nieuwordhout {6 - self.remainingGuesses}/6{'*' if self.hardmode else ''}\n\n"
            for g in self.guesses:
                tempBoard += f"{g.code}\n"

            print(tempBoard)
            quit()

        if not self.remainingGuesses:
            tempBoard = f"Nieuwordhout X/6\n\n"
            for g in self.guesses:
                tempBoard += f"{g.code}\n"

            print(tempBoard)
            quit()

    def getAnswer(self):
        """read answers from validAnswer.txt, quit if unsuccessful"""

        if self.definedAnswer is not None:
            print(f"The defined answer is {self.definedAnswer.upper()}")
            return self.definedAnswer.upper()

        try:
            fh = open('validAnswer.txt')
            words = fh.read().split()

            answer = random.choice(words).upper()
            answer = "SAUTE"

            if self.transparent:
                print("Read " + str(len(words)) + " valid answers and selected one.")
                print("The answer is " + answer + ".")
            else:
                print("Welcome to Nieuwordhout")

            return answer

        except:
            print("Cannot read validAnswer.txt.")
            quit()

    def getValidGuesses(self):
        """read valid guesses from validGuess.txt and validAnswer.txt, quit if unsuccessful"""
        try:
            fhg = open('validGuess.txt')
            validGuesses = set(fhg.read().upper().split())

            fha = open('validAnswer.txt')
            validAnswer = set(fha.read().upper().split())

            totalGuesses = validGuesses | validAnswer

            if self.transparent:
                print("Read " + str(len(totalGuesses)) + " valid guesses.")

            return totalGuesses
        except:
            print("Cannot read validGuess.txt.")
            quit()

    def getValidAnswers(self):
        # read valid answers from validAnswer.txt, quit if unsuccessful
        try:
            fha = open('validAnswer.txt')
            validAnswer = set(fha.read().upper().split())

            if self.transparent:
                print("Read " + str(len(validAnswer)) + " valid answers.")

            return validAnswer
        except:
            print("Cannot read validGuess.txt.")
            quit()

    def cleanLetters(self):
        # Remove duplicates and alphabetize the letters dictionary
        self.letters['greenLetters'] = sorted(list(set(self.letters['greenLetters'])))
        self.letters['yellowLetters'] = sorted(list(set(self.letters['yellowLetters'])))
        self.letters['greyLetters'] = sorted(list(set(self.letters['greyLetters'])))

        # Remove any letters from yellow that are green(caused by duplicates in answer/guess)
        for l in self.letters['yellowLetters']:
            if l in self.letters['greenLetters']:
                self.letters['yellowLetters'].remove(l)


def encode(answer, guess):
    # Generates guess code from word
    code = ''

    for i in range(5):
        if guess[i] == answer[i]:
            code += GREEN
        elif guess[i] in answer:
            code += YELLOW
        else:
            code += GREY

    return code


def parseArguments():
    """Parse arguments"""
    parser = argparse.ArgumentParser(prog='Wordle',
                                     description='Play Wordle')

    parser.add_argument('-trans',
                        help='turn on transparency(show remaining words)',
                        action='store_true')

    parser.add_argument('-words',
                        help='show remaining words and answers',
                        action='store_true')

    parser.add_argument('-hardmode',
                        help='turn on hard mode',
                        action='store_true')

    parser.add_argument('-answer',
                        help='define an answer or leave blank for random',
                        action='store')

    return parser.parse_args()


def main():
    args = parseArguments()

    game = Inst(args.answer, args.trans, args.words, args.hardmode)

    while True:
        # Call for guess
        game.getGuess()

        # Check if player won or lost
        game.checkWin()

        # Print board
        print(game)



if __name__ == "__main__":
    main()
