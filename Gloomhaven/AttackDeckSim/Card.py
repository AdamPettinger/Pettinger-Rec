class AttackCard:
    # number = integer, condition = string
    # critical = "Miss" || "Critical", rolling = boolean
    def __init__(self, number, condition, critical, rolling):
        self.value = number
        self.is_rolling = rolling
        self.condition = condition

        if (critical == "Miss" or critical == "Critical" or
            critical == "Curse" or critical == "Bless"):
            self.type = critical
        else:
            self.type = "Normal"

    def __str__(self):
        if (self.type != "Normal"):
            return self.type
        
        if self.is_rolling:
            pre_str = "Rolling "
        else:
            pre_str = ""

        if self.condition:
            post_str = ", with "
        else:
            post_str = ""

        output = pre_str + str(self.value) + post_str + self.condition
        return output

    def reshuffle(self):
        return (self.type == "Critical" or self.type == "Miss")

class ComboCard:
    def __init__(self, single_card, attack_card, number, card_type, conditions):
        if single_card:
            self.value = attack_card.value
            self.type = attack_card.type
            self.conditions = [""]
            self.conditions[0] = attack_card.condition

        else:
            self.value = number
            self.type = card_type
            self.conditions = conditions
            self.remove_duplicate_conditions()

    def remove_duplicate_conditions(self):
        list_of_allowed_duplicates = ['Push', 'Pull', 'Pierce',
                                      'Target', 'Curse', 'Bless']

        unique_conditions = list(set(self.conditions))
        new_conditions = list(set(self.conditions))

        for c in unique_conditions:
            if c in list_of_allowed_duplicates:
                num_to_add = self.conditions.count(c) - 1
                for i in range(num_to_add):
                    new_conditions.append(c)

        self.conditions = new_conditions

    def __str__(self):
        if (self.type == "Miss" or self.type == "Critical" or
            self.type == "Curse" or self.type == "Bless" or
            self.type == "Advantaged Miss" or self.type == "Super Critical" or
            self.type == "Disadvantaged Critical"):
            pre_string = str(self.value) + ", " + self.type
        else:
            pre_string = str(self.value)

        full_string = (pre_string + " " + str(self.conditions))
        if full_string.endswith("['']"):
            full_string = full_string[:-4]
        elif full_string.endswith("[]"):
            full_string = full_string[:-2]

        return full_string

condition_dictionary = {
    "Push" : 0,
    "Pull" : 0,
    "Pierce" : 0,
    "Target" : 0,
    "Poison" : 0,
    "Wound" : 0,
    "Immobilize" : 0,
    "Disarm" : 0,
    "Stun" : 0,
    "Muddle" : 0,
    "Curse" : 0,
    "Invisible" : 0,
    "Strengthen" : 0,
    "Bless" : 0
}

special_dictionary = {
    "Miss" : 0,
    "Critical" : 0,
    "Curse" : 0,
    "Bless" : 0,
    "Advantaged Miss" : 0, # Rolling + Miss while advantage
    "Disadvantaged Critical" : 0, # Rolling + Crit while disadvantage
    "Super Critical" : [] # Rolling Crit Advantage, track each ones +value
}

class Player:
    def __init__(self, player_dict):
        self.round_per_game = player_dict["Rounds per Game"]
        self.advantage_dist = player_dict["Advantage Distribution"]
        self.num_attacks_dist = player_dict["Number of Attacks Distribution"]
        self.starting_curses = player_dict["Number of Starting Curses"]
        self.starting_blesses = player_dict["Number of Starting Blesses"]
        self.curse_chance = player_dict["Likelihood of getting Cursed"]
        self.bless_chance = player_dict["Likelihood of getting Blessed"]
        
