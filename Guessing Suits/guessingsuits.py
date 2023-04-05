import random

gameRunning = True

userInput = "none"

hintCounter = 0
guessCounter = 0
victoryPoints = 0

#Takes the Split version of cards and compares both the numeric value and the suit and returns the comparison
def cardComparison(list1, list2):
    if numericDictionary[list1[0]] < numericDictionary[list2[0]]: #Prime value less than hint value
        print("The value of this card is greater than the first card.")

    elif numericDictionary[list1[0]] == numericDictionary[list2[0]]: #Prime value equal to hint value
        print("The value of this card is the same as the first card.")

    elif numericDictionary[list1[0]] > numericDictionary[list2[0]]: #Prime value greater than hint value
        print("The value of this card is less than the first card.")

    if list1[1] == list2[1]:
        print("These cards are of the same suits.", '\n')

    else:
        print("These cards are of different suits.", '\n')

#Allows for translating of spelled out numbers into numeric values
numericDictionary = {'Ace' : 1, 'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5, 'Six' : 6, 'Seven' : 7, 'Eight' : 8, 'Nine' : 9, 'Ten' : 10, 'Jack' : 11, 'Queen' : 12, 'King' : 13}

#Static List, this list should not be altered by the code
fullList = ["Ace of Spades", "Two of Spades", "Three of Spades", "Four of Spades", "Five of Spades", "Six of Spades",
        "Seven of Spades", "Eight of Spades", "Nine of Spades", "Ten of Spades", "Jack of Spades", "Queen of Spades", "King of Spades",
        "Ace of Diamonds", "Two of Diamonds", "Three of Diamonds", "Four of Diamonds", "Five of Diamonds", "Six of Diamonds",
        "Seven of Diamonds", "Eight of Diamonds", "Nine of Diamonds", "Ten of Diamonds", "Jack of Diamonds", "Queen of Diamonds", "King of Diamonds",
        "Ace of Clubs", "Two of Clubs", "Three of Clubs", "Four of Clubs", "Five of Clubs", "Six of Clubs",
        "Seven of Clubs", "Eight of Clubs", "Nine of Clubs", "Ten of Clubs", "Jack of Clubs", "Queen of Clubs", "King of Clubs",
        "Ace of Hearts", "Two of Hearts", "Three of Hearts", "Four of Hearts", "Five of Hearts", "Six of Hearts",
        "Seven of Hearts", "Eight of Hearts", "Nine of Hearts", "Ten of Hearts", "Jack of Hearts", "Queen of Hearts", "King of Hearts"]

#A coppied version of the deck translated into all lower case for non-case sensitive checking
lowerList = [x.lower() for x in fullList]

#loops until user requests an end
#Contains the start of the game loop, generates a Primary Card, and three Hint Cards
#When restarting returns to this point, to generate a new set of cards and reset the hintCounter
while gameRunning:
    cardStack = fullList
    hintCounter = 0
    guessCounter = 0

    #Generates first card
    primeCard = random.choice(cardStack)
    cardStack.remove(primeCard)
    primeCardSplit = primeCard.split(" of ")

    #Generates the first hint card
    hintCardOne = random.choice(cardStack)
    cardStack.remove(hintCardOne)
    cardOneSplit = hintCardOne.split(" of ")

    #Generates the second hint card
    hintCardTwo = random.choice(cardStack)
    cardStack.remove(hintCardTwo)
    cardTwoSplit = hintCardTwo.split(" of ")

    #Generates the third hint card
    hintCardThree = random.choice(cardStack)
    cardStack.remove(hintCardThree)
    cardThreeSplit = hintCardThree.split(" of ")

    #Generates the fourth hint card
    hintCardFour = random.choice(cardStack)
    cardStack.remove(hintCardFour)
    cardFourSplit = hintCardFour.split(" of ")

    print('\n')
    print("Welcome to Guessing Suits!")
    print("We will now draw four cards out of a deck of standard playing cards. Your goal is to guess what the first card is.")
    print("You have access to three hint cards, the first hint is free. We will tell you the relation between each hint card and the first card.")
    print("i.e. greater than, less than, equal to, same suit, different suit.")

    if victoryPoints > 0:
        print("\n    Your current score is: ", victoryPoints, '\n')

    #Contains the main game loop //////////////////////////////////////////////////////////////////
    while gameRunning:

        #Failstate
        if guessCounter >= 3:
            print("You have run out of guesses! \nThe card was, ", primeCard)
            print("Would you like to try again? y/n \n")
            userInput = input().lower()

            if userInput == "y":
                break

            else:
                print("Thank you for playing!")
                gameRunning = False
                break

        #Prints of hints based on how many hints you have recieved ////////////////////////////////
        if hintCounter == 0:
            print('\n', "Your first hint: ", hintCardOne)
            cardComparison(primeCardSplit, cardOneSplit)

        elif hintCounter == 1:
            print('\n', "Your first hint: ", hintCardOne)
            cardComparison(primeCardSplit, cardOneSplit)
            print('\n', "Your second hint: ", hintCardTwo)
            cardComparison(primeCardSplit, cardTwoSplit)

        elif hintCounter == 2:
            print('\n', "Your first hint: ", hintCardOne)
            cardComparison(primeCardSplit, cardOneSplit)
            print('\n', "Your second hint: ", hintCardTwo)
            cardComparison(primeCardSplit, cardTwoSplit)
            print('\n', "Your third hint: ", hintCardThree)
            cardComparison(primeCardSplit, cardThreeSplit)
            print('\n', "Your are out of hints.")

        else:
            print('\n', "Your first hint: ", hintCardOne)
            cardComparison(primeCardSplit, cardOneSplit)
            print('\n', "Your second hint: ", hintCardTwo)
            cardComparison(primeCardSplit, cardTwoSplit)
            print('\n', "Your third hint: ", hintCardThree)
            cardComparison(primeCardSplit, cardThreeSplit)
            print('\n', "Your fourth hint: ", hintCardFour)
            cardComparison(primeCardSplit, cardFourSplit)
            print('\n', "Your are out of hints.")

        print("   END: Ends program\n", "  RESTART: Restarts game\n", "  HINT: Gives another hint\n")

        userInput = input().lower()
        
        #Runs when the user correctly gusses the chosen card //////////////////////////////////////
        if userInput == primeCard.lower():
            print("Well done! You have guessed correctly!", '\n')
            victoryPoints += 10 - hintCounter - (guessCounter * 2)
            break

        #Runs if the users inputted value is a card, but not the correct card /////////////////////
        elif userInput in lowerList:
            print("That is incorrect.", '\n')
            guessCounter += 1

        #Runs when the user enters "END" //////////////////////////////////////////////////////////
        elif userInput == "end":
            print("Goodbye", '\n')
            gameRunning = False
            break

        #Runs when the user enters "RESTART" //////////////////////////////////////////////////////
        elif userInput == "restart":
            print("Reseting...", '\n')
            break

        #Prints out one of the hint cards when the player enters "HINT" ///////////////////////////
        elif userInput == "hint":
            hintCounter += 1

        #Prints when the user enters and unrecognized command ////////////////////////////////////
        else:
            print('\n', "Command not recognized.", '\n')