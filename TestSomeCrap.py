from Levenshtein import distance as lev
import phonetics
import pandas as pd

def convertTuple(tup):

    # initialize an empty string
    str = ''
    for item in tup:
        str = str + item

    return str


score = lev("Adam Weaver", "Adumb Weever")
print(score)

