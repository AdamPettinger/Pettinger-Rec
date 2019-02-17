deck_definition = {
    "Special" : ["Miss", "Critical"], # Put the miss, critical, bless, and curses here
    "Rolling" : [], #Put all rolling cards here, with [1, 1] for values and ["Earth", "Push"] for conditions
    -2 : [""], # Put each -2 card here, with a condition applied as ["Push", "Earth"]. If no condition, leave ["", ""] for counting purposes. Don't include rolling -2's
    -1 : ["", "", "", "", ""],
    0 : ["", "", "", "", "", ""],
    1 : ["", "", "", "", ""],
    2 : [""]
}

player_definition = {
    "Rounds per Game" : 15,
    "Advantage Distribution" : [0.1, 0.8, 0.1],
    "Number of Attacks Distribution" : [0.75, 0.25, 0],
    "Number of Starting Curses" : 0,
    "Number of Starting Blesses" : 0,
    "Likelihood of getting Cursed": 0,
    "Likelihood of getting Blessed": 0
}
