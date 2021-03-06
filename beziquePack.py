# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 23:18:40 2019
Notes: White space/style guide?
Classes:
    Player
        Score
        If they are dealing
        Hand
    
@author: Harry
"""

import random
import time

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value #rename to rank
        self.getRank()
        
        if self.value in ['A','10']:
            self.points = 10
        else:
            self.points = 0
            
    def __str__(self):
        return " of ".join((self.value, self.suit)) #str vs repr? want to print combined strings of cards and other info

    def __repr__(self):
        return " of ".join((self.value, self.suit))
    
    def getRank(self): #do we use getters and setters in python? do properties need to be predefined? 
        valueLookup = dict(zip(["A", "7", "8", "9", "10", "J", "Q", "K"],[8,1,2,3,7,4,5,6]))#card will calculate its own rank/value - in ascendingorder
        self.rank = valueLookup[self.value]
    


class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Clubs","Diamonds","Hearts","Spades"] for v in
                      (["A", "7", "8", "9", "10", "J", "Q", "K"])*2] #store list of cards in order somewhere?

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def display(self):
        handStr= ''
        i = 1
        cardNumStr = ''
        for card in self.cards:
            print(card)
            handStr = (handStr + card.value + card.suit[0] + ' ')
            cardNumStr = cardNumStr + str(i) + "  "
            if card.value == '10':
                cardNumStr = cardNumStr + " "
            i = i + 1
        print(handStr)
        print(cardNumStr)
        
            
    def sortHand(self): #list comprehensions, map and lambda or for loop, use to learn
        
        suitList = ["Clubs","Diamonds","Hearts","Spades"] #property of the deck class?
        suitedCards = dict(zip(suitList,[[],[],[],[]])) #typed out 4 empty lists, better way to do this?
        sortedCards = []
    
        for s in ["Clubs","Diamonds","Hearts","Spades"]:
            for card in self.cards:
                if card.suit == s:
                    suitedCards[s].append(card)
            if suitedCards[s]:        
                suitedCards[s] = sorted(suitedCards[s],key=lambda card:card.rank)       
                sortedCards.extend(suitedCards[s])

        self.cards = sortedCards
        self.suitedCards = suitedCards #could just store values as ints instead of card objects?
        
class Player:
    def __init__(self,name,hand,dealer=False):
        self.name = name
        self.score = 0
        self.dealer = dealer
        self.hand = hand
        
class OpponentAi:
    def __init__(self,hand,dealer=False):
        self.playerInfo = Player('Villan',hand,dealer=False)
        self.decRdy = False
        self.followSuit = False
        
#    def respondCard(self,playedCard=card):
#        if self.playerInfo.hand.suitedCards[playedCard.suit]: #check if opponent has any cards of the suit played
            
        
#        if self.decRdy: #if AI has a declaration to be made, the trick will try to be won
            
        
        

class Game:
    def __init__(self):
        pass

    def play(self):
#        playing = True
        
#        while playing:
        self.deck = Deck()
        self.deck.shuffle()
        self.playerAction = True #flag if the player is leading the action
        
        print('Welcome to Bezique')
        playerName = input('Please enter your name: ')
        
        decidingDealer = True
        
        while decidingDealer:
            print('You cut the deck to reveal...')
            time.sleep(1)
            myCutCard = self.deck.cards[random.randint(0,64)] #64 hardcoded, could detect length of deck..?
            print(myCutCard)
            print('Opponent cuts the deck to reveal...')
            time.sleep(1)
            opponentCutCard = self.deck.cards[random.randint(0,64)]
            print(opponentCutCard)
            time.sleep(1)
            
            if myCutCard.rank > opponentCutCard.rank:
                print('You win the cut, assigned as dealer!')
                dealerFlag = True
                decidingDealer = False
                self.playerAction = False
            elif opponentCutCard: 
                print('Opponent wins the cut, opponent assigned as dealer')
                decidingDealer = False
                dealerFlag = False
                self.playerAction = True
            else:
                print('Values equal cutting again...')
            print()


        self.player = Player(playerName,Hand(),dealerFlag)
        self.opponentAI = OpponentAi(Hand(),not(dealerFlag))

#        self.player_hand = Hand(dealerFlag)
#        self.dealer_hand = Hand(not(dealerFlag))

        for i in range(8):
#            self.player_hand.add_card(self.deck.deal())
            self.player.hand.add_card(self.deck.deal())
            self.opponentAI.playerInfo.hand.add_card(self.deck.deal())
            
        self.player.hand.sortHand()

        print("Your hand is:")
        self.player.hand.display()
        print()
        print("Villan's hand is:")
        self.opponentAI.playerInfo.hand.display()
        print()
        print("Top card is:")
        displayCard = self.deck.deal() #display card property of deck? Or game?
        print(displayCard)
        print("Trumps are: " + displayCard.suit)
        self.trumpSuit = displayCard.suit
        print()
        
        if displayCard.value == '7':
            print('Dealer turned up a 7, scores 10 points!')
            if self.playerAction:
                self.opponentAI.playerInfo.score += 10
            else:
                self.player.score += 10 
            
            print('Player score: ' + str(self.player.score))
            print('Opponent score: ' + str(self.opponentAI.playerInfo.score))
            print()
        
        bezHand = Hand() #property of class?
        
        if displayCard.suit == 'Clubs' or displayCard.suit == 'Hearts':
            bezHand.add_card(Card('Spades','Q'))
            bezHand.add_card(Card('Diamonds','J'))
        else:
            bezHand.add_card(Card('Clubs','Q'))
            bezHand.add_card(Card('Hearts','J'))
            
        print("Bezique is:")
        bezHand.display()
        print()
        
        playing = True
        
        while playing:
            if self.playerAction:                
                playedCard = self.playerSelectCard()
                opponentCard = self.opponentAI.playerInfo.hand.cards.pop(random.randint(0,7)) #for now just picking a random card...
                print('Opponent plays...')
                print(opponentCard)
                time.sleep(0.5)
                self.evaluateTrick(playedCard,opponentCard)
#                if playedCard.suit != opponentCard.suit: #need to make generic with logic for if opponent goes first
#                    if  opponentCard.suit != self.trumpSuit:
#                        print('You win!')
#                    else:
#                        print('Opponent trumps and wins!')
#                else:
#                    if playedCard.rank < opponentCard.rank:
#                        print('Opponent wins')
#                    else:
#                        print('You win')
            else:
#                self.opponentAIPlay() # tell opponent to play first
                opponentCard = self.opponentAI.playerInfo.hand.cards.pop(random.randint(0,7)) #for now just picking a random card...
                print('Opponent plays...')
                print(opponentCard)
                print()
                playedCard = self.playerSelectCard()
                self.evaluateTrick(opponentCard,playedCard) #could set first and second cards in loop and call this function only once outside if statement
            
            print()
            print('Player score: ' + str(self.player.score))
            print('Opponent score: ' + str(self.opponentAI.playerInfo.score))
            print()
            time.sleep(0.5)
            
            declaring = True
            
            if self.playerAction:
                while declaring:
                    self.player.hand.display()
                    actionChoice = input('Your turn, declare or pickup or quit? [d/p/q])')
                    if actionChoice == 'd':
                        decChoice = input('Select cards to declare (1-7) ')
                        if len(decChoice) == 1:
                            decChoice = int(decChoice)
                            cardChoice = self.player.hand.cards[(decChoice - 1)]
                            if (cardChoice.suit == self.trumpSuit) and (cardChoice.value == '7'):
                                if displayCard.value == '7': #should this be a property/atribute of self/game object?
                                    print('Seven of trumps shown in hand, 10 points scored')
                                else:
                                    self.player.hand.add_card(displayCard)
                                    oldDisplayCard = str(displayCard)
                                    displayCard = self.player.hand.cards.pop((decChoice - 1))#swap the card
                                    self.player.hand.sortHand()
                                    print('Face up card ' + oldDisplayCard + ' swapped for ' + str(displayCard))
                                    
                                self.player.score += 10
                            else:
                                print('Card selection cannot be declared')#can't declare this card
                        else: #could use length to narrow down further
                            decChoice = decChoice.split(',')
                            cardIndex = [int(x)-1 for x in decChoice]
                            cardIndex.sort()
                            suitList = [self.player.hand[cardIndex].suit for i in cardIndex]
                            valueList = [self.player.hand[cardIndex].value for i in cardIndex]
                            
                            #need to make generic for opponent too!!
                            if len(cardIndex) == 2: #bezique or marriage #large if statement, store bezique knowledge beforehand? #more clever way of matching up use boolean array?
                                if ((suitList == ['Diamonds','Spades'] and valueList == ['J','Q'] and 
                                    (displayCard.suit == 'Hearts' or displayCard.suit == 'Clubs')) or 
                                    (suitList == ['Clubs','Hearts'] and valueList == ['Q','J'] and 
                                    (displayCard.suit == 'Diamonds' or displayCard.suit == 'Spades'))): #cards are already sorted                                
                                    print('Bezique declared, 40 points!')
                                    self.player.score += 40
                                elif len(set(suitList)==1):
                                    if valueList == ['Q','K']:
                                        if suitList[0] == displayCard.suit:
                                            print('Royal marriage declared, 40 points!')
                                            self.player.score += 40
                                        else:
                                            print('Common marriage declared, 20 points!')
                                            self.player.score += 20
                                else:
                                    print('Selected cards cannot be declared')
                                print()
                            elif len(cardIndex) == 4: #double bezique or set
                                print()
                                
                            elif len(cardIndex) == 5: #sequence
                                if (displayCard.suit in set(suitList)) and (len(set(suitList)) == 1) and (valueList == ['J','Q','K','A','10']):
                                    print('Sequence scored!!')
                                    self.player.score += 250
                                    
                                
#                                suitList = [self.player.hand[(i-1)].suit for i in decChoice]
#                                valueList = 
#                                seqHand = Hand()
#                                for i in cardIndex:
#                                    seqHand.add_card(self.player.hand.cards[i])
                            
                    elif actionChoice == 'q':
                        declaring = False
                        playing = False
                                                
                    elif actionChoice == 'p':
                        declaring = False
            
            newCard = self.deck.deal()
            newCard = Card(displayCard.suit,'7') #temp
            print('You pick up card: ')
            print(newCard)
            print()
            self.player.hand.add_card(newCard)
            self.player.hand.sortHand()
#            self.player.hand.display() #where to display? just show new card here?
            self.opponentAI.playerInfo.hand.add_card(self.deck.deal())
                
            #evaluate played cards            
            

    def playerSelectCard(self):
        self.player.hand.display()
        cardChoice = int(input('Select a card to play (1-8) '))
        playedCard = self.player.hand.cards.pop((cardChoice - 1))
        print('Playing...')
        print(playedCard)
        time.sleep(0.5)
        return playedCard
    
    def evaluateTrick(self,leadCard,secondCard):       
        if leadCard.suit != secondCard.suit: #need to make generic with logic for if opponent goes first
            if  secondCard.suit != self.trumpSuit:
                leadWin = True
            else:
                leadWin = False
                print('Trick trumped!')
        else:
            if leadCard.rank < secondCard.rank:
                leadWin = False
            else:
                leadWin = True
                
        trickScore = leadCard.points + secondCard.points
                
        if leadWin ^ self.playerAction:
            print('Opponent wins')
            self.playerAction = False
            self.opponentAI.playerInfo.score += trickScore            
        else:
            print('You win!')
            self.playerAction = True
            self.player.score += trickScore            

if __name__ == "__main__":
    g = Game()
    myHand = g.play()