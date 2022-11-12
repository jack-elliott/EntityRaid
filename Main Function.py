# ============================================ DEFINE FUNCTIONS ====================================================== #
# SOCIAL NETWORK DISAMBIGUATION

# INSTRUCTIONS AND IMPLICATIONS:


#    Key formatting and positioning should be exactly similar to ours
#    Interaction data can vary in positioning, but not in formatting
#    REGISTRY IS FORMATTED WITH FIRST AND LAST NAME IN THE 0th COLUMN WITH A SPACE IN BETWEEN THEM
#    ASSUMES THAT BOTH PEER COLUMN GROUPS ARE THE SAME SIZE

import os

# USER INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# This should be the absolute path file location of the qualtrics data file

######### JACK LOCATION ######
#dataFileLocation = r'C:/Users/A02234125/Desktop/ActualSurveyData.csv'

# This should be the file location on your computer of the key .csv
#keyLocation = r'C:/Users/A02234125/Desktop/ActualKey.csv'

# This should be the absolute path file location of the registry data file
#registryLocation = r'C:/Users/A02234125/Desktop/ActualRoster.csv'

######### ADAM LOCATION ######
#dataFileLocation = '/Users/adamweaver/Documents/ActualSurveyData(09:28:2022).csv'

# This should be the file location on your computer of the key .csv
#keyLocation = '/Users/adamweaver/Desktop/SNA/ActualKey.csv'

# This should be the absolute path file location of the registry data file
#registryLocation = '/Users/adamweaver/Desktop/SNA/ActualRoster(09:28:2022).csv'

##########

## ADAM SYNTHETIC LOCATION:
dataFileLocation = '/Users/adamweaver/Desktop/SNA/SyntheticInteractionData.csv'

# This should be the file location on your computer of the key .csv
keyLocation = '/Users/adamweaver/Desktop/SNA/SyntheticKey(Fall2022).csv'

# This should be the absolute path file location of the registry data file
registryLocation = '/Users/adamweaver/Desktop/SNA/SyntheticRegistry.csv'

###

##### REAL DATA VALUES ###
#ParticipantColumn = 21
#NicknameColumn = 25
#PeerColumnGroup1 = [26, 45]
#PeerColumnGroup2 = [87, 106]
#RowStart = 3
#RegistryRowStart = 2

#testNumber = 53

#####
## SYNTHETIC DATA VALUES ###
ParticipantColumn = 0
NicknameColumn = 1
PeerColumnGroup1 = [2, 13]
PeerColumnGroup2 = 0
RowStart = 3
RegistryRowStart = 2

testNumber = 54

# =============================================================================
# cwd = os.getcwd()
# print(dataFileLocation)
# =============================================================================

# END USER INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def looper(ParticipantName, key):
    # now check each key row
    for i in range(len(key)):

        # now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
        for j in range(len(key[i]) - 2):

            # Check the first name in the key
            if ParticipantName[0] == key[i][j + 1]:

                # Check the second name IF the first name matches
                if ParticipantName[1] == key[i][j + 2]:
                    # If the name is already in the key, return false (makes sense later)
                    return False

    # if the name was not already in the key (made it here), return true
    return True

def keyPosition(ParticipantName, key):
    # now check each key row
    for i in range(len(key)):

        # now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
        for j in range(len(key[i]) - 2):

            # Check the first name in the key
            if ParticipantName[0] == key[i][j + 1]:

                # Check the second name IF the first name matches
                if ParticipantName[1] == key[i][j + 2]:
                    # If the name is already in the key, return location
                    return key[i][0] - 1

    # if the name was not already in the key (made it here), return true
    return True

def addRegistryNames(registryLocation):

    # import respective libraries
    import pandas as pd

    # read in the key file to a list
    key = [[]]

    # read the registry file to a list
    registry = pd.read_csv(registryLocation, header=None)
    registry = registry.values.tolist()


    firstcolumn = [i[0] for i in registry]
    firstcolumnsplit = []
    for names in firstcolumn:
        newcolumns = names.split(' ', 1)
        firstcolumnsplit.append(newcolumns)

    registry = firstcolumnsplit

    # Turn the registry to all lowercase characters
    for a in range(len(registry)):
        for b in range(len(registry[0])):
            if isinstance(registry[a][b], str):
                registry[a][b] = registry[a][b].lower()

# Set new lists for a registry without duplicates (NewRegistry) and a place to record duplicate names (Duplicates)
    NewRegistry = []
    Duplicates = []

# Remove duplicate names from the registry to make NewRegistry, and record duplicates in a list
    for i in registry:
        if i not in NewRegistry:
            NewRegistry.append(i)
        else:
            Duplicates.append(i)

    print("There are", len(Duplicates), "duplicate names in the registry. These include:", Duplicates)
# If we want to export the duplicate names, we have to do it here (duplicates list is cleared on Line 40)
# Remove any names that had duplicates using the duplicates list and the NewRegistry
    FinalRegistry = [x for x in NewRegistry if not x in Duplicates or Duplicates.remove(x)]

    def spaceCounter(string):

        # counter
        count = 0

        # loop for search each index
        for i in range(0, len(string)):

            # Check each char
            # is blank or not
            if string[i] == " ":
                count += 1

        return count

    def hyphenDetector(string):
        for i in range(0, len(string)):
            if string[i] == '-':
                return True

    MultipleLastNames = []

    FinalRegistry.pop(RegistryRowStart - 2)

    for name in FinalRegistry:
        spaceCount = spaceCounter(name[1])
        hyphen = hyphenDetector(name[1])
        if spaceCount >= 1:
            MultipleLastNames.append(name)
        if hyphen:
            MultipleLastNames.append(name)


    for names in MultipleLastNames:
        if names in FinalRegistry:
            FinalRegistry.remove(names)

    print("There are", len(MultipleLastNames), "students with multiple last names. These include:", MultipleLastNames)
    # WE PROBABLY WANT TO REMOVE HYPHENATED NAMES/DOUBLE LAST NAMES HERE!

    print("There are", len(FinalRegistry), "names in the registry that have been added to the key.")
    for l in range(len(FinalRegistry)):
        for m in range(len(FinalRegistry[l]) - 1):

            # identify the name to be checked for in the key
            ParticipantName = [FinalRegistry[l][m], FinalRegistry[l][m + 1]]

            # now run the sub-routine to see if the name is in the key
            check = looper(ParticipantName, key)

            # If the name is not in the key, add the name to the key
            if check:
                key.append([len(key), FinalRegistry[l][m], FinalRegistry[l][m + 1]])

    import csv
    with open('Key_Registry'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(key)

    # spit the key out
    return key

def addParticipantsNames(keyLocation, dataFileLocation):
    # read in the key file to a list

    import pandas as pd
    key = pd.read_csv(keyLocation, header=None, engine='python')
    key.fillna('none', inplace=True)
    key = key.values.tolist()

    # read in the data file of interest to a list
    data = pd.read_csv(dataFileLocation, header=None)
    data = data.values.tolist()

    # Convert all of the data strings to just lowercase and remove all white space to make life easier
    for i in range(len(data)):  # loop through the whole list of data
        for j in range(len(data[0])):  # loop through each element per row
            if isinstance(data[i][j], str):
                data[i][j] = data[i][j].lower()

    ParticipantNames = []

    for i in range(len(data) - RowStart):
        # In this case, the names are in the zero column. This will change depending on the survey data formatting.
        ParticipantNames.append([data[RowStart + i][ParticipantColumn], data[RowStart + i][NicknameColumn]])

    # Split the participant Names into First Name/Last Name components

    dfParticipantNames = pd.DataFrame(ParticipantNames)
    dfParticipantNames[2] = dfParticipantNames[1]
    dfSplit = dfParticipantNames[0].str.split(' ', expand=True)
    dfParticipantNames[0] = dfSplit[0]
    dfParticipantNames[1] = dfSplit[1]
    ParticipantNames = dfParticipantNames.values.tolist()

    for h in range(len(key)):
        for u in range(len(key[h])-1):
            key[h][u+1] = key[h][u+1].lower()
            if key[h][u] == 'None':
                key[h][u] = key[h][u].replace('None', 'none')

    newNicknameColumn = 2

    # loop through each of the raw data rows
    for l in range(len(ParticipantNames)):

        # loop through each raw data column (set of names) corresponding to a given name not,
        # first names are in cols 1,3,5,... last names col. 2,4,6,...
        for m in range(len(ParticipantNames[0]) - 1):

            # identify the name to be checked for in the key
            ParticipantName = [ParticipantNames[l][0], ParticipantNames[l][1]]

# ==================================================NICKNAMES========================================================= #

            if ParticipantNames[l][newNicknameColumn] != "N/A" or "NA" or "na" or "n/a" or "none" or "None" or "Nope":
                if not isinstance(ParticipantNames[l][newNicknameColumn], float):

# --------------------------------------------- SEPARATED BY COMMA -----------------------------------------------------
                    if "," in ParticipantNames[l][newNicknameColumn]:

                        ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].replace(", ", ",")
                        SplitComma = ParticipantNames[l][newNicknameColumn].split(",")

                        check = looper(ParticipantName, key)
                        location = keyPosition(ParticipantName, key)

                        if check:

                            key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])

                            for name in SplitComma:

                                if " " in name:
                                    SplitCommaSpace = name.split(" ")

                                    if SplitCommaSpace[1] != ParticipantNames[l][1]:

                                        key[len(key) - 1].append(name)
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                        key[len(key) - 1].append(SplitCommaSpace[0])
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                        key[len(key) - 1].append(SplitCommaSpace[1])
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                    else:

                                        key[len(key) - 1].append(SplitCommaSpace[0])
                                        key[len(key) - 1].append(SplitCommaSpace[1])

                                else:

                                    key[len(key)-1].append(name)
                                    key[len(key)-1].append(ParticipantNames[l][m+1])

                        else:

                            ColumnLocationList = []
                            for i in range(len(key[location])):
                                if key[location][i] == "none":
                                    ColumnLocation = i
                                    ColumnLocationList.append(ColumnLocation)
                            if ColumnLocationList:
                                ActualColumnLocation = min(ColumnLocationList)

                            if not ColumnLocationList:
                                ActualColumnLocation = 1

                            if ParticipantNames[l][newNicknameColumn] not in key[location]:

                                for name in SplitComma:

                                    if " " in name:
                                        SplitCommaSpace = name.split(" ")
                                        if SplitCommaSpace[1] != ParticipantNames[l][1]:

                                            key[location].insert(ActualColumnLocation, name)
                                            key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                                            key[location].insert(ActualColumnLocation + 2, SplitCommaSpace[0])
                                            key[location].insert(ActualColumnLocation + 3, ParticipantNames[l][1])

                                            key[location].insert(ActualColumnLocation + 4, SplitCommaSpace[1])
                                            key[location].insert(ActualColumnLocation + 5, ParticipantNames[l][1])

                                        else:

                                            key[location].insert(ActualColumnLocation, SplitCommaSpace[0])
                                            key[location].insert(ActualColumnLocation + 1, SplitCommaSpace[1])

                                    else:

                                        key[location].insert(ActualColumnLocation, name)
                                        key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

    # -------------------------------------------- SEPARATED BY AN OR ------------------------------------------------------

                    if "or" in ParticipantNames[l][newNicknameColumn]:

                        ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].replace(" or ", "or")
                        SplitOr = ParticipantNames[l][newNicknameColumn].split('or')

                        check = looper(ParticipantName, key)
                        location = keyPosition(ParticipantName, key)

                        if check:

                            key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])

                            for name in SplitOr:

                                if " " in name:
                                    SplitOrSpace = name.split(" ")

                                    if SplitOrSpace[1] != ParticipantNames[l][1]:

                                        key[len(key) - 1].append(name)
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                        key[len(key) - 1].append(SplitOrSpace[0])
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                        key[len(key) - 1].append(SplitOrSpace[1])
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                    else:
                                        key[len(key) - 1].append(SplitOrSpace[0])
                                        key[len(key) - 1].append(SplitOrSpace[1])

                                else:

                                    key[len(key) - 1].append(name)
                                    key[len(key) - 1].append(ParticipantNames[l][1])

                        else:

                            ColumnLocationList = []
                            for i in range(len(key[location])):
                                if key[location][i] == "none":
                                    ColumnLocation = i
                                    ColumnLocationList.append(ColumnLocation)

                            if ColumnLocationList != []:
                                ActualColumnLocation = min(ColumnLocationList)

                            if ParticipantNames[l][newNicknameColumn] not in key[location]:

                                for name in SplitOr:

                                    if " " in name:

                                        SplitOrSpace = name.split(" ")

                                        if SplitOrSpace[1] != ParticipantNames[l][1]:

                                            key[location].insert(ActualColumnLocation, name)
                                            key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                                            key[location].insert(ActualColumnLocation + 2, SplitOrSpace[0])
                                            key[location].insert(ActualColumnLocation + 3, ParticipantNames[l][1])

                                            key[location].insert(ActualColumnLocation + 4, SplitOrSpace[1])
                                            key[location].insert(ActualColumnLocation + 5, ParticipantNames[l][1])

                                        else:
                                            key[location].insert(ActualColumnLocation, SplitOrSpace[0])
                                            key[location].insert(ActualColumnLocation + 1, SplitOrSpace[1])

                                    else:

                                        key[location].insert(ActualColumnLocation, name)
                                        key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                        ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].replace("or", " or ")

    #  ------------------------------------JUST ONE NICKNAME-----------------------------------------------------------#

                    if "," not in ParticipantNames[l][newNicknameColumn] and " " not in ParticipantNames[l][newNicknameColumn]:

                        check = looper(ParticipantName, key)
                        location = keyPosition([ParticipantNames[l][m], ParticipantNames[l][m + 1]], key)

                        checktwo = looper([ParticipantNames[l][newNicknameColumn], ParticipantName[1]], key)
                        locationtwo = keyPosition([ParticipantNames[l][newNicknameColumn], ParticipantNames[1]], key)

                        print(ParticipantName)
                        print(ParticipantNames[l][newNicknameColumn])
                      #  print(check)
                      #  print(checktwo)

                        if not check: # if name is in the key, but ...
                            if checktwo: # ... nickname is not in the key
                                ColumnLocationList = []
                                for i in range(len(key[location])):
                                    if key[location][i] == "none":
                                        ColumnLocation = i
                                        ColumnLocationList.append(ColumnLocation)
                                    else:
                                        ActualColumnLocation = 3
                                if ColumnLocationList != []:
                                    ActualColumnLocation = min(ColumnLocationList)

                               # print(ParticipantNames[l][0])
                               # print(ParticipantNames[l][1])
                               # print(locationtwo)
                               # print(location)
                                if not isinstance(location, float):
                                    print("LOCATION IS", location)
                                    key[location].insert(ActualColumnLocation, ParticipantNames[l][newNicknameColumn])
                                    key[location].insert(ActualColumnLocation + 1, ParticipantName[1])

                        if checktwo: # if nickname is not in the key
                            if check: # AND the name is not already in the key
                                key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1],
                                       ParticipantNames[l][newNicknameColumn], ParticipantNames[l][1]])

# ===============================================END NICKNAME========================================================= #
            # now run the sub-routine to see if the name is in the key
            check = looper(ParticipantName, key)
            if not isinstance(ParticipantNames[l][newNicknameColumn], float):
                if "," not in ParticipantNames[l][newNicknameColumn] and " " not in ParticipantNames[l][newNicknameColumn]:
                    checktwo = looper([ParticipantNames[l][newNicknameColumn], ParticipantNames[l][1]], key)
                else:
                    checktwo = True
            else:
                checktwo = True
            # If the name is not in the key, add the name to the key
            if check and checktwo:
                key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])

    LengthList = []
    for i in range(len(key)):
        LengthList.append(len(key[i]))
    MaxColumns = max(LengthList)
    for i in range(len(key)):
        if len(key[i]) < MaxColumns:
            for o in range(MaxColumns-len(key[i])):
                key[i].append("none")

    print('There are', len(ParticipantNames[0]), "participant names (not in the registry) that have been added to the key.")
    print("The total size of the key after being initialized is", len(key))

    import csv
    with open('KeyAfterParticipantNames'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(key)

    # spit the key out
    return key

def replacingFunc(dataFileLocation, keyLocation):
    # Import libraries necessary and assign aliases
    import pandas as pd

    # Read in the data file of interest to a list
    data = pd.read_csv(dataFileLocation, header=None)
    data = data.values.tolist()

    # Read in the key file to a list
    key = pd.read_csv(keyLocation, header=None)
    key = key.values.tolist()

    def alphaStrip(string):

        out = ""

        for i in range(len(string)):

            if string[i].isalpha():
                out = out + string[i]

        return out

    # Convert all of the data strings to just lowercase and remove all white space to make life easier
    for i in range(len(data)):  # loop through the whole list of data
        for j in range(len(data[0])):  # loop through each element per row
            if isinstance(data[i][j], str):  # check if each element is a string, if so convert to upper and remove whitespace
                data[i][j] = data[i][j].lower()
                data[i][j] = data[i][j].replace(" ", "")
                data[i][j] = alphaStrip(data[i][j])

    # Now, make the key all lowercase so that matching will work in the following logic
    for a in range(len(key)):
        for b in range(len(key[0])):
            if isinstance(key[a][b], str):
                key[a][b] = key[a][b].lower()

    # Loop through the key and data and replace accordingly
    resolvedcount = 0
# =============================================================================
#     import time
#     start = time.time()
# =============================================================================
    for i in range(RowStart, len(data)):#loop through every row of the raw data
        for s in range(PeerColumnGroup1[1]-PeerColumnGroup1[0]):
            for l in range(len(key)):
                for m in range(len(key[l]) - 2):
                    if isinstance(data[i][s+PeerColumnGroup1[0]], str) and isinstance(data[i][s+PeerColumnGroup1[0]+1], str):
                        if key[l][m + 1] and key[l][m + 2] != "none":
                            if data[i][s+PeerColumnGroup1[0]] == key[l][m + 1]:
                                if data[i][s+PeerColumnGroup1[0]+1] == key[l][m + 2]:
                                    resolvedcount += 1
                                    data[i][s + PeerColumnGroup1[0]] = key[l][0]
                                    data[i][s + PeerColumnGroup1[0] + 1] = key[l][0]
# =============================================================================
#                                     new = time.time()
#                                     timetoresolvesingle = new - start
#                                     print(timetoresolvesingle)
# =============================================================================
        if PeerColumnGroup2 != 0:
            for q in range(PeerColumnGroup2[1]-PeerColumnGroup2[0]):
                if isinstance(data[i][q + PeerColumnGroup2[0]], str) and isinstance(data[i][q + PeerColumnGroup2[0] + 1], str):
                    if key[l][m + 1] and key[l][m + 2] != "none":
                        if data[i][q + PeerColumnGroup2[0]] == key[l][m + 1]:
                            if data[i][q + PeerColumnGroup2[0] + 1] == key[l][m + 2]:
                                resolvedcount += 1
                                data[i][q + PeerColumnGroup1[0]] = key[l][0]
                                data[i][q + PeerColumnGroup1[0] + 1] = key[l][0]
#  --------------------------- REPLACE PARTICIPANT'S SELF REPORTED NAMES --------------------------------------------  #
                   # ParticipantSelfReportedNames = []
                #    KeyName = [key[l][m+1], key[l][m+2]]
                 #   if isinstance(KeyName[1], float):
                 #       ParticipantSelfReportedNames.append([key[l][m+1], key[l][m+2]])
                 #   if isinstance(KeyName[0], float):
                  #      ParticipantSelfReportedNames.append([key[l][m+1], key[l][m+2]])
                 #       print(KeyName[0])
                  #  if not isinstance(KeyName[1], float) and not isinstance(KeyName[0], float):
                   #     print("The data is now here")
                    #    KeyName[0] = ''.join(KeyName)
                    #    if data[i][ParticipantColumn] == KeyName[0]:
                     #       data[i][ParticipantColumn] = key[l][0]
                     #       resolvedcount += 1

    print("The number of names resolved in the exact replacement stage is:", resolvedcount)
   # print("Participants who did not report their last name are:", ParticipantSelfReportedNames)

    ambiguouscount = 0

# MAYBE ADD SOMETHING HERE ABOUT N/A string values
    for i in range(RowStart, len(data)):
        for j in range(PeerColumnGroup1[0], PeerColumnGroup1[1] + 1):
            if isinstance(data[i][j], str) and data[i][j] != "n/a" and data[i][j] != "nan" and data[i][j] != " ":
                ambiguouscount += 1
    if PeerColumnGroup2 != 0:
        for i in range(RowStart, len(data)):
            for j in range(PeerColumnGroup2[0], PeerColumnGroup2[1] + 1):
                if isinstance(data[i][j], str) and data[i][j] != "n/a" and data[i][j] != "nan" and data[i][j] != " ":
                    ambiguouscount += 1

    print("The number of remaining names (ambiguous) is:", (ambiguouscount/2))
    # write the data file to a .csv
    import csv
    with open('DataforComparison'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(data)

    # spit these out so we can check to make sure deals work
    return data

def convertTuple(tup):

    # initialize an empty string
    str = ''
    for item in tup:
        str = str + item

    return str

def compare(KeyName, AmbiguousName):

    from Levenshtein import distance as lev
    import phonetics
# This is a simple Levenshtein Distance calculation from the library. I print this value to confirm its validity
    print("KeyName is", KeyName)
    print("Ambiguous Name is", AmbiguousName)
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
    import pandas as pd
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

    for o in range(len(data) - RowStart):
        for p in range(PeerColumnGroup1[1] - PeerColumnGroup1[0] - 1): # This is the number of columns of interaction data containing peer names divided by 2

            for i in range(len(key)):
                    # now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
                for j in range(0, len(key[i]) - 1, 2):

                    AmbiguousName = [data[o+RowStart][p+PeerColumnGroup1[0]], data[o+RowStart][p+1+PeerColumnGroup1[0]]]

                    if PeerColumnGroup2 != 0:
                        AmbiguousName = [data[o+RowStart][p+PeerColumnGroup2[0]], data[o+RowStart][p+1+PeerColumnGroup2[0]]]

                    KeyName = [key[i][j+1], key[i][j+2]]

                    if isinstance(AmbiguousName[0], str) and isinstance(AmbiguousName[1], str):

                        if AmbiguousName[0].isalpha() and AmbiguousName[1].isalpha():

                            ComparisonScoreFirstName = compare(KeyName[0], AmbiguousName[0])

                            ComparisonScoreLastName = compare(KeyName[1], AmbiguousName[1])


                            if ComparisonScoreLastName[0] <= 2 and ComparisonScoreFirstName[0] <= 2 and ComparisonScoreLastName[1] <= 2 and ComparisonScoreFirstName[1] <= 2:

                                CompareList.append([KeyName[0], KeyName[1], AmbiguousName[0], AmbiguousName[1],
                                                    ComparisonScoreFirstName[0], ComparisonScoreLastName[1],
                                                    ComparisonScoreLastName[0], ComparisonScoreLastName[1]])



    # Put titles on the "CompareList" sheet
    CompareList.insert(0, ["Key First Name", "Key Last Name", "Ambiguous First Name",
                           "Ambiguous Last Name", "First Name: LD", "First Name: Metaphone",
                           "Last Name: LD", "Last Name: Metaphone"])


    List1 = list(range(PeerColumnGroup1[0], PeerColumnGroup1[1], 2))
    if PeerColumnGroup2 != 0:
        List2 = list(range(PeerColumnGroup2[0], PeerColumnGroup2[1], 2))
        PeerList = List1 + List2
    else:
        PeerList = List1

    AmbiguousList = []
    for n in range(RowStart, len(data)):
        for columns in PeerList:
            print("CHECK", data[n][columns])
            ambiguous = looper(data[n][columns], key)
            print(ambiguous)
            if ambiguous:
                if n < 10:
                    data[n][columns] = '0000' + str(n)
                    AmbiguousList.append([data[n][columns], ['0000' + str(n)]])
                if n >= 10:
                    data[n][columns] = '000' + str(n)
                    AmbiguousList.append([data[n][columns], ['000' + str(n)]])
                if n >= 100:
                    data[n][columns] = '00' + str(n)
                    AmbiguousList.append([data[n][columns], ['00' + str(n)]])
                if n >= 1000:
                    data[n][columns] = '0' + str(n)
                    AmbiguousList.append([data[n][columns], ['0' + str(n)]])

    EdgeList = []

    for i in range(RowStart, len(data)):
        for columns in PeerList:
            EdgeList.append([data[i][ParticipantColumn], data[i][columns]])

   # print(EdgeList)


    # Write the "CompareList" to a csv file
    import csv
    with open('CompleteTrialIteration'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
    
    #write the .csv
        writer.writerows(CompareList)
    
    #spit these out so we can check to make sure deals work
    return CompareList

########################################### MAIN FUNCTION LOGIC ########################################################


# EVENTUALLY I NEED TO MAKE COPIES OF THE REAL DATA HERE

#check if the output files exist (due to the testNumber already being used) If so, delete prior to writing new files
if os.path.isdir(str('Key_Registry'+str(testNumber)+'.csv')):
    
    os.remove(str('Key_Registry'+str(testNumber)+'.csv'))
    os.remove(str('KeyAfterParticipantNames'+str(testNumber)+'.csv'))
    os.remove(str('DataforComparison'+str(testNumber)+'.csv'))
    
    
#rite the output files to the working directory of main()
key = addRegistryNames(registryLocation)

keyLocation = str('Key_Registry'+str(testNumber)+'.csv')

key = addParticipantsNames(keyLocation, dataFileLocation)

keyLocation = str('KeyAfterParticipantNames'+str(testNumber)+'.csv')

data = replacingFunc(dataFileLocation, keyLocation)

dataFileLocation = str('DataforComparison'+str(testNumber)+'.csv')

#keyLocation = '/Users/adamweaver/Documents/GitHub/KeyAfterParticipantNames43.csv'

#dataFileLocaiton = '/Users/adamweaver/Documents/GitHub/DataforComparison43.csv'

compareKeytoData(keyLocation, dataFileLocation)

# Check what the synthetic data looks like and if the ambiguous list is getting added correctly (not ever being false)
# THE AMBIGUOUS LIST NEEDS TO BE EVERY TWO!
# Why is it every two?
# Get replacing participant names to work

