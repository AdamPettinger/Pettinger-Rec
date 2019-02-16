deck_definition = {
    "Special" : ["Miss", "Critical"], # Put the miss, critical, bless, and curses here
    "Rolling" : ["Push", "Push"], #Put all rolling cards here, with [1, 1] for values and ["Earth", "Push"] for conditions
    -2 : [""], # Put each -2 card here, with a condition applied as ["Push", "Earth"]. If no condition, leave ["", ""] for counting purposes. Don't include rolling -2's
    -1 : ["", "", "", "", ""],
    0 : ["", "", "", "", "", "", "Target", "Target"],
    1 : ["", "", "", "", "", "Push", "Push", "Push", "Push"],
    2 : [""]
}
