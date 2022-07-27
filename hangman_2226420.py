# Coding Challenge 4, hangman.py
# Name: Subinkhadka
# Student No: np03cs4s220145
# Hangman Game

import random
import sys
from string import ascii_lowercase

WORDLIST_FILENAME = "words.txt"

def choose_random_word(all_words):
 """choose random words from the list of words"""
 return random.choice(all_words)
responses = [
 "I am thinking of a word that is {0} letters long",
 "Congratulations, you won!",
 "Your total score for this game is: {0}",
 "Sorry, you ran out of guesses. The word was: {0}",
 "You have {0} guesses left.",
 "Available letters: {0}",
 "Good guess: {0}",
 "Oops! That letter is not in my word: {0}",
 "Oops! You've already guessed that letter: {0}",
]

secrect_word = []
def load_words():
    try:
        print("Loading word from the file: ",WORDLIST_FILENAME)
        file = open(WORDLIST_FILENAME,"r")
        wordlist = file.read().split(' ')
        print(len(wordlist)," words got load")
        print("Welcome to Hangman Ultimate Edition")
        file.close()
        return wordlist
    except Exception as ex:
        print(ex)

def is_word_guessed(word, letters_guessed):
    for char in word:
        if char not in letters_guessed:
            return False
    return True

def get_guessed_word(word, letters_guessed):
    for letter in letters_guessed:
        for i in range(len(word)):
            if word[i] == letter:
                secrect_word[i] = word[i]
    return ''.join(secrect_word)

def get_remaining_letters(letters_guessed):
    remaining_letters = list(ascii_lowercase)
    for letter in letters_guessed:
        remaining_letters.remove(letter)
    return ''.join(remaining_letters)

def is_letter_repeated(letter,letters_guessed):
    if letter in letters_guessed:
        return True
    return False

def is_letter_matched(letter,word):
    if letter in word:
        return True
    return False

def get_score(name):
    lines = read_scores()
    for i in range(len(lines)):
        if name == lines[i][1]:
            return lines[i][0]
    return 0

def save_score(name, score):
    try:
        lines = read_scores()
        pre_score = get_score(name)
        file = open("scores.txt","w")

        if pre_score == 0:
            file.writelines(str(score)+","+str(name)+"\n")
        for i in range(len(lines)):
            if name == lines[i][1]:
                lines[i][0] = score
            file.writelines(str(lines[i][0])+","+str(lines[i][1])+"\n")

        file.close()
    except Exception as ex:
        print(ex)

def hangman(word):
    name = input("Enter you name: ")
    print("I am thinking of a word that is {0} letters long".format(len(word)))
    print("-------------")
    secrect_word.clear()
    for i in range(len(word)):
        secrect_word.append('_ ')
    letters_guessed = []
    wrong_attempts = 0
    max_attempts = 6
    remaining_attempts = max_attempts-wrong_attempts

    while not is_word_guessed(word,letters_guessed) and remaining_attempts > 0:
        print("You have {0} guess left.".format(remaining_attempts))
        print("Available letters:{0}".format(get_remaining_letters(letters_guessed)))

        input_letter = input("Please guess a letter: ").lower()

        if( not input_letter.isalpha() or len(input_letter)!= 1):
            print("Invalid input!! Your guess number is reduced by one")
            print("\n-----------------------\n")
            wrong_attempts += 1
            remaining_attempts = max_attempts - wrong_attempts
            if remaining_attempts == 0:
                print(responses[3].format(word))
            continue

        if is_letter_repeated(input_letter,letters_guessed):
            print(responses[8].format(get_guessed_word(word,letters_guessed)))
            print("\n-----------------------\n")
        else:
            letters_guessed.append(input_letter)
            if is_letter_matched(input_letter,word):
                print(responses[6].format(get_guessed_word(word,letters_guessed)))
                print("\n-----------------------\n")
                if is_word_guessed(word,letters_guessed):
                    print(responses[1])
                    current_score = remaining_attempts * len(set(word))
                    previous_score = (int)(get_score(name))
                    print(responses[2].format(current_score))
                    if current_score > previous_score:
                        option = input("A new personal best! Would you like to save your score(y/n): ").lower()
                        if option == "y":
                            save_score(name,current_score)
                            print("Ok, your score has been saved.")
                        else:
                            print("Your score has not been saved.")
            else:
                print(responses[7].format(get_guessed_word(word,letters_guessed)))
                print("\n-----------------------\n")
                if input_letter in []:
                    wrong_attempts += 2
                else:
                    wrong_attempts += 1
                remaining_attempts = max_attempts-wrong_attempts
                if remaining_attempts == 0:
                    print(responses[3].format(word))

def conditions():
    print("Do you want to play (p), view the leaderboard (l) or quit (q): ")
    option = input()
    return option.lower()

def read_scores():
    lines = []
    file = open("scores.txt","r")
    for line in file:
        lines.append(line.strip('\n').split(','))
    file.close()
    return lines

def view_leaderboard():
    lines = read_scores()
    print("Score Name")
    print("--------------------------------")
    for i in range(len(lines)):
        print(lines[i][0]," ",lines[i][1])

def main():
    print()
    wordlist = load_words()
    option = conditions()
    if option == "p":
        word = choose_random_word(wordlist)
        hangman(word)

    elif option == "l":
        view_leaderboard()

    elif option == "q":
        print("Thanks for playing, goodbye!")
        sys.exit()
    else:
        print("Wrong Input !, Try agian")
main()

# Driver function for the program
if __name__ == "__main__":
    main()
