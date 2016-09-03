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
    highest_class = "high card"
    class_dict = {"straight flush": 1, "four of a kind": 2, "full house": 3, "flush": 4, "straight": 5,
                  "three of a kind": 6, "two pair": 7, "pair": 8, "high card": 9}

    def check_class(self, new_class):
        """
        :param new_class: the class to be potentially set as the highest class
        sets highest class
        """
        if self.class_dict[new_class] < self.class_dict[self.highest_class]:
            self.highest_class = new_class


    def num_hist(self):
        """
        :return: builds a histogram of the numbers that appear in a hand.
        """
        self.nums = {}
        for card in self.cards:
            self.nums[card.rank] = self.nums.get(card.rank, 0) + 1

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
                self.check_class("flush")
                return True
        return False

    def has_pair(self):
        """
        :return: True if hand has pair, else False
        """
        self.num_hist()
        for val in self.nums.values():
            if val >= 2:
                self.check_class("pair")
                return True
        return False

    def has_two_pair(self):
        # TODO
        """
        :return: if the hand has two pairs of cards
        """
        return False

    def has_three(self):
        """
        :return: if the hand has three of the same rank
        """
        self.num_hist()
        for val in self.nums.values():
            if val >= 3:
                self.check_class("three of a kind")
                return True
        return False

    def has_straight(self):
        """
        :return: if the hand has five cards with ranks in seq
        """
        # TODO
        return False

    def has_full_house(self):
        """
        :return: if the hand a three of a kind and a pair
        """
        # TODO
        return False

    def has_four(self):
        """
        :return: if the hand has four of the same rank
        """
        self.num_hist()
        for val in self.nums.values():
            if val >= 4:
                self.check_class("four of a kind")
                return True
        return False

    def has_straight_flush(self):
        """
        :return: if the hand has a straight that is a flush
        """
        # TODO
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
    # TODO run this X amount of times to get hand class probabilities
    for i in range(hand_amount):
        print "HAND %s" % (i + 1)
        hand = PokerHand()
        deck.move_cards(hand, card_amount)
        hand.sort()
        print hand
        print "...Hand has..."
        # print hand.has_straight_flush()
        print "Four of a kind:  " + str(hand.has_four())
        # print hand.has_full_house()
        print "Flush: " + str(hand.has_flush())
        # print hand.has_straight()
        print "Three of a kind: " + str(hand.has_three())
        # print hand.has_two_pair()
        print "Pair: " + str(hand.has_pair())
        print "Highest class: " + hand.highest_class
        print "----------------------------"
