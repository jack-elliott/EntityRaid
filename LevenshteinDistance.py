# Import the respective libraries
from Levenshtein import distance as lev
import phonetics
import pandas as pd

def convertTuple(tup):

    # initialize an empty string
    str = ''
    for item in tup:
        str = str + item

    return str


def keylooper(key):
    # now check each key row
    for i in range(len(key)):

        # now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
        for j in range(len(key[i]) - 2):

            return key[i][j]


def compare(KeyName, AmbiguousName):


# This is a simple Levenshtein Distance calculation from the library. I print this value to confirm its validity
    LevenshteinDistance = lev(KeyName, AmbiguousName)

# This calculates the phonetic key according to the double metaphone for the KEY name
    PhoneticCodeKey = phonetics.dmetaphone(KeyName)

# This calculates the phonetic key according to the double metaphone for the AMBIGUOUS name
    PhoneticCodeAmbiguous = phonetics.dmetaphone(AmbiguousName)

    PhoneticCodeKey = convertTuple(PhoneticCodeKey)
    PhoneticCodeAmbiguous = convertTuple(PhoneticCodeAmbiguous)

    PhoneticCodeKey = PhoneticCodeKey.lower()
    PhoneticCodeKey = PhoneticCodeKey.replace(" ", "")

    PhoneticCodeAmbiguous = PhoneticCodeAmbiguous.lower()
    PhoneticCodeAmbiguous = PhoneticCodeAmbiguous.replace(" ", "")

    PhoneticDifference = lev(PhoneticCodeKey, PhoneticCodeAmbiguous)

    return [LevenshteinDistance, PhoneticDifference]

def compareKeytoData(keyLocation, dataFileLocation):
    # read in the key file to a list


    key = pd.read_csv(keyLocation, header=None)
    key = key.values.tolist()

    # read in the data file of interest to a list
    data = pd.read_csv(dataFileLocation, header=None)
    data = data.values.tolist()

    for a in range(len(data)):
        for b in range(len(data[0])):
            if isinstance(data[a][b], str):
                data[a][b] = data[a][b].lower()

    CompareList = []

    for o in range(len(data) - 1):
        for p in range(0, len(data[0]) - 1, 2): # This is the number of columns of interaction data containing peer names divided by 2
            #if isinstance(data[i][p], str): # Is this even working?

            for i in range(len(key)):
                    # now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
                for j in range(0, len(key[i]) - 1, 2):

                    AmbiguousName = [data[o+1][p+1], data[o+1][p+2]]

                    KeyName = [key[i][j+1], key[i][j+2]]

                    if AmbiguousName[0].isalpha() and AmbiguousName[1].isalpha():

                        ComparisonScoreFirstName = compare(KeyName[0], AmbiguousName[0])

                        ComparisonScoreLastName = compare(KeyName[1], AmbiguousName[1])

                        CompareList.append([KeyName[0], KeyName[1], AmbiguousName[0], AmbiguousName[1],
                                            ComparisonScoreFirstName[0], ComparisonScoreLastName[1],
                                            ComparisonScoreLastName[0], ComparisonScoreLastName[1]])

    # Put titles on the "CompareList" sheet
    CompareList.insert(0, ["Key First Name", "Key Last Name", "Ambiguous First Name",
                           "Ambiguous Last Name", "First Name: LD", "First Name: Metaphone",
                           "Last Name: LD", "Last Name: Metaphone"])

    # Write the "CompareList" to a csv file
    import csv
    with open('CompareListTrial12.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(CompareList)

    # spit these out so we can check to make sure deals work
    return CompareList


# This should be the absolute path file location of the qualtrics data file
dataFileLocation = '/Users/adamweaver/Desktop/SNA/SyntheticInteractionDataNumbers.csv'

# This should be the file location on your computer of the key .csv
keyLocation = '/Users/adamweaver/Desktop/SNA/SyntheticKey(Fall2022).csv'

compareKeytoData(keyLocation, dataFileLocation)








   # RemainingNames = []

  #  for i in range(len(data) - 1):
        # In this case, the names are in the zero column. This will change depending on the survey data formatting.
       # RemainingNames.append([data[1 + i][0]])
#
    # Split the participant Names into First Name/Last Name components
  #  dfParticipantNames = pd.DataFrame(ParticipantNames)
  #  dfParticipantNames[[0, 1]] = dfParticipantNames[0].str.split(' ', expand=True)
  #  ParticipantNames = dfParticipantNames.values.tolist()

    # loop through each of the raw data rows
   # for l in range(len(ParticipantNames)):

        # loop through each raw data column (set of names) corresponding to a given name not, first names are in cols 1,3,5,... last names col. 2,4,6,...
       # for m in range(len(ParticipantNames[l]) - 1):

            # identify the name to be checked for in the key
          #  ParticipantName = [ParticipantNames[l][m], ParticipantNames[l][m + 1]]

            # now run the sub-routine to see if the name is in the key
           # check = looper(ParticipantName, key)

            # If the name is not in the key, add the name to the key
          #  if check:
            #    key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])
# This if statement serves as the consolidation parameters.
# Eventually, I want to confirm the effectiveness of these measures through reading related research
#if PhoneticCodeKey == PhoneticCodeAmbiguous or LevenshteinDistance == 1:
   # print("Consolidate")

# If the name doesn't meet our consolidation parameters, it will get send to a clustering process, right?
#else:
   # print("Send to hierarchical clustering??")

# QUESTIONS:
# 1. The Levenshtein Distance is great, but doesn't account for potential nicknames
#              -We could use a double Levenshtein Distance calculation. This would include:
#                   Comparing last names with a Levenshtein Distance, then
#                   If this yields a distance of one, save these string values in a list
#                   We then could compare just the first letter of the first name to see if they match
#                   ...if they do, we could either:
#                           -Consolidate
#                           -Use this information in the clustering process?




