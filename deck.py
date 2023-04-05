import random

class CardGame:
    def __init__(self, cards, suits):
        self.cards = cards
        self.suits = suits

        # Constant version of deck that will not be shuffled or altered
        self.c_deck = []
        for suit in self.suits:
            for card in self.cards:
                self.c_deck.append(card + " of " + suit)

        self.v_deck = []
        for suit in self.suits:
            for card in self.cards:
                self.v_deck.append(card + " of " + suit)

        self.drawnCards = []
        self.discard = []

    # Lists every card in the deck ////////////////////////////////////////
    #def listCards(self):
        #for suit in self.suits:
            #for card in self.cards:
                #print(card + " of " + suit)
            #print()

    def addCards(self, cardNames):
        for cards in cardNames:
            self.c_deck.append(cards)

    # Randomizes the order of the "deck" list /////////////////////////////
    def shuffle(self):
        random.shuffle(self.v_deck)
        print("Shuffled...")

    # Draws the first card in the "deck" and then removes it from the deck
    def drawCard(self):
        self.drawnCards.append(self.v_deck[0])
        self.v_deck.pop(0)

    # Sets the "deck" variable to be the same as the "c_deck" to reset the deck to original form
    def resetDeck(self):
        self.v_deck = self.c_deck
        print("Reset...")

    # Default Print Statement /////////////////////////////////////////////
    def __str__(self):
        return f"{self.c_deck}"



standardGameDeck = CardGame(["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"],["Clubs", "Spades", "Diamonds", "Hearts"])
#print(standardGameDeck)

tarotDeck = CardGame(["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"],["Swords", "Goblets", "Pentacles", "Wands"])
#print(minorArcana)

tarotDeck.addCards(["The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World", "The Fool"])

print(tarotDeck, '\n', "# of Cards: ", len(tarotDeck.c_deck))

#print(standardGameDeck.v_deck, '\n')
standardGameDeck.shuffle()
#print(standardGameDeck.v_deck, " # of Cards: ", len(standardGameDeck.v_deck),  '\n')

# Draw 5 cards
for i in range(1, 6):
    standardGameDeck.drawCard()
print(standardGameDeck.drawnCards)

# Reshuffle
standardGameDeck.shuffle()
#print(standardGameDeck.v_deck, " # of Cards: ", len(standardGameDeck.v_deck),  '\n')

# Draw 5 cards
for i in range(1, 6):
    standardGameDeck.drawCard()
print(standardGameDeck.drawnCards)

#standardGameDeck.addCards(["Bird of Death", "Ambiton of Mortality", "Lies of Innocence"])
#print(standardGameDeck.c_deck)

#standardGameDeck.resetDeck()
#print(standardGameDeck.v_deck, '\n')