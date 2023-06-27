# ============================================ DEFINE FUNCTIONS ====================================================== #
# SOCIAL NETWORK DISAMBIGUATION

# INSTRUCTIONS AND IMPLICATIONS:


#    Key formatting and positioning should be exactly similar to ours
#    Interaction data can vary in positioning, but not in formatting
#    REGISTRY IS FORMATTED WITH FIRST AND LAST NAME IN THE 0th COLUMN WITH A SPACE IN BETWEEN THEM
#    ASSUMES THAT BOTH PEER COLUMN GROUPS ARE THE SAME SIZE

import os

# USER INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## SYNTHETIC SAMPLE INPUTS:
dataFileLocation = 'SyntheticInteractionData.csv'

# This should be the file location on your computer of the key .csv
keyLocation = 'SyntheticKey.csv'

# This should be the absolute path file location of the registry data file
registryLocation = 'SyntheticRegistry.csv'

###

##### REAL DATA VALUES ###
ParticipantColumn = 21
NicknameColumn = 25
ANumberColumn = 24
newANumberColumn = 3
newParticipantNamesColumns = [0, 1]
PeerColumnGroup1 = [26, 45]
PeerColumnGroup2 = [87, 106]
RowStart = 3
RegistryRowStart = 2

StringLastNameThresehold = 2
StringFirstNameThresehold = 3
PhoneticLastNameThresehold = 1
PhoneticFirstNameThresehold = 1

ConsolidateStringLastNameThresehold = 2
ConsolidateStringFirstNameThresehold = 3
ConsolidatePhoneticLastNameThresehold = 1
ConsolidatePhoneticFirstNameThresehold = 1

testNumber = 127

#10:50 is 30 mins inrefdt

#####
## SYNTHETIC DATA VALUES ###
#ParticipantColumn = 0
#NicknameColumn = 1
#PeerColumnGroup1 = [2, 13]
#PeerColumnGroup2 = 0
#RowStart = 3
#RegistryRowStart = 2

#testNumber = 70

# =============================================================================
# cwd = os.getcwd()
# print(dataFileLocation)
# =============================================================================

# END USER INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np

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
                    return i

    # if the name was not already in the key (made it here), return true
    return True

def keyPositionANUMBER(Anumber, key):
    # now check each key row
    for i in range(len(key)):

        # Check the first name in the key
        if Anumber == key[i][0]:

            return float(i + 1)

    # if the name was not already in the key (made it here), return true
    return True

def registrarData(ANumber, keyentry, ParticipantNameList):
    # now check each key row

    for i in range(len(ParticipantNameList)):

        anumber = ParticipantNameList[i][newANumberColumn]
        if not isinstance(anumber, float):
            if anumber[0] == "a" and len(anumber) == 9:
                ParticipantNameList[i][newANumberColumn] = anumber[1] + anumber[2] + anumber[3] + anumber[4] + anumber[5] + anumber[6] + anumber[7] + anumber[8]

        if anumber == ANumber:
            KeyPosition = keyPositionANUMBER(ANumber, keyentry)
            if isinstance(KeyPosition, float):
                return int(KeyPosition)

    return False

def edgeToAdjacency(edgeList, nodeCount="Auto"):
    # find the necessary size of the adjacency matrix,
    # NOTE if isolates are not within the max of the edge list, will be left out
    if nodeCount == "Auto":
        N = np.amax(edgeList)
        print("Automatic ", end="")
    else:
        N = nodeCount
        print("Manual ", end="")

    print("N = " + str(N))

    # initialize the NxN adjacency Matrix A
    A = np.zeros((N, N))

    # add the edges to A
    for i in range(len(edgeList)):
        for j in range(len(edgeList[i])):
            A[edgeList[i][0] - 1][edgeList[i][1] - 1] = 1

    return A

def concat_keyPosition(ParticipantName, key):
    # now check each key row
    for i in range(len(key)):

        # now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
        for j in range(len(key[i]) - 3):

            # Check the first name in the key
            concatenatedkeyname = str(key[i][j + 2]) + str(key[i][j + 3])

            if ParticipantName == concatenatedkeyname:

                return key[i][1] - 1

    # if the name was not already in the key (made it here), return true
    return True

def duplicates(key, ParticipantName):
    DuplicateRows = []
    for i in range(RowStart, len(key)):
        for j in range(len(key[0]) - 3):
            if key[i][j+2] == ParticipantName[0]:
                if key[i][j+3] == ParticipantName[1]:
                    DuplicateRows.append(i)

    return DuplicateRows

def removeDuplicatesFromKey(key):
    DuplicateRows = []
    DuplicateList = []
    OriginalLocations = []
    for i in range(len(key)):
        ParticipantNameRow = key[i]
        OriginalLocation = i
        OriginalLocations.append(OriginalLocation)
        for n in range(len(ParticipantNameRow) - 3):
            if ParticipantNameRow[n + 2] != 'none':
                if ParticipantNameRow[n + 3] != 'none':
                    ParticipantName = [ParticipantNameRow[n + 2], ParticipantNameRow[n + 3]]
                    DuplicateCheck = duplicates(key, ParticipantName)
                    newDuplicateCheck = []
                    Duplicates = []
                    for columns in DuplicateCheck:
                        if columns not in newDuplicateCheck:
                            newDuplicateCheck.append(columns)
                        else:
                            Duplicates.append(columns)
                    if OriginalLocation in newDuplicateCheck:
                        newDuplicateCheck.remove(OriginalLocation)
                    if len(newDuplicateCheck) > 0:
                        from Levenshtein import distance as lev
                        for i in range(len(newDuplicateCheck)):
                            if key[newDuplicateCheck[i]][0] != 'undefined' or ParticipantNameRow[0] != 'undefined':
                                ANumberStringSim = lev(key[newDuplicateCheck[i]][0], ParticipantNameRow[0])
                            else:
                                ANumberStringSim = 0
                            if ANumberStringSim < 3:
                                DuplicateRows.append(key[newDuplicateCheck[i]])
                    newDuplicateCheck.insert(0, OriginalLocation)
                    DuplicateList.append(newDuplicateCheck)

    newList = []
    for a in range(len(DuplicateList)):
        for b in range(len(DuplicateList[a]) - 1):
            for c in range(len(OriginalLocations)):
                if len(DuplicateList[a]) == 2:
                    if DuplicateList[a][b] > DuplicateList[a][b + 1]:
                        newList.append(DuplicateList[a][b])
                    else:
                        newList.append(DuplicateList[a][b + 1])
                if len(DuplicateList[a]) == 3:
                    if DuplicateList[a][b] > DuplicateList[a][b + 1] and DuplicateList[a][b] > DuplicateList[a][b + 2]:
                        newList.append(DuplicateList[a][b])
                    if DuplicateList[a][b + 1] > DuplicateList[a][b] and DuplicateList[a][b + 1] > DuplicateList[a][
                        b + 2]:
                        newList.append(DuplicateList[a][b + 1])
                    if DuplicateList[a][b + 2] > DuplicateList[a][b] and DuplicateList[a][b + 2] > DuplicateList[a][
                        b + 1]:
                        newList.append(DuplicateList[a][b + 2])

    finalDuplicateRowsList = []

    for column in newList:
        if column not in finalDuplicateRowsList:
            finalDuplicateRowsList.append(column)

    Remove = []
    for i in range(len(key)):
        for m in range(len(newList)):
            if i == int(newList[m]):
                Remove.append(key[i])

    for rows in Remove:
        if rows in key:
            key.remove(rows)

    return key

def addRegistryNames(registryLocation):

    # import respective libraries
    import pandas as pd

    # read in the key file to a list
    key = [[]]

    # read the registry file to a list
    registryone = pd.read_csv(registryLocation, header=None)
    registryone = registryone.values.tolist()


    firstcolumn = [i[0] for i in registryone]
    anumbercolumn = [i[3] for i in registryone]

    firstcolumnsplit = []
    for names in firstcolumn:
        newcolumns = names.split(' ', 1)
        firstcolumnsplit.append(newcolumns)

    for i in range(len(anumbercolumn)):
        firstcolumnsplit[i].insert(0, anumbercolumn[i])

    for i in range(len(firstcolumnsplit)):
        anumber = firstcolumnsplit[i][0]
        if anumber[0] == "A" and len(anumber) == 9:
            firstcolumnsplit[i][0] = anumber[1] + anumber[2] + anumber[3] + anumber[4] + anumber[5] + \
                                                    anumber[6] + anumber[7] + anumber[8]

    registry = firstcolumnsplit

    # Turn the registry to all lowercase characters
    for a in range(len(registry)):
        for b in range(len(registry[0])):
            if isinstance(registry[a][b], str):
                registry[a][b] = registry[a][b].lower()

# Set new lists for a registry without duplicates (NewRegistry) and a place to record duplicate names (Duplicates)

    RemainingNames = []
    Duplicates = []

# Remove duplicate names from the registry to make NewRegistry, and record duplicates in a list
    for row in firstcolumn:
        if row not in RemainingNames:
            RemainingNames.append(row)
        else:
            Duplicates.append(row)

    print("There are", len(Duplicates), "duplicate names in the registry. These include:", Duplicates)
# If we want to export the duplicate names, we have to do it here (duplicates list is cleared on Line 40)
# Remove any names that had duplicates using the duplicates list and the NewRegistry
    firstcolumnsplittwo = []
    DuplicateRegistryNames = []
    for names in RemainingNames:
        newcolumns = names.split(' ', 1)
        firstcolumnsplittwo.append(newcolumns)
        for i in range(len(registry)):
            if registry[i][1] == newcolumns[0] and registry[i][2] == newcolumns[1]:
                DuplicateRegistryNames.append(registry[i])

    for rows in DuplicateRegistryNames:
        if rows in registry:
            registry.remove(rows)

    FinalRegistry = registry

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

    LastNames = []
    for i in range(len(FinalRegistry)):
        LastNames.append(FinalRegistry[i][2])

    for name in LastNames:
        spaceCount = spaceCounter(name)
        hyphen = hyphenDetector(name)
        if spaceCount >= 1:
            MultipleLastNames.append(name)
        if hyphen:
            MultipleLastNames.append(name)

    MultipleLastNameRows = []
    for i in range(len(FinalRegistry)):
        if FinalRegistry[i][2] in MultipleLastNames:
            MultipleLastNameRows.append(FinalRegistry[i])

    for rows in MultipleLastNameRows:
        if rows in FinalRegistry:
            FinalRegistry.remove(rows)

    for rows in FinalRegistry:
        if rows[0] == ' undefined':
            FinalRegistry.remove(rows)

    global LengthofRegistry
    LengthofRegistry = len(FinalRegistry)

    print("There are", len(MultipleLastNames), "students with multiple last names. These include:", MultipleLastNameRows)
    # WE PROBABLY WANT TO REMOVE HYPHENATED NAMES/DOUBLE LAST NAMES HERE!

    print("There are", len(FinalRegistry), "names in the registry that have been added to the key.")
    for l in range(len(FinalRegistry)):
        for m in range(len(FinalRegistry[l]) - 1):

            Anumber = FinalRegistry[l][0]
            # identify the name to be checked for in the key
            ParticipantName = [FinalRegistry[l][1], FinalRegistry[l][2]]

            # now run the sub-routine to see if the name is in the key
            check = looper(ParticipantName, key)

            # If the name is not in the key, add the name to the key
            if check:
                key.append([Anumber, len(key), FinalRegistry[l][1], FinalRegistry[l][2]])

    import csv

    mypath = 'output/Iteration' + str(testNumber) + '/'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    with open(mypath + 'Key_Registry' + str(testNumber) + '.csv', 'w', encoding='UTF8', newline='') as f:
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

    for i in range(len(key)):  # loop through the whole list of data
        for j in range(len(key[0])):  # loop through each element per row
            if isinstance(key[i][j], str):
                key[i][j] = key[i][j].lower()

    ParticipantNames = []

    for i in range(len(data) - RowStart):
        if not isinstance(data[RowStart + i][ParticipantColumn], float):
            if data[RowStart + i][ParticipantColumn][0] == ' ':
                Name = data[RowStart + i][ParticipantColumn]
                StrLen = len(data[RowStart + i][ParticipantColumn])
                NameList = []
                for i in range(StrLen - 1):
                    NameList.append(Name[i + 1])
                stringreconstructed = ''.join(NameList)
                data[RowStart + i][ParticipantColumn] = stringreconstructed
            if '(' not in data[RowStart + i][ParticipantColumn]:
            # In this case, the names are in the zero column. This will change depending on the survey data formatting.
                ParticipantNames.append([data[RowStart + i][ParticipantColumn], data[RowStart + i][NicknameColumn], data[RowStart + i][ANumberColumn]])

    # Split the participant Names into First Name/Last Name components

    dfParticipantNames = pd.DataFrame(ParticipantNames)
    dfParticipantNames[3] = dfParticipantNames[2]
    dfParticipantNames[2] = dfParticipantNames[1]
    dfSplit = dfParticipantNames[0].str.split(' ', expand=True)
    dfParticipantNames[0] = dfSplit[0]
    dfParticipantNames[1] = dfSplit[1]
    ParticipantNames = dfParticipantNames.values.tolist()

    for rows in ParticipantNames:
        if isinstance(rows[1], str):
            if '-' in rows[1]:
                ParticipantNames.remove(rows)

    for rows in ParticipantNames:
        if isinstance(rows[1], str):
            if ' ' in rows[1]:
                ParticipantNames.remove(rows)

    for i in range(len(ParticipantNames)):
        anumber = ParticipantNames[i][newANumberColumn]
        if not isinstance(anumber, float):
            if anumber[0] == "a" and len(anumber) == 9:
                ParticipantNames[i][newANumberColumn] = anumber[1] + anumber[2] + anumber[3] + anumber[4] + anumber[5] + anumber[6] + anumber[7] + anumber[8]
            if anumber[0] == "a" and len(anumber) == 8:
                ParticipantNames[i][newANumberColumn] = anumber[1] + anumber[2] + anumber[3] + anumber[4] + anumber[5] + \
                                                        anumber[6] + anumber[7]
    for h in range(len(key)):
        for u in range(len(key[h])-2):
            key[h][u+2] = key[h][u+2].lower()
            if key[h][u] == 'None':
                key[h][u] = key[h][u].replace('None', 'none')

    newNicknameColumn = 2

    for i in range(len(ParticipantNames)):
        if isinstance(ParticipantNames[i][newNicknameColumn], str):
            if "." in ParticipantNames[i][newNicknameColumn]:
                ParticipantNames[i][newNicknameColumn] = ParticipantNames[i][newNicknameColumn].replace('.', ',')
            if ParticipantNames[i][newNicknameColumn][0] == "n" or "N":
                if ParticipantNames[i][newNicknameColumn][0] == "o":
                    if ParticipantNames[i][newNicknameColumn][0] == "n":
                        if ParticipantNames[i][newNicknameColumn][0] == "e":
                            ParticipantNames[i][newNicknameColumn] = 'none'

    SingleNameList = []
    AnumberCheck = ['filler', False]
    for l in range(len(ParticipantNames)):
        AnumberCheck = [ParticipantNames[l][newANumberColumn], False]
        for m in range(len(ParticipantNames[0]) - 1):
            ParticipantName = [ParticipantNames[l][0], ParticipantNames[l][1]]
            ANUMBER = ParticipantNames[l][newANumberColumn]
            nickname = ParticipantNames[l][newNicknameColumn]
            if ParticipantName[0] != '' and ParticipantName[1] != '':
                if isinstance(ANUMBER, str):
                    #if not isinstance(ParticipantNames[l][newNicknameColumn], float):
                    if not registrarData(ANUMBER, key, ParticipantNames):
                        key.append([ANUMBER, len(key) + 1, ParticipantName[0], ParticipantName[1]])
                        AnumberCheck = [ANUMBER, True]
                        if not isinstance(ParticipantNames[l][newNicknameColumn], float):
                            if "," in ParticipantNames[l][newNicknameColumn]:
                                SplitComma = ParticipantNames[l][newNicknameColumn].split(",")
                                for i in range(len(SplitComma)):
                                    SplitComma[i] = SplitComma[i].replace(" ", "")
                                for name in SplitComma:
                                    if " " in name:
                                        SplitCommaSpace = name.split(" ")
                                        if SplitCommaSpace[1] != ParticipantNames[l][1]:
                                            #AnumberCheck = [ANUMBER, True]
                                            key[len(key) - 1].append(name)
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                            key[len(key) - 1].append(SplitCommaSpace[0])
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                            key[len(key) - 1].append(SplitCommaSpace[1])
                                            key[len(key) - 1].append(ParticipantNames[l][1])
                                        else:
                                            #AnumberCheck = [ANUMBER, True]
                                            key[len(key) - 1].append(SplitCommaSpace[0])
                                            key[len(key) - 1].append(SplitCommaSpace[1])
                                    else:
                                        #AnumberCheck = [ANUMBER, True]
                                        key[len(key) - 1].append(name)
                                        key[len(key) - 1].append(ParticipantNames[l][m + 1])
                            if "or" in ParticipantNames[l][newNicknameColumn]:
                                SplitOr = ParticipantNames[l][newNicknameColumn].split('or')
                                for i in range(len(SplitOr)):
                                    SplitOr[i] = SplitOr[i].replace(" ", "")
                                for name in SplitOr:
                                    if " " in name:
                                        SplitOrSpace = name.split(" ")
                                        if SplitOrSpace[1] != ParticipantNames[l][1]:
                                            #AnumberCheck = [ANUMBER, True]
                                            key[len(key) - 1].append(name)
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                            key[len(key) - 1].append(SplitOrSpace[0])
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                            key[len(key) - 1].append(SplitOrSpace[1])
                                            key[len(key) - 1].append(ParticipantNames[l][1])
                                        else:
                                            #AnumberCheck = [ANUMBER, True]
                                            key[len(key) - 1].append(SplitOrSpace[0])
                                            key[len(key) - 1].append(SplitOrSpace[1])
                                    else:
                                        #AnumberCheck = [ANUMBER, True]
                                        key[len(key) - 1].append(name)
                                        key[len(key) - 1].append(ParticipantNames[l][1])
                            if "," not in ParticipantNames[l][newNicknameColumn] and "or" not in ParticipantNames[l][newNicknameColumn]:
                                #AnumberCheck = [ANUMBER, True]
                                ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].lower()
                                if ParticipantNames[l][newNicknameColumn] != 'none':
                                    if ParticipantNames[l][newNicknameColumn] != 'na':
                                        if ParticipantNames[l][newNicknameColumn] != 'nan':
                                            if ' ' not in ParticipantNames[l][newNicknameColumn]:
                                                ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].lower()
                                                key[len(key) - 1].insert(4, ParticipantNames[l][newNicknameColumn])
                                                key[len(key) - 1].insert(5, ParticipantName[1])
                                                key[len(key) - 1].insert(6, ParticipantName[0])
                                                key[len(key) - 1].insert(7, ParticipantName[1])
                                            if ' ' in ParticipantNames[l][newNicknameColumn]:
                                                SplitSpace = ParticipantNames[l][newNicknameColumn].split(' ')
                                                if SplitSpace[1] == ParticipantName[1]:
                                                    key[len(key) - 1].insert(4, SplitSpace[0])
                                                    key[len(key) - 1].insert(5, ParticipantName[1])
                                                else:
                                                    key[len(key) - 1].insert(4, SplitSpace[0])
                                                    key[len(key) - 1].insert(5, ParticipantName[1])
                                                    key[len(key) - 1].insert(6, SplitSpace[1])
                                                    key[len(key) - 1].insert(7, ParticipantName[1])

                    else:
                        if not AnumberCheck[1]:
                            AnumberCheck = [ANUMBER, True]
                            if not isinstance(ParticipantNames[l][newNicknameColumn], float):
                                if "," in ParticipantNames[l][newNicknameColumn]:
                                    location = int(registrarData(ANUMBER, key, ParticipantNames)) - 1
                                    SplitComma = ParticipantNames[l][newNicknameColumn].split(",")
                                    for i in range(len(SplitComma)):
                                        SplitComma[i] = SplitComma[i].replace(" ", "")
                                    ColumnLocationList = []
                                    for i in range(len(key[location])):
                                        if key[location][i] == "none":
                                            ColumnLocation = i
                                            ColumnLocationList.append(ColumnLocation)
                                    if ColumnLocationList:
                                        ActualColumnLocation = min(ColumnLocationList)
                                    if not ColumnLocationList:
                                        ActualColumnLocation = 2
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

                                if "or" in ParticipantNames[l][newNicknameColumn]:
                                    location = int(registrarData(ANUMBER, key, ParticipantNames)) - 1
                                    SplitOr = ParticipantNames[l][newNicknameColumn].split('or')
                                    for i in range(len(SplitOr)):
                                        SplitOr[i] = SplitOr[i].replace(" ", "")
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

                                if "," not in ParticipantNames[l][newNicknameColumn] and "or" not in ParticipantNames[l][
                                    newNicknameColumn]:
                                    location = int(registrarData(ANUMBER, key, ParticipantNames)) - 1
                                    ColumnLocationList = []
                                    for i in range(len(key[location])):
                                        if key[location][i] == "none":
                                            ColumnLocation = i
                                            ColumnLocationList.append(ColumnLocation)
                                        else:
                                            ActualColumnLocation = 4
                                    if ColumnLocationList != []:
                                        ActualColumnLocation = min(ColumnLocationList)
                                    if not isinstance(location, float):
                                        if ParticipantNames[l][newNicknameColumn] != 'none':
                                            if ' ' not in ParticipantNames[l][newNicknameColumn]:
                                                ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].lower()
                                                key[location].insert(ActualColumnLocation, ParticipantNames[l][newNicknameColumn])
                                                key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                                key[location].insert(ActualColumnLocation + 2, ParticipantName[0])
                                                key[location].insert(ActualColumnLocation + 3, ParticipantName[1])
                                            if ' ' in ParticipantNames[l][newNicknameColumn]:
                                                SplitSpace = ParticipantNames[l][newNicknameColumn].split(' ')
                                                if SplitSpace[1] == ParticipantName[1]:
                                                    key[location].insert(ActualColumnLocation, SplitSpace[0])
                                                    key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                                else:
                                                    key[location].insert(ActualColumnLocation, SplitSpace[0])
                                                    key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                                    key[location].insert(ActualColumnLocation + 2, SplitSpace[1])
                                                    key[location].insert(ActualColumnLocation + 3, ParticipantName[1])

    # -----------------------------------------------------------      ------------------------------------------------------
                else:
                    check = looper(ParticipantName, key)
                    if not check:
                        location = keyPosition(ParticipantName, key)
                        ColumnLocationList = []
                        for i in range(len(key[location])):
                            if key[location][i] == "none":
                                ColumnLocation = i
                                ColumnLocationList.append(ColumnLocation)
                        if ColumnLocationList != []:
                            ActualColumnLocation = min(ColumnLocationList)
                        else:
                            ActualColumnLocation = 4
                        key[location].insert(ActualColumnLocation, ParticipantName[0])
                        key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                    else:
                        if not isinstance(ParticipantNames[l][newNicknameColumn], float):
                            location = keyPosition(ParticipantName, key)
                            if "," in ParticipantNames[l][newNicknameColumn]:
                                SplitComma = ParticipantNames[l][newNicknameColumn].split(",")
                                for i in range(len(SplitComma)):
                                    SplitComma[i] = SplitComma[i].replace(" ", "")
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

                            if "or" in ParticipantNames[l][newNicknameColumn]:
                                SplitOr = ParticipantNames[l][newNicknameColumn].split('or')
                                for i in range(len(SplitOr)):
                                    SplitOr[i] = SplitOr[i].replace(" ", "")
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

                            if "," not in ParticipantNames[l][newNicknameColumn] and " " not in ParticipantNames[l][
                                newNicknameColumn]:
                                ColumnLocationList = []
                                for i in range(len(key[location])):
                                    if key[location][i] == "none":
                                        ColumnLocation = i
                                        ColumnLocationList.append(ColumnLocation)
                                    else:
                                        ActualColumnLocation = 4
                                if ColumnLocationList != []:
                                    ActualColumnLocation = min(ColumnLocationList)
                                if not isinstance(location, float):
                                    if ParticipantNames[l][newNicknameColumn] != 'none':
                                        if ' ' not in ParticipantNames[l][newNicknameColumn]:
                                            ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][
                                                newNicknameColumn].lower()
                                            key[location].insert(ActualColumnLocation,
                                                                 ParticipantNames[l][newNicknameColumn])
                                            key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                            key[location].insert(ActualColumnLocation + 2, ParticipantName[0])
                                            key[location].insert(ActualColumnLocation + 3, ParticipantName[1])
                                        if ' ' in ParticipantNames[l][newNicknameColumn]:
                                            SplitSpace = ParticipantNames[l][newNicknameColumn].split(' ')
                                            if SplitSpace[1] == ParticipantName[1]:
                                                key[location].insert(ActualColumnLocation, SplitSpace[0])
                                                key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                            else:
                                                key[location].insert(ActualColumnLocation, SplitSpace[0])
                                                key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                                key[location].insert(ActualColumnLocation + 2, SplitSpace[1])
                                                key[location].insert(ActualColumnLocation + 3, ParticipantName[1])

            else:
                SingleNameList.append(ParticipantName[0])

    LengthList = []
    for i in range(len(key)):
        LengthList.append(len(key[i]))
    MaxColumns = max(LengthList)
    for i in range(len(key)):
        if len(key[i]) < MaxColumns:
            for o in range(MaxColumns-len(key[i])):
                key[i].append("none")

    # Remove duplicates from the key if they have the same name
    key = removeDuplicatesFromKey(key)

    def alphaStrip(string):
        out = ""

        for i in range(len(string)):

            if string[i].isalpha():
                out = out + string[i]

        return out

    for i in range(len(key)):
        for j in range(len(key[i]) - 2):
            if isinstance(key[i][j+2], str):
                key[i][j+2] = alphaStrip(key[i][j+2])

    print('There are', len(key) - LengthofRegistry, "participant names (not in the registry) that have been added to the key.")
    print("The total size of the key after being initialized is", len(key))

    import csv

    mypath = 'output/Iteration' + str(testNumber) + '/'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    with open(mypath + 'KeyAfterParticipantNames' + str(testNumber) + '.csv', 'w', encoding='UTF8', newline='') as f:
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
                for m in range(0, len(key[l]) - 3, 2):
                    if isinstance(data[i][s+PeerColumnGroup1[0]], str) and isinstance(data[i][s+PeerColumnGroup1[0]+1], str):
                        if key[l][m + 2] and key[l][m + 3] != "none":
                            if data[i][s+PeerColumnGroup1[0]] == key[l][m + 2]:
                                if data[i][s+PeerColumnGroup1[0]+1] == key[l][m + 3]:
                                    resolvedcount += 1
                                    data[i][s + PeerColumnGroup1[0]] = key[l][1]
                                    data[i][s + PeerColumnGroup1[0] + 1] = key[l][1]
# =============================================================================
#                                     new = time.time()
#                                     timetoresolvesingle = new - start
#                                     print(timetoresolvesingle)
# =============================================================================
    if PeerColumnGroup2 != 0:
        print("hello")
        for i in range(RowStart, len(data)):  # loop through every row of the raw data
            for s in range(PeerColumnGroup2[1] - PeerColumnGroup2[0]):
                for l in range(len(key)):
                    for m in range(0, len(key[l]) - 3, 2):
                        if isinstance(data[i][s + PeerColumnGroup2[0]], str) and isinstance(
                                data[i][s + PeerColumnGroup2[0] + 1], str):
                            if key[l][m + 2] and key[l][m + 3] != "none":
                                if data[i][s + PeerColumnGroup2[0]] == key[l][m + 2]:
                                    if data[i][s + PeerColumnGroup2[0] + 1] == key[l][m + 3]:
                                        resolvedcount += 1
                                        data[i][s + PeerColumnGroup2[0]] = key[l][1]
                                        data[i][s + PeerColumnGroup2[0] + 1] = key[l][1]


        if PeerColumnGroup2 != 0:
            print("hello")
            for l in range(len(key)):
                for m in range(0, len(key[l]) - 3, 2):
                    for q in range(PeerColumnGroup2[1]-PeerColumnGroup2[0]):
                        if isinstance(data[i][q + PeerColumnGroup2[0]], str) and isinstance(data[i][q + PeerColumnGroup2[0] + 1], str):
                            if key[l][m + 2] and key[l][m + 3] != "none":
                                if data[i][q + PeerColumnGroup2[0]] == key[l][m + 2]:
                                    if data[i][q + PeerColumnGroup2[0] + 1] == key[l][m + 3]:
                                        resolvedcount += 1
                                        data[i][q + PeerColumnGroup1[0]] = key[l][1]
                                        data[i][q + PeerColumnGroup1[0] + 1] = key[l][1]
#  --------------------------- REPLACE PARTICIPANT'S SELF REPORTED NAMES --------------------------------------------  #

    for i in range(RowStart, len(data)):

        Location = concat_keyPosition(data[i][ParticipantColumn], key)
        data[i][ParticipantColumn] = Location

    print("The number of names resolved in the exact replacement stage is:", resolvedcount)
   # print("Participants who did not report their last name are:", ParticipantSelfReportedNames)

    ambiguouscount = 0

# MAYBE ADD SOMETHING HERE ABOUT N/A string values
    for i in range(RowStart, len(data)):
        for j in range(PeerColumnGroup1[0], PeerColumnGroup1[1] + 1):
            if isinstance(data[i][j], str):
                if data[i][j] != 'nan':
                    ambiguouscount += 1

    if PeerColumnGroup2 != 0:
        for i in range(RowStart, len(data)):
            for j in range(PeerColumnGroup2[0], PeerColumnGroup2[1] + 1):
                if isinstance(data[i][j], str):
                    if data[i][j] != 'nan':
                        ambiguouscount += 1

    #print("The number of remaining names (ambiguous) is:", (ambiguouscount/2))

    print("Number of 'High Confidence' Names are:", len(key))

    # write the data file to a .csv
    import csv

    mypath = 'output/Iteration' + str(testNumber) + '/'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    with open(mypath +'DataforComparison'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
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

    List1 = list(range(PeerColumnGroup1[0], PeerColumnGroup1[1], 2))
    if PeerColumnGroup2 != 0:
        List2 = list(range(PeerColumnGroup2[0], PeerColumnGroup2[1], 2))
        PeerList = List1 + List2
    else:
        PeerList = List1

    # read in the key file to a list
    import pandas as pd
    key = pd.read_csv(keyLocation, header=None)
    key.fillna('none', inplace=True)
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
        for columns in PeerList: # This is the number of columns of interaction data containing peer names divided by 2

            for i in range(len(key)):
                    # now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
                for j in range(0, len(key[i]) - 3, 2):

                    AmbiguousName = [data[o+RowStart][columns], data[o+RowStart][columns + 1]]

                    KeyName = [key[i][j+2], key[i][j+3]]

                    if isinstance(AmbiguousName[0], str) and isinstance(AmbiguousName[1], str):

                        if AmbiguousName[0].isalpha() and AmbiguousName[1].isalpha():
                            if AmbiguousName[0] != 'none':
                                if AmbiguousName[0] != 'na':

                                    ComparisonScoreFirstName = compare(KeyName[0], AmbiguousName[0])

                                    ComparisonScoreLastName = compare(KeyName[1], AmbiguousName[1])


                            if ComparisonScoreLastName[0] <= StringLastNameThresehold \
                                    and ComparisonScoreFirstName[0] <= StringFirstNameThresehold and \
                                    ComparisonScoreLastName[1] <= PhoneticLastNameThresehold and \
                                    ComparisonScoreFirstName[1] <= PhoneticFirstNameThresehold:

                                CompareList.append([KeyName[0], KeyName[1], AmbiguousName[0], AmbiguousName[1],
                                                    ComparisonScoreFirstName[0], ComparisonScoreLastName[1],
                                                    ComparisonScoreLastName[0], ComparisonScoreLastName[1]])

                            if ComparisonScoreLastName[0] <= ConsolidateStringLastNameThresehold \
                                    and ComparisonScoreFirstName[0] <= ConsolidateStringFirstNameThresehold and \
                                    ComparisonScoreLastName[1] <= ConsolidatePhoneticLastNameThresehold and \
                                    ComparisonScoreFirstName[1] <= ConsolidatePhoneticFirstNameThresehold:

                                data[o+RowStart][columns] = key[i][1]
                                data[o+RowStart][columns + 1] = key[i][1]

    # Put titles on the "CompareList" sheet
    CompareList.insert(0, ["Key First Name", "Key Last Name", "Ambiguous First Name",
                           "Ambiguous Last Name", "First Name: LD", "First Name: Metaphone",
                           "Last Name: LD", "Last Name: Metaphone"])

    #NumberOfHighConfidenceNames = len(key)

    #print("Number of High Confidence Names is as follows:", NumberOfHighConfidenceNames)

    # Length + 1 is what I need, HOWEVER, I need the index of the length
    # Start appending those values at that index.

    AmbiguousList = []
    m = 0
    for n in range(RowStart, len(data)):
        for columns in PeerList:
            Name = [data[n][columns], data[n][columns + 1]]
            c_one = str(Name[0]).isalpha()
            c_two = str(Name[1]).isalpha()

            #ambiguous = looper(data[n][columns], key)

            if isinstance(Name[0], str):
                if c_one and c_two:
                    AmbiguousNumber = len(key) + m
                    data[n][columns] = AmbiguousNumber
                    data[n][columns + 1] = AmbiguousNumber
                    AmbiguousList.append([Name, [AmbiguousNumber]])
                    m += 1

    print("The number of ambiguous names in the data are:", m)

    DIData = data
    EdgeList = []

    for i in range(RowStart, len(data)):
        for columns in PeerList:
            if data[i][ParticipantColumn] != "true":
               # print("yell")
               # if isinstance(data[n][columns], str):
                    # Might need to add the isalpha thing in here
                  #  print("ow")
                import math
                check = math.isnan(float(data[i][columns]))
                if not check:
                    EdgeList.append([data[i][ParticipantColumn], data[i][columns]])
    print(EdgeList)

    for i in range(len(EdgeList)):
        for j in range(len(EdgeList[i])):
            EdgeList[i][j] = int(EdgeList[i][j])

    AdjacencyMatrix = edgeToAdjacency(EdgeList)

    print(AdjacencyMatrix)

    # Write the "CompareList" to a csv file
    import csv
    mypath = 'output/Iteration'+str(testNumber)+'/'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    with open(mypath+'CompleteTrialIteration'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(CompareList)

    with open(mypath+'DeIdentifiedData'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(DIData)
    
    #spit these out so we can check to make sure deals work
    return [CompareList, DIData]

########################################### MAIN FUNCTION LOGIC ########################################################


# EVENTUALLY I NEED TO MAKE COPIES OF THE REAL DATA HERE
mypath = 'output/Iteration'+str(testNumber)+'/'
#check if the output files exist (due to the testNumber already being used) If so, delete prior to writing new files
if os.path.isdir(str('Key_Registry'+str(testNumber)+'.csv')):
    
    os.remove(str('Key_Registry'+str(testNumber)+'.csv'))
    os.remove(str('KeyAfterParticipantNames'+str(testNumber)+'.csv'))
    os.remove(str('DataforComparison'+str(testNumber)+'.csv'))
    os.remove(str('DeIdentifiedData'+str(testNumber)+'.csv'))
    
#rite the output files to the working directory of main()
key = addRegistryNames(registryLocation)

keyLocation = str(mypath+'Key_Registry'+str(testNumber)+'.csv')

#keyLocation ='/Users/adamweaver/Documents/GitHub/output/Iteration78/Key_Registry78.csv'

key = addParticipantsNames(keyLocation, dataFileLocation)

keyLocation = str(mypath+'KeyAfterParticipantNames'+str(testNumber)+'.csv')

data = replacingFunc(dataFileLocation, keyLocation)

dataFileLocation = str(mypath+'DataforComparison'+str(testNumber)+'.csv')

#keyLocation = '/Users/adamweaver/Documents/GitHub/KeyAfterParticipantNames43.csv'

#dataFileLocaiton = '/Users/adamweaver/Documents/GitHub/DataforComparison43.csv'

compareKeytoData(keyLocation, dataFileLocation)

# Check what the synthetic data looks like and if the ambiguous list is getting added correctly (not ever being false)
# THE AMBIGUOUS LIST NEEDS TO BE EVERY TWO!
# Why is it every two?
# Get replacing participant names to work

