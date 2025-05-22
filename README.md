Wordle-Solver 🧩
Wordle-Solver is a simple command-line tool that helps you solve the popular word game WORDLE. It’s especially helpful for those who find Wordle challenging and want a bit of assistance without spoiling the fun!

🎯 What Is Wordle-Solver?
Wordle-Solver is a helper tool designed to suggest the best next word to try in Wordle. It can be used with:

The original Wordle game

Unlike the original game, it uses a larger word list, which means it can handle many versions of Wordle, not just the official one.

Wordle-Solver runs in the command line. To use it:

Play Wordle normally and make a guess.

Convert the color result into symbols:

_ for gray (letter not in word)

? for yellow (letter in word, wrong spot)

+ for green (correct letter, correct spot)

🔍 How Does It Work?
Wordle-Solver uses probability and feedback to figure out the best possible words to try next. Here’s how it works:

You enter the word you tried and the result you got (colors from Wordle).

Wordle-Solver uses that feedback to narrow down the list of possible words.

It suggests a new word that is most likely to give you useful feedback next.

In the early tries, it might suggest words with common letters—even if they aren’t the right word—because those guesses help eliminate more options.

🧠 Example
Say you guessed the word opera and Wordle gave you the following feedback:

o – not in the word (gray)

p – in the word, wrong spot (yellow)

e – in the right spot (green)

r – in the word, wrong spot (yellow)

a – not in the word (gray)

In Wordle-Solver, you’d enter this as:
entered: opera
try:_?+?_
Then it might respond:

Suggested words (from simple word list):
        press
You can then try press in Wordle and repeat the process.

Word not accepted by Wordle?
Wordle only allows words from its own word list, so sometimes Wordle-Solver might suggest a word that Wordle doesn’t accept.