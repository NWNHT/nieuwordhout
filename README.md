# nieuwordhout
Wordle clone + tools

wordle.py is my original wordle clone.

remaining.py will take the answer and the sequence of guesses, returning the possible words after each guess(hardmode assumed)

wordle2.py is a more robust clone and integrates remaining.py to allow for a transparent mode
-h		help
-hardmode	turn on hardmode
-trans		turn on transparency
-words		display the remaining words(requires -trans)
-answer		specify the answer, otherwise random. Word is not checked for suitability.
