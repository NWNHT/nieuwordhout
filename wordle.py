

# Process:
# Read both files
# Select a word

# While loop until guesses > 6 or quit
# Request guess
# Parse guess
#   if n in answer[position] - green
#   elif n in answer - yellow

# Print result
# Print history or words along with colour blocks
# If they are all green then the person has won

import random
import string

def getAnswer(transparent):
    # read answers from validAnswer.txt, quit if unsuccessful
    try:
        fh = open('validAnswer.txt')
        words = fh.read().split()
        print("Read " + str(len(words)) + " valid answers and selected one.")

        answer = random.choice(words).upper()

        if transparent:
            print("The answer is " + answer + ".")

        return answer
    except:
        print("Cannot read validAnswer.txt.")
        quit()


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


def getGuess(validGuesses):
    # Request and clean a guess from the user, return guess
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
        if not guess in validGuesses:
            print("Not a valid word, please guess again.")
            continue

        return guess


def parseGuess(guess, answer, letters, transparent):
    # Parse the current guess and return the current guess string
    outputString = ''
    for (i, c) in enumerate(guess):

        if c in letters['unusedLetters']: letters['unusedLetters'].remove(c)

        if c == answer[i]:
            outputString = outputString + '\U0001F7E9'
            letters['greenLetters'].append(c)
        elif c in answer:
            outputString = outputString + '\U0001F7E8'
            letters['yellowLetters'].append(c)
        else:
            outputString = outputString + '\U00002B1B'
            letters['greyLetters'].append(c)

    return (outputString + "  " + guess + '\n', letters)


def cleanLetters(letters):
    # Remove duplicates and alphabetize the letters dictionary
    letters['greenLetters'] = sorted(list(set(letters['greenLetters'])))
    letters['yellowLetters'] = sorted(list(set(letters['yellowLetters'])))
    letters['greyLetters'] = sorted(list(set(letters['greyLetters'])))

    return letters


def main():
    # Transparency flag
    transparency = True
    verbose = True

    # Read files and select an answer
    validGuesses = getValidGuesses()
    answer = getAnswer(transparency)

    # Initialize Loop
    remainingGuesses = 6
    prettyPrintString = '\n'
    letters = {'unusedLetters': [n for n in string.ascii_uppercase], 'greenLetters': [], 'yellowLetters': [], 'greyLetters': []}

    print("Welcome to Nieuwordhout, type guesses below and type 'quit' at any time to exit.")

    while remainingGuesses:

        # Get guess from player
        guess = getGuess(validGuesses)

        # Parse the word for matches, clean the letters dictionary
        (guessLine, letters) = parseGuess(guess, answer, letters, transparency)
        letters = cleanLetters(letters)
        prettyPrintString += guessLine

        # Iterate guess counter
        remainingGuesses -= 1

        # Print results if correct, else print status
        if guess == answer:
            print("You guessed correctly, here are your results:")
            print("Nieuwordhout " + str(6 - remainingGuesses) + "/6" + prettyPrintString)
            quit()
        else:
            print("Nieuwordhout" + prettyPrintString)
            if verbose:
                print('Available Letters:\t' + " ".join(letters['unusedLetters']))
                print('Green Letters:\t\t' + " ".join(letters['greenLetters']))
                print('Yellow Letters:\t\t' + " ".join(letters['yellowLetters']))
                print('Incorrect Letters:\t' + " ".join(letters['greyLetters']))
                print('\n')


    # If the number of guesses runs out then print unsuccessful results
    else:
        print("yikes")
        print("Nieuwordhout X/6" + prettyPrintString)




if __name__ == "__main__":
    main()








