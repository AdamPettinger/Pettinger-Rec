from collections import Counter 

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
    def __init__(self, number, card_type, conditions):
        self.value = number
        self.type = card_type
        self.conditions = conditions
        self.remove_duplicate_conditions()

    def remove_duplicate_conditions(self):
        list_of_allowed_duplicates = ['Push', 'Pull', 'Pierce',
                                      'Target', 'Curse', 'Bless']

        count_dict = Counter(self.conditions)
        print(count_dict)
        self.conditions = list(set(self.conditions))
        for cond in count_dict:
            if cond in list_of_allowed_duplicates:
                for i in range(count_dict[cond] - 1):
                    self.conditions.append(cond)

    def __str__(self):
        if (self.type == "Miss" or self.type == "Critical" or
            self.type == "Curse" or self.type == "Bless"):
            pre_string = str(self.value) + ", " + self.type
        else:
            pre_string = str(self.value)

        return (pre_string + " " + str(self.conditions))
                
            
##        if (self.type == "Miss" or self.type == "Critical" or
##            self.type == "Curse" or self.type == "Bless"):
##            return self.type
##
##        if len(self.conditions) == 0:
##            return str(self.value)
##        
##        cond_str = " with "
##        for i in self.conditions:
##            cond_str += i + " and "
##
##        if cond_str.endswith(' and '):
##            cond_str = cond_str[:-5]
##
##        return (str(self.value) + cond_str)
##            
