from Card import AttackCard, ComboCard
from Deck_Definition import *
from random import shuffle

def setup_deck():
    deck = []

    for x in deck_definition:
        #print(str(x) + ": " + str(deck_definition[x]))
        #print(len(deck_definition[x]))
        if(str(x) == "Rolling"):
            for i in deck_definition[x]:
                if type(i) is int:
                    deck.append(AttackCard(i, "", "", True))
                elif type(i) is str:
                    deck.append(AttackCard(0, i, "", True))
        else:
            for i in deck_definition[x]:
                if(i == "Miss" or
                   i == "Critical" or
                   i == "Curse" or
                   i == "Bless"):
                    deck.append(AttackCard(0, "", i, False))
                else:
                    deck.append(AttackCard(x, i, "Normal", False))

    shuffle(deck)
    for i in deck:
        print(str(i))
    return deck

def draw_card(deck):
    card = deck[0]
    deck.pop(0)
    print("Drew: " + str(card))
    return card, deck;

def get_effective_card(cards, advantage):
    # Cards is in order drawn. So every element before the last is rolling
    # Only the end card may be Miss, Crit, Curse, Bless

    if(advantage == 0 or (advantage == 1 and cards[0].is_rolling)):
        # Neither disadvantage or advantage
        # OR
        # Advantage, but there are rolling modifiers
        # Just sum all the rolling modifiers with the last card
        card_type = cards[-1].type
        value = 0
        conditions = []
        for i in cards:
            value += i.value
            if i.condition:
                conditions.append(i.condition)
        return ComboCard(value, card_type, conditions)
    elif(advantage == -1):
        # Disadvantage, disregard the rolling cards and take the non-rolling
        # If we have two non-rolling, take worst. First if tied
        if(cards[0].is_rolling):
            # Rules state we disregard this and take the non-rolling
            return ComboCard(cards[-1].value, cards[-1].type, cards[-1].condition)
        # Else, we need to pick from the two
        if ((cards[0].type == "Miss") or (cards[0].type == "Curse") or
            (cards[1].type == "Miss") or (cards[1].type == "Miss")):
            # If either of them are Curses or Misses, we Miss
            return ComboCard(0, "Miss", "")
        if cards[0].condition:
            value_0 = cards[0].value + 1
        else:
            value_0 = cards[0].value
        if cards[1].condition:
            value_1 = cards[1].value + 1
        else:
            value_1 = cards[1].value
        if value_0 <= value_1:
            return ComboCard(cards[0].value, cards[0].type, cards[0].condition)
        else:
            return ComboCard(cards[1].value, cards[1].type, cards[1].condition)
    elif(advantage == 1):
        # Advantage without rolling cards, take the best one
        # If either are Bless or Critical, we take it
        if ((cards[0].type == "Bless") or (cards[0].type == "Critical") or
            (cards[1].type == "Bless") or (cards[1].type == "Critical")):
            # If either of them are Curses or Misses, we Miss
            return ComboCard(0, "Critical", "")
        if cards[0].condition:
            value_0 = cards[0].value + 1
        else:
            value_0 = cards[0].value
        if cards[1].condition:
            value_1 = cards[1].value + 1
        else:
            value_1 = cards[1].value
        if value_0 >= value_1:
            return ComboCard(cards[0].value, cards[0].type, cards[0].condition)
        else:
            return ComboCard(cards[1].value, cards[1].type, cards[1].condition)

def play_until_shuffle(deck, attack_num_dist, advantage_dist):
    reshuffle_triggered = False
    selected_results = []

    while((not reshuffle_triggered) and len(deck) > 0):
        # Pick number of attacks this round
        num_attacks = 1

        for a in range(num_attacks):
            # Determine if this attack has (dis)advantage
            # 0 = Neither, 1 = Advantage, -1 = Disadvantage
            advantage = 1
            
            drawn_cards = []
            # Draw the first card
            card, deck = draw_card(deck)
            drawn_cards.append(card)
            # Check to see if we just drew the Miss or Crit
            reshuffle_triggered = reshuffle_triggered or drawn_cards[-1].reshuffle()

            # Draw until we do not draw a rolling modifier
            while(drawn_cards[-1].is_rolling):
                card, deck = draw_card(deck)
                drawn_cards.append(card)
                reshuffle_triggered = reshuffle_triggered or drawn_cards[-1].reshuffle()

            # If we have (dis)advantage, we need at least 2 cards
            if ((len(drawn_cards)<2) and (advantage != 0)):
                card, deck = draw_card(deck)
                drawn_cards.append(card)
                reshuffle_triggered = reshuffle_triggered or drawn_cards[-1].reshuffle()
                if(drawn_cards[-1].is_rolling):
                    # So the first card is normal, the second rolling.
                    # Reverse them for the picking function
                    drawn_cards = [drawn_cards[1], drawn_cards[0]]

            selected_results.append(get_effective_card(drawn_cards, advantage))
            print(str(selected_results[-1]))

attack_deck = setup_deck()
play_until_shuffle(attack_deck, 0, 0)
