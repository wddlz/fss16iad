# fss16iad, Team C, Code 3
### Exercise 6 Poker

###Part 1,2,3,4 (build hands and classify them)###
![screen1pt1](https://github.com/wddlz/fss16iad/blob/master/code/3/Poker/screenshots/ThreeAndFour1.PNG)
![screen1pt2](https://github.com/wddlz/fss16iad/blob/master/code/3/Poker/screenshots/ThreeAndFour2.PNG)

###Part 4,5 (get probabilities of hand scores)###
![screen2pt1](https://github.com/wddlz/fss16iad/blob/master/code/3/Poker/screenshots/FiveAndSix1.PNG)
***Ratios to reach*** (from https://en.wikipedia.org/wiki/Poker_probability)
+ Target for 5 per hand:
  + straight flush (72,192:1 || 0.00139%)
  + four of a kind (4,164:1 || 0.024%)
  + full house (693:1 || 0.1441%)
  + flush (508:1 || 0.1965%)
  + straight (254:1 || 0.3925%)
  + three of a kind (46.3:1 || 2.1128%)
  + two pair (20:1 || 4.7539%)
  + pair (1.37:1 || 42.2569%)
+ Target for 7 per hand:
  + straight flush (3,589.6:1 || 0.0279%)
  + four of a kind (594:1 || 0.168%)
  + full house (37.5:1 || 2.60%)
  + flush (32.1:1 || 3.03%)
  + straight (20.6:1 || 4.62%)
  + three of a kind (19.7:1 || 4.83%)
  + two pair (3.26 || 23.5%)
  + pair (1.28:1 || 43.8%)

***From assignment text***

The following are the possible hands in poker, in increasing order of value (and decreasing order of probability):
  + **pair:**
    + two cards with the same rank
  + **two pair:**
    + two pairs of cards with the same rank
  + **three of a kind:**
    + three cards with the same rank
  + **straight:**
    + five cards with ranks in sequence (aces can be high or low, so Ace-2-3-4-5 is a straight and so is 10-Jack-Queen-King-Ace, but Queen-King-Ace-2-3 is not.)
  + **flush:**
    + five cards with the same suit
  + **full house:**
    + three cards with one rank, two cards with another
  + **four of a kind:**
    + four cards with the same rank
  + **straight flush:**
    + five cards in sequence (as defined above) and with the same suit

The goal of these exercises is to estimate the probability of drawing these various hands.

1. Download the following files from http://thinkpython.com/code:
  + **Card.py**
    + : A complete version of the Card, Deck and Hand classes in this chapter.
  + **PokerHand.py**
    + : An incomplete implementation of a class that represents a poker hand, and some code that tests it

2. If you run PokerHand.py, it deals seven 7-card poker hands and checks to see if any of them contains a flush. Read this code carefully before you go on.

3. Add methods to PokerHand.py named has_pair, has_twopair, etc. that return True or False according to whether or not the hand meets the relevant criteria. Your code should work correctly for “hands” that contain any number of cards (although 5 and 7 are the most common sizes).

4. Write a method named classify that figures out the highest-value classification for a hand and sets the label attribute accordingly. For example, a 7-card hand might contain a flush and a pair; it should be labeled “flush”.

5. When you are convinced that your classification methods are working, the next step is to estimate the probabilities of the various hands. Write a function in PokerHand.py that shuffles a deck of cards, divides it into hands, classifies the hands, and counts the number of times various classifications appear.

6. Print a table of the classifications and their probabilities. Run your program with larger and larger numbers of hands until the output values converge to a reasonable degree of accuracy. Compare your results to the values at http://en.wikipedia.org/wiki/Hand_rankings.
