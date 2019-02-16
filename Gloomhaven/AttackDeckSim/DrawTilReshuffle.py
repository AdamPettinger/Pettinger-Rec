from Card import *
from Deck_Definition import *
from random import shuffle
import copy, statistics

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
    return deck

def draw_card(deck):
    card = deck[0]
    deck.pop(0)
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
        if len(cards) == 1:
            return ComboCard(True, cards[0], 0, 0, 0)
        
        for i in cards:
            value += i.value
            if i.condition:
                conditions.append(i.condition)
        # Mark if we just Missed with advantage
        if(cards[-1].type == "Miss" or cards[-1].type == "Curse"):
            return ComboCard(False, 0, 0, "Advantaged Miss", "")
        # Mark if we just Super Criticalled
        elif(cards[-1].type == "Critical" or cards[-1].type == "Bless"):
            return ComboCard(False, 0, value, "Super Critical", conditions)
        return ComboCard(False, 0, value, card_type, conditions)
    elif(advantage == -1):
        # Disadvantage, disregard the rolling cards and take the non-rolling
        # If we have two non-rolling, take worst. First if tied
        if(cards[0].is_rolling):
            # Rules state we disregard this and take the non-rolling
            # Mark if we just Criticalled with Dis because of this
            if(cards[-1].type == "Critical" or cards[-1].type == "Bless"):
                return ComboCard(False, 0, 0, "Disadvantaged Critical", "")
            return ComboCard(True, cards[1], 0, 0, 0)
        # Else, we need to pick from the two
        if ((cards[0].type == "Miss") or (cards[0].type == "Curse") or
            (cards[1].type == "Miss") or (cards[1].type == "Miss")):
            # If either of them are Curses or Misses, we Miss
            return ComboCard(False, 0, 0, "Miss", "")
        # If one is bless/critical, take the other
        elif ((cards[0].type == "Bless") or (cards[0].type == "Critical")):
            return ComboCard(True, cards[1], 0, 0, 0)
        elif ((cards[1].type == "Bless") or (cards[1].type == "Critical")):
            return ComboCard(True, cards[0], 0, 0, 0)
        if cards[0].condition:
            value_0 = cards[0].value + 1
        else:
            value_0 = cards[0].value
        if cards[1].condition:
            value_1 = cards[1].value + 1
        else:
            value_1 = cards[1].value
        if value_0 <= value_1:
            return ComboCard(True, cards[0], 0, 0, 0)
        else:
            return ComboCard(True, cards[1], 0, 0, 0)
    elif(advantage == 1):
        # Advantage without rolling cards, take the best one
        # If either are Bless or Critical, we take it
        if ((cards[0].type == "Bless") or (cards[0].type == "Critical") or
            (cards[1].type == "Bless") or (cards[1].type == "Critical")):
            # If either of them are Blesses or Criticals, we Crit
            return ComboCard(False, 0, 0, "Critical", "")
        # If one is curse/miss, take the other
        elif ((cards[0].type == "Miss") or (cards[0].type == "Curse")):
            return ComboCard(True, cards[1], 0, 0, 0)
        elif ((cards[1].type == "Miss") or (cards[1].type == "Curse")):
            return ComboCard(True, cards[0], 0, 0, 0)
        if cards[0].condition:
            value_0 = cards[0].value + 1
        else:
            value_0 = cards[0].value
        if cards[1].condition:
            value_1 = cards[1].value + 1
        else:
            value_1 = cards[1].value
        if value_0 >= value_1:
            return ComboCard(True, cards[0], 0, 0, 0)
        else:
            return ComboCard(True, cards[1], 0, 0, 0)

def play_until_shuffle(deck, attack_num_dist, advantage_dist):
    reshuffle_triggered = False
    selected_results = []
    number_rounds = 0
    total_attacks = 0

    while((not reshuffle_triggered) and len(deck) > 0):
        number_rounds += 1
        # Pick number of attacks this round
        num_attacks = 1
        total_attacks += num_attacks

        for a in range(num_attacks):
            # Determine if this attack has (dis)advantage
            # 0 = Neither, 1 = Advantage, -1 = Disadvantage
            advantage = 0
            
            drawn_cards = []
            # Draw the first card
            card, deck = draw_card(deck)
            drawn_cards.append(card)
            # Check to see if we just drew the Miss or Crit
            if drawn_cards[-1].reshuffle(): reshuffle_triggered = True
            
            # Draw until we do not draw a rolling modifier
            while(drawn_cards[-1].is_rolling):
                card, deck = draw_card(deck)
                drawn_cards.append(card)
                if drawn_cards[-1].reshuffle(): reshuffle_triggered = True
                
            # If we have (dis)advantage, we need at least 2 cards
            if ((len(drawn_cards)<2) and (advantage != 0)):
                card, deck = draw_card(deck)
                drawn_cards.append(card)
                if drawn_cards[-1].reshuffle(): reshuffle_triggered = True
                if(drawn_cards[-1].is_rolling):
                    # So the first card is normal, the second rolling.
                    # Reverse them for the picking function
                    drawn_cards = [drawn_cards[1], drawn_cards[0]]

            selected_results.append(get_effective_card(drawn_cards, advantage))

    return selected_results, number_rounds, total_attacks

def process_attack_results(attack_results):
    n = len(attack_results)
    total_conditions = copy.deepcopy(condition_dictionary)
    total_specials = copy.deepcopy(special_dictionary)
    all_values = []

    # Iter through each result and add it to the totals
    for result in attack_results:
        if result.type == "Normal":
            all_values += [result.value]

        elif result.type == "Super Critical":
            total_specials["Super Critical"] += [result.value]

        else:
            total_specials[result.type] += 1/n

        for cond in result.conditions:
                if cond: total_conditions[cond] += 1/n

            
    print(str(statistics.mean(all_values)) + " +- " + str(statistics.stdev(all_values)))
    print(total_conditions)
    print(total_specials)
    return

def play_num_rounds_without_reset(min_rounds):
    attack_deck = setup_deck()
    
    played_rounds = 0
    attacks_taken = 0
    attack_results = []

    while(played_rounds <= min_rounds):
        new_results, new_rounds, new_attacks = play_until_shuffle(attack_deck, 0, 0)

        played_rounds += new_rounds
        attacks_taken += new_attacks
        attack_results += new_results

    return



attack_deck = setup_deck()
test_select, test_rounds, test_attacks = play_until_shuffle(attack_deck, 0, 0)
print('Attacked ' + str(test_attacks) + ' times in ' + str(test_rounds) + ' rounds')
for i in test_select:
    print(str(i))

process_attack_results(test_select)
