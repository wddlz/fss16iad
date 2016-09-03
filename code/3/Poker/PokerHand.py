# coding=utf-8
"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from Card import *
__author__ = "ian drosos"


class PokerHand(Hand):
    """
    DOC-STRINGING IT UP
    """
    def num_hist(self):
        """
        :return: builds a histogram of the numbers that appear in a hand.
        """
        self.nums = {}

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.

        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_pair(self):
        """
        :return: True if hand has pair, else False
        """
        return True
        return False

if __name__ == '__main__':
    # make a deck
    deck = Deck()
    deck.shuffle()
    card_amount = 0
    hand_amount = 0
    # Card.py hard-codes that there is only 1 deck of 52 cards, So hands must adhere to limited cards
    # # For example, for a 13 card hand, only 4 hands can be made with 0 cards left. For a 12 card hand, 4 hands can
    # # also be made but with 4 cards remaining...
    # So amount of hands = 52 / amount of cards in each hand
    print "How many cards per hand for your game? >> "
    while True:
        try:
            card_amount = int(raw_input())
            break
        except Exception, e:
            print e
            print "Please choose a valid integer... >> "

    hand_amount = 52 / card_amount
    # print "\nDealing %s cards\n" % str(card_amount)
    # calculate possible hand amount
    print "----------------------------"
    print "Dealing %s hands of %s cards" % (str(hand_amount), str(card_amount))
    print "----------------------------"
    # deal the cards and classify the hands
    for i in range(hand_amount):
        print "HAND %s" % (i + 1)
        hand = PokerHand()
        deck.move_cards(hand, card_amount)
        hand.sort()
        print hand
        print hand.has_flush()
        print "----------------------------"
