import random
import tkinter as tk
from tkinter import messagebox

class WordleGame():
    def __init__(self):
        self.guess_count = 0
        self.validwords = []
        self.validguesswords = []
        self.blacklistedletters = []
        self.greenlistedletters = [' ' for _ in range(5)]
        self.yellowlistedletters = []
        self.validwordsremaining = []
        self.get_random_secret_word()
        self.run_game()

        
    def get_random_secret_word(self):
        with open('wordlewinners.txt') as f:
            validwords = ([*map(str.strip, f.readlines())])
            self.validwords = validwords
            self.validwordsremaining = validwords.copy() 
            self.secretword = random.choice(validwords)
        with open('wordle_words.txt') as file:
            self.validguesswords = ([*map(str.strip, file.readlines())])


    def user_guess(self):
        guess = input("Guess a word: ")
        if guess in self.validguesswords and len(guess) == 5:
            self.return_colours(guess)
        else:
            print("invalid guess")
        return guess

    def return_colours(self,guess):
        colours = []
        for idx, letter in enumerate(guess):
            if self.secretword[idx] == letter:
                colours.append('green')
                self.greenlistedletters[idx] = letter
            elif letter in self.secretword:
                colours.append('yellow')
                self.yellowlistedletters.append(letter)
            else:
                colours.append('black')
                self.blacklistedletters.append(letter)
        print(f"     {guess[0].upper()}       {guess[1].upper()}        {guess[2].upper()}        {guess[3].upper()}        {guess[4].upper()}")
        print(colours)
        #print(self.greenlistedletters)
        return(colours)
    
    def return_colours_hypo(self,guess):
        colours = []
        for idx, letter in enumerate(guess):
            if self.secretword[idx] == letter:
                colours.append('green')
                self.hypogreenlistedletters[idx] = letter
            elif letter in self.secretword:
                colours.append('yellow')
                self.hypoyellowlistedletters.append(letter)
            else:
                colours.append('black')
                self.hypoblacklistedletters.append(letter)
        #print(self.greenlistedletters)
        return(colours)
    
    
    def run_game(self):
        print(f"total valid  words : {len(self.validwords)}")
        while self.guess_count < 6:
            print(f"Guess {self.guess_count + 1}")
            if self.guess_count > 0:
                hypothetical_results = self.bestword()
            guess = self.user_guess()
            if guess in self.validguesswords and len(guess) == 5:
                self.validwordsleft()
                if self.guess_count > 0:
                    result = [(rank + 1, length, word) for rank, (length, word) in enumerate(hypothetical_results) if word == guess]
                    # Check if the result list is not empty
                    if result:
                        rank, length, word = result[0]
                        print(f"Rank of your guess '{guess}': {rank}")
                    else:
                        print(f"Your had enough information to know that {guess} was not the correct word")
                if guess == self.secretword:
                    print(f"you won in {self.guess_count + 1} moves")
                    break
                else:
                    if self.guess_count == 6:
                        print(f"bad luck! The word was {self.secretword}")
                    else:
                        self.guess_count += 1
        

    def validwordsleft(self):
        #Create copy of the list for iteration
        for word in self.validwordsremaining[:]:
            for letter in self.blacklistedletters:
                try:
                    if letter in word:
                        self.validwordsremaining.remove(word)
                except: 
                    pass
            for letter in self.yellowlistedletters:
                try:
                    if not letter in word:
                        self.validwordsremaining.remove(word)
                except: 
                    pass
            for idx, letter in enumerate(self.greenlistedletters):
                if letter != ' ':
                    try:
                        if self.greenlistedletters[idx] != word[idx]:
                            self.validwordsremaining.remove(word)
                    except:
                        pass
        print(f"number of valid words remaining: {len(self.validwordsremaining)}")
        #if len(self.validwordsremaining) < 20:
            #print(f"Less than 20 words remaining:  {(self.validwordsremaining)}")

    def validwordsleft_hypo(self):
        #Create copy of the list for iteration

        for word in self.hypotheticalvalidwordsremaining[:]:
            for letter in self.hypoblacklistedletters:
                try:
                    if letter in word:
                        self.hypotheticalvalidwordsremaining.remove(word)
                except: 
                    pass
            for idx, letter in enumerate(self.hypogreenlistedletters):
                if letter != ' ':
                    try:
                        if self.hypogreenlistedletters[idx] != word[idx]:
                            self.hypotheticalvalidwordsremaining.remove(word)
                    except:
                        pass

    def bestword(self):
        
        hypothetical_results = []

        for word in (self.validwordsremaining):
            self.hypotheticalvalidwordsremaining = self.validwordsremaining.copy()
            self.hypoblacklistedletters = self.blacklistedletters.copy()
            self.hypogreenlistedletters = self.greenlistedletters.copy()
            self.hypoyellowlistedletters = self.yellowlistedletters.copy()

            hypothetical_guess = word
            self.return_colours_hypo(hypothetical_guess)
            self.validwordsleft_hypo()

            lenh = len(self.hypotheticalvalidwordsremaining)

            hypothetical_results.append((lenh,word))
        hypothetical_results.sort()
        return hypothetical_results
        
        




mygame = WordleGame()


