# -*- coding: utf-8 -*-
# !/usr/bin/python
"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""
from __future__ import division
from Card import *
import sys

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
        """
        :return: if the hand has two pairs of cards
        """
        count = 0
        self.num_hist()
        for val in self.nums.values():
            if val >= 2:
                count += 1
        if count >= 2:
            self.check_class("two pair")
            return True
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
        self.num_hist()
        self.nums[14] = self.nums.get(1, 0)  # since Ace is both 1 and 11 set both 1 and 14 to ace count
        # now test for seq of 5 e.g. Ace, 2, 3, 4, 5 of any suit (straight flush will match suits and be a seq)
        # So if there is a 2 (count is 1), if the next number is a 3 count += 1 else start count over (as the hand
        # does not have the number being checked)
        count = 0
        for x in xrange(1, 14):
            if self.nums.get(x, 0):
                count += 1
                if count == 5:
                    self.check_class("straight")
                    return True  # 5 in a seq = straight
            else:
                count = 0
        return False

    def has_full_house(self):
        """
        :return: if the hand a three of a kind and a pair
        """
        three_count = 0
        two_count = 0
        self.num_hist()
        for val in self.nums.values():
            if val >= 3 and three_count == 0:  # get first 3 count and then find a pair
                three_count += 1
            elif val >= 2:
                two_count += 1
        if three_count >= 1 and two_count >= 1:
            self.check_class("full house")
            return True
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
        # like has_straight but does it per suit
        self.suit_hist()
        self.num_hist()
        suit_rank = {0: [], 1: [], 2: [], 3: []}
        for card in self.cards:
            # make a list of ranks for each suits
            suit_rank.get(card.suit).append(card.rank)
            if card.rank == 1:  # deal with aces being 1 and 14 rank
                suit_rank.get(card.suit).append(14)

        # print suit_rank
        # But we need to sort each suits list to prevent 14 from being next to 1
        for sr in suit_rank:
            suit_rank[sr] = sorted(suit_rank[sr])
            count = 0
            # print suit_rank
            # each list of ranks will then be searched for a straight
            for x in xrange(1, 14):
                if x in suit_rank[sr]:
                    # similar logic to straight, being done for each suit. so if Hearts list contains 1, count = 1
                    # then if Hearts list contains 2, count = 2, then if Hearts list does not contain 3, count = 0
                    count += 1
                    if count == 5:
                        # no need to check every suit if one of the suits has a straight flush
                        self.check_class("straight flush")
                        return True
                else:
                    count = 0
        return False


if __name__ == '__main__':
    card_amount = 0
    hand_amount = 0
    # Card.py hard-codes that there is only 1 deck of 52 cards, So hands must adhere to limited cards
    # # For example, for a 13 card hand, only 4 hands can be made with 0 cards left. For a 12 card hand, 4 hands can
    # # also be made but with 4 cards remaining...
    # So amount of hands = 52 / amount of cards in each hand
    print "How many cards per hand for your game?: "
    sys.stdout.flush()
    while True:
        try:
            card_amount = int(raw_input())
            break
        except Exception, e:
            print e
            print "Please choose a valid integer: "
            sys.stdout.flush()

    hand_amount = 52 // card_amount  # double slash for integer division
    # print "\nDealing %s cards\n" % str(card_amount)
    # calculate possible hand amount
    print "----------------------------"
    print "Dealing %s hands of %s cards" % (str(hand_amount), str(card_amount))
    print "----------------------------"
    # deal the cards and classify the hands
    """
    This is the first part of the Poker exercise, commented for the statistics part as printing thousands of hands
    is unreadable. If you want to see the hands work, uncomment this code and comment the statistics code below
    """
    # for i in range(hand_amount):
    #     print "HAND %s" % (i + 1)
    #     hand = PokerHand()
    #     deck.move_cards(hand, card_amount)
    #     hand.sort()
    #     print hand
    #     print "...Hand has..."
    #     print "Straight flush: " + str(hand.has_straight_flush())
    #     print "Four of a kind:  " + str(hand.has_four())
    #     print "Full house: " + str(hand.has_full_house())
    #     print "Flush: " + str(hand.has_flush())
    #     print "Straight: " + str(hand.has_straight())
    #     print "Three of a kind: " + str(hand.has_three())
    #     print "Two pairs: " + str(hand.has_two_pair())
    #     print "Pair: " + str(hand.has_pair())
    #     print "Highest class: " + hand.highest_class
    #     print "----------------------------"
    """
    STATISTICS CODE
    Target for 5 per hand:
        SF (72,192:1 || 0.00139%)
        4oaK (4,164:1 || 0.024%)
        FH (693:1 || 0.1441%)
        Flush (508:1 || 0.1965%)
        Straight (254:1 || 0.3925%)
        3oaK (46.3:1 || 2.1128%)
        2P (20:1 || 4.7539%)
        Pair (1.37:1 || 42.2569%)
    Target for 7 per hand:
        SF (3,589.6:1 || 0.0279%)
        4oaK (594:1 || 0.168%)
        FH (37.5:1 || 2.60%)
        Flush (32.1:1 || 3.03%)
        Straight (20.6:1 || 4.62%)
        3oaK (19.7:1 || 4.83%)
        2P (3.26 || 23.5%)
        Pair (1.28:1 || 43.8%)
    """
    run_amount = 0
    print "How many runs(for stats)?: "
    sys.stdout.flush()
    while True:
        try:
            run_amount = int(raw_input())
            break
        except Exception, e:
            print e
            print "Please choose a valid integer: "
            sys.stdout.flush()
    print "%s games being played..." % run_amount
    stats_dict = {"straight flush": 0, "four of a kind": 0, "full house": 0, "flush": 0, "straight": 0,
                  "three of a kind": 0, "two pair": 0, "pair": 0}
    anti_counter = run_amount
    while anti_counter > 0:
        # make a deck (a new one for each run so don't run out of cards in the deck)
        deck = Deck()
        deck.shuffle()
        for i in range(hand_amount):
            hand = PokerHand()
            deck.move_cards(hand, card_amount)
            hand.sort()
            if hand.has_straight_flush():
                stats_dict["straight flush"] += 1
            if hand.has_four():
                stats_dict["four of a kind"] += 1
            if hand.has_full_house():
                stats_dict["full house"] += 1
            if hand.has_flush():
                stats_dict["flush"] += 1
            if hand.has_straight():
                stats_dict["straight"] += 1
            if hand.has_three():
                stats_dict["three of a kind"] += 1
            if hand.has_two_pair():
                stats_dict["two pair"] += 1
            if hand.has_pair():
                stats_dict["pair"] += 1
            # if hand.highest_class == "high card":
            #     stats_dict["high card"] += 1  # all hands have high card, so this is for an "else"
        anti_counter -= 1
    total = hand_amount * run_amount
    print "---------"
    print stats_dict
    print "---------"
    for sd in stats_dict:
        percentage = stats_dict[sd] / total
        ratio = total / stats_dict[sd]
        print sd + " : " + str(ratio) + " to 1 || " + str(percentage * 100) + "%"
    print str(total) + " hands analyzed"
