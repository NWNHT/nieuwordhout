# nieuwordhout
Wordle clone + tools

### Wordle.py
wordle.py is my original wordle clone.

remaining.py will take the answer and the sequence of guesses, returning the possible words after each guess(hardmode assumed)

### Wordle2.py
wordle2.py is a more robust clone and integrates remaining.py to allow for a transparent mode.  It has the options as listed below:

-h		help

-hardmode	turn on hardmode

-trans		turn on transparency

-words		display the remaining words(requires -trans)

-answer		specify the answer, otherwise random. Word is not checked for suitability. (Ex: `-answer PRIME`)
