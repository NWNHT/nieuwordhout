import string

# Program to take the answer, take your guesses, and print the remaining words


GREEN = '\U0001F7E9'
YELLOW = '\U0001F7E8'
GREY = '\U00002B1B'

def requestInput(ipt, validGuesses):
    # General function to request either answer or guess from user
    # Exit option
    if ipt == 'QUIT':
        quit()

    if len(ipt) != 5:
        print("Answer was not five letters, please guess again.")
        return -1
    if not set(ipt).issubset(string.ascii_uppercase):
        print("Answer must contain only letters, please guess again.")
        return -1
    if not ipt in validGuesses:
        print("Not a valid word, please guess again.")
        return -1

    return ipt


def requestAnswer(validGuesses):
    # Request the answer from the user

    while True:
        try:
            ans = input("Please enter the answer: ").upper()

        except:
            print("I have no idea what you just tried to type.")
            continue

        if requestInput(ans, validGuesses) != -1:
            break

    return requestInput(ans, validGuesses)


def requestGuess(validGuesses):
    # Request the answer from the user

    while True:
        try:
            ans = input("Please enter your guess: ").upper()

        except:
            print("I have no idea what you just tried to type.")
            continue

        if requestInput(ans, validGuesses) != -1:
            break

    return requestInput(ans, validGuesses)


def getValidGuesses():
    # read valid guesses from validGuess.txt and validAnswer.txt, quit if unsuccessful
    try:
        fhg = open('validGuess.txt')
        validGuesses = set(fhg.read().upper().split())

        fha = open('validAnswer.txt')
        validAnswer = set(fha.read().upper().split())

        totalGuesses = validGuesses | validAnswer
        print("Read " + str(len(totalGuesses)) + " valid guesses.")

        return totalGuesses
    except:
        print("Cannot read validGuess.txt.")
        quit()


def getValidAnswers():
    # read valid answers from validAnswer.txt, quit if unsuccessful
    try:
        fha = open('validAnswer.txt')
        validAnswer = set(fha.read().upper().split())

        print("Read " + str(len(validAnswer)) + " valid answers.")

        return validAnswer
    except:
        print("Cannot read validGuess.txt.")
        quit()


def filterWords(answer, guess, remainingWords):
    # Return words that give the same code for guess that 'answer' would
    code = encode(answer, guess)

    for word in remainingWords.copy():
        if encode(word, guess) != code:
            remainingWords.remove(word)

    return remainingWords


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

def printWords(wordSet):
    # print
    wordStr = ""

    for word in sorted(list(wordSet)):
        wordStr += f"{word}, "

    wordStr += "\b\b"
    print(wordStr)




def main():

    # Generate list of valid guesses
    validGuesses = getValidGuesses()
    validAnswers = getValidAnswers()
    # Create copies to use for the remaining words
    remainingGuesses = validGuesses.copy()
    remainingAnswers = validAnswers.copy()

    # Get the Wordle answer from user, initialize guesses list
    answer = requestAnswer(validGuesses)
    guesses = []
    guessesStr = ""

    while True:

        # Request a new guess, modify the guess/code list
        guesses.append(requestGuess(validGuesses))
        guessesStr += f"{guesses[-1]}\n{encode(answer, guesses[-1])}\n"

        # Filter the available words using filterWords
        remainingGuesses = remainingGuesses.intersection(filterWords(answer, guesses[-1], validGuesses.copy()))
        remainingAnswers = remainingAnswers.intersection(filterWords(answer, guesses[-1], validAnswers.copy()))

        # Print the results
        print(guessesStr)
        print(f"There are {len(remainingGuesses)} word(s) available and {len(remainingAnswers)} answer(s) available.")
        printWords(remainingGuesses)
        printWords(remainingAnswers)




if __name__ == "__main__":
    main()

