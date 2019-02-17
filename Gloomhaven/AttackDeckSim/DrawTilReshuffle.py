from Card import *
from Deck_Definition import *
import random
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

    random.shuffle(deck)
    return deck

def draw_card(deck):
    card = deck[0]
    deck.pop(0)
    #print('Drew: ' + str(card))
    return card, deck;

def get_effective_card(cards, advantage):
    # Cards is in order drawn. So every element before the last is rolling
    # Only the end card may be Miss, Crit, Curse, Bless
    if(advantage == 0):
        # Neither disadvantage or advantage
        # Just sum all the rolling modifiers with the last card
        card_type = cards[-1].type
        value = 0
        conditions = []
        
        for i in cards:
            value += i.value
            if i.condition:
                conditions.append(i.condition)
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
        value = 0
        conditions = []
        if cards[0].is_rolling:
            # Advantage with rolling modifiers...
            # Mark if we just Missed with advantage
            if(cards[-1].type == "Miss" or cards[-1].type == "Curse"):
                return ComboCard(False, 0, 0, "Advantaged Miss", "")
            # Using the rolling cards to find the new value and conditions
            for i in cards:
                value += i.value
                if i.condition:
                    conditions.append(i.condition)
            # Mark if we just Super Criticalled
            if(cards[-1].type == "Critical" or cards[-1].type == "Bless"):
                return ComboCard(False, 0, value, "Super Critical", conditions)
            return ComboCard(False, 0, value, card_type, conditions)
        
        # Advantage without rolling cards, take the best one
        # If either are Bless or Critical, we take it
        if ((cards[0].type == "Bless") or (cards[0].type == "Critical") or
            (cards[1].type == "Bless") or (cards[1].type == "Critical")):
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

def determine_advantage(dist):
    x = random.uniform(0, sum(dist))
    
    for i in range(len(dist)-1):
        if x <= sum(dist[0:i+1]):
            return i-1

    return 1

def determine_number_attacks(dist):
    x = random.uniform(0, sum(dist))

    for i in range(len(dist)-1):
        if x <= sum(dist[0:i+1]):
            return i+1

    return len(dist)

def play_until_shuffle(deck, player):
    reshuffle_triggered = False
    selected_results = []
    number_rounds = 0
    total_attacks = 0
    cards_to_reshuffle = []
    advantage_tracker = []

    while((not reshuffle_triggered) and len(deck) > 0):
        number_rounds += 1
        # Pick number of attacks this round
        num_attacks = determine_number_attacks(player.num_attacks_dist)
        total_attacks += num_attacks

        for a in range(num_attacks):
            # Determine if this attack has (dis)advantage
            # 0 = Neither, 1 = Advantage, -1 = Disadvantage
            advantage = determine_advantage(player.advantage_dist)
            advantage_tracker.append(advantage)
            
            drawn_cards = []
            # Draw the first card
            card, deck = draw_card(deck)
            drawn_cards.append(card)
            # Check to see if we just drew the Miss or Crit
            if drawn_cards[-1].reshuffle(): reshuffle_triggered = True
            if not (drawn_cards[-1].type == "Curse" or drawn_cards[-1].type == "Bless"):
                cards_to_reshuffle.append(drawn_cards[-1])
            if len(deck) == 0:
                deck += cards_to_reshuffle
                random.shuffle(deck)
                reshuffle_triggered = True
            
            # Draw until we do not draw a rolling modifier
            while(drawn_cards[-1].is_rolling):
                card, deck = draw_card(deck)
                drawn_cards.append(card)
                if drawn_cards[-1].reshuffle(): reshuffle_triggered = True
                if not (drawn_cards[-1].type == "Curse" or drawn_cards[-1].type == "Bless"):
                    cards_to_reshuffle.append(drawn_cards[-1])
                if len(deck) == 0:
                    deck += cards_to_reshuffle
                    random.shuffle(deck)
                    reshuffle_triggered = True
                
            # If we have (dis)advantage, we need at least 2 cards
            if ((len(drawn_cards)<2) and (advantage != 0)):
                card, deck = draw_card(deck)
                drawn_cards.append(card)
                if drawn_cards[-1].reshuffle(): reshuffle_triggered = True
                if not (drawn_cards[-1].type == "Curse" or drawn_cards[-1].type == "Bless"):
                    cards_to_reshuffle.append(drawn_cards[-1])
                if len(deck) == 0:
                    deck += cards_to_reshuffle
                    random.shuffle(deck)
                    reshuffle_triggered = True
                if(drawn_cards[-1].is_rolling):
                    # So the first card is normal, the second rolling.
                    # Reverse them for the picking function
                    drawn_cards = [drawn_cards[1], drawn_cards[0]]

            selected_results.append(get_effective_card(drawn_cards, advantage))

    deck += cards_to_reshuffle
    random.shuffle(deck)
    #print('Shuffling Deck...')
    return selected_results, number_rounds, total_attacks, deck, advantage_tracker

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

def play_num_rounds_without_reset(player):
    attack_deck = setup_deck()
    for i in range(player.starting_curses):
        attack_deck.append(AttackCard(0, "", "Curse", False))
    for i in range(player.starting_blesses):
        attack_deck.append(AttackCard(0, "", "Bless", False))
    random.shuffle(attack_deck)
    
    played_rounds = 0
    attacks_taken = 0
    attack_results = []
    shuffles = 0
    number_of_advantage = []

    while(played_rounds <= player.round_per_game):
        new_results, new_rounds, new_attacks, attack_deck, advantage_tracker = \
            play_until_shuffle(attack_deck, player)

        played_rounds += new_rounds
        attacks_taken += new_attacks
        attack_results += new_results
        shuffles += 1
        number_of_advantage += advantage_tracker

   # process_attack_results(attack_results)
    return attack_results, played_rounds, attacks_taken, shuffles, number_of_advantage

def play_num_games(num_games, player):
    played_rounds = 0
    attacks_taken = 0
    attack_results = []
    shuffles = 0

    for i in range(num_games):
        new_results, new_rounds, new_attacks, new_shuffles, number_of_advantage = \
            play_num_rounds_without_reset(player)
        played_rounds += new_rounds
        attacks_taken += new_attacks
        attack_results += new_results
        shuffles += new_shuffles

    process_attack_results(attack_results)

    advantage_distribution = [number_of_advantage.count(-1)/len(number_of_advantage)]
    advantage_distribution.append(number_of_advantage.count(0)/len(number_of_advantage))
    advantage_distribution.append(number_of_advantage.count(1)/len(number_of_advantage)) 
    
    print('Played ' + str(played_rounds) + ' rounds, and made ' + str(attacks_taken) + ' attacks')
    print('Shuffled ' + str(shuffles) + ' times.')
    print('Averaged ' + str(attacks_taken/shuffles) + ' attacks per shuffle!')
    print('Advantage distribution was: ' + str(advantage_distribution))
    return


test_player = Player(player_definition)
play_num_games(10000, test_player)

##test_dist = [0, 0.25, 0.5]
##results = []
##for i in range(100000):
##    results.append(determine_number_attacks(test_dist))
##
##n = len(results)
##print('Percent of ' + '1' + ' attacks: ' + str(results.count(1)/n))
##print('Percent of ' + '2' + ' attacks: ' + str(results.count(2)/n))
##print('Percent of ' + '3' + ' attacks: ' + str(results.count(3)/n))
