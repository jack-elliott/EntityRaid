# EntityRAID: Entity Resolution for Ambiguous Interaction Data
# EntityRAID is intended for large-data SNA

# INSTRUCTIONS AND IMPLICATIONS:

#    Key formatting and positioning should be exactly similar to ours
#    Interaction data can vary in positioning, but not in formatting
#    REGISTRY IS FORMATTED WITH FIRST AND LAST NAME IN THE 0th COLUMN WITH A SPACE IN BETWEEN THEM
#    ASSUMES THAT BOTH PEER COLUMN GROUPS ARE THE SAME SIZE

import os

# USER INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# This should be the absolute path file location of the qualtrics data file in .csv
# USE OUR EXAMPLES FOR A BETTER UNDERSTANDING OF THE CODE

######### ADAM LOCATION ######

dataFileLocation = 'INPUTDATAFILELOCATIONHERE.csv'

keyLocation = 'INPUTKEYFILELOCATIONHERE.csv'

registryLocation = 'INPUTREGISTRYLOCATIONHERE.csv'

# The following are input variables that tell the code how the data is organized. We left the values we used
# for our actual data for an example


ParticipantColumn = 21  # Which column the participants self-report their names
NicknameColumn = 25  # Which column the participants self-report their nicknames
ANumberColumn = 24  # Which column the participants report their school number (if applicable)
PeerColumnGroup1 = [26, 45]  # Which columns participants report their peer interactions
PeerColumnGroup2 = [87, 106]  # If there is a second group (add more), add these columns here. If not, report []
RowStart = 4  # After inspecting your data file csv, which row does the actual data start
RegistryRowStart = 2  # Similar to above, but for the registry (if applicable)


# PLEASE INPUT THE THRESHOLDS FOR REPORTING; CONSOLIDATION
# From our experience, the consolidation threshold produces closest to accurate results. Adjust the first set if
# you would like to see for yourself

StringLastNameThresehold = 2
StringFirstNameThresehold = 2
PhoneticLastNameThresehold = 1
PhoneticFirstNameThresehold = 1

ConsolidateStringLastNameThresehold = 2
ConsolidateStringFirstNameThresehold = 2
ConsolidatePhoneticLastNameThresehold = 1
ConsolidatePhoneticFirstNameThresehold = 1

testNumber = 184  # This number may help in data management, especially if you are editing this code


# END USER INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

newANumberColumn = 3
newParticipantNamesColumns = [0, 1]
import numpy as np

# BEGIN PRELIMINARY FUNCTIONS ------------------------------------------------------------------------------------------

def looper(ParticipantName, key):  # General looper
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


def alphaStrip(string):  # Remove alpha characters from a string
    out = ""

    for i in range(len(string)):

        if string[i].isalpha():
            out = out + string[i]

    return out


def ambiguouskeylooper(ParticipantName, AmbiguousKey):  # Loop through ambiguous key. Returns index if found

    for i in range(len(AmbiguousKey)):

        if ParticipantName[0] == AmbiguousKey[i][1]:

            if ParticipantName[1] == AmbiguousKey[i][2]:

                return AmbiguousKey[i][0]

    return 'butterfly'


def DuplicateKeyLooper(ParticipantName, DuplicateList):  # General looper for duplicate key

    for i in range(len(DuplicateList)):
        if ParticipantName[0] == DuplicateList[i][0]:
            if ParticipantName[1] == DuplicateList[i][1]:
                return 'Yes'
    return 'No'


def ambiguousKey(data, key):  # This function creates a full-name reference 'low-confidence' key

    LengthOfHighConfidenceKey = key[len(key) - 1][1]

    AmbiguousKey = []
    List1 = list(range(PeerColumnGroup1[0], PeerColumnGroup1[1], 2))
    if PeerColumnGroup2 != 0:
        List2 = list(range(PeerColumnGroup2[0], PeerColumnGroup2[1], 2))
        PeerList = List1 + List2
    else:
        PeerList = List1

    for i in range(RowStart, len(data)):
        for j in range(len(data[i])):
            if str(data[i][j]) == 'none':
                data[i][j] = 'nan'

    m = 1
    for i in range(RowStart, len(data)):
        for columns in PeerList:
            if str(data[i][columns]) != 'nan':
                if str(data[i][columns + 1]) != 'nan':
                    if str(data[i][columns]).isalpha():
                        if str(data[i][columns + 1]).isalpha():
                            Check = ambiguouskeylooper([data[i][columns], data[i][columns + 1]], AmbiguousKey)
                            if Check == 'butterfly':
                                ParticipantName = [data[i][columns], data[i][columns + 1]]
                                DuplicateCheck = DuplicateKeyLooper(ParticipantName, NewDuplicates)
                                DuplicateCounter = 0
                                if DuplicateCheck == 'No':
                                    AmbiguousKeyIndex = int(LengthOfHighConfidenceKey) + int(m)
                                    AmbiguousKey.append([AmbiguousKeyIndex, data[i][columns], data[i][columns+1]])
                                    m += 1
                                else:
                                    DuplicateCounter += 1

    return AmbiguousKey


def keyPosition(ParticipantName, key):  # This function finds the index of a reference, if found
    for i in range(len(key)):

        for j in range(len(key[i]) - 2):

            if ParticipantName[0] == key[i][j + 1]:

                if ParticipantName[1] == key[i][j + 2]:
                    # If the name is already in the key, return location
                    return i

    # if the name was not already in the key (made it here), return true
    return True


def keyPositionANUMBER(Anumber, key):  # This function returns the index if the school number is found in the key
    # now check each key row
    for i in range(len(key)):

        # Check the first name in the key
        if Anumber == key[i][0]:

            return float(key[i][1])

    # if the name was not already in the key (made it here), return true
    return True


def registrarData(ANumber, keyentry, ParticipantNameList):

    from Levenshtein import distance as lev
    for i in range(len(ParticipantNameList)):

        anumber = ParticipantNameList[i][newANumberColumn]
        if not isinstance(anumber, float):
            if anumber[0] == "a" and len(anumber) == 9:
                ParticipantNameList[i][newANumberColumn] = anumber[1] + anumber[2] + anumber[3] + anumber[4] + anumber[5] + anumber[6] + anumber[7] + anumber[8]

        LD = lev(str(anumber), str(ANumber))
        if LD < 1:
            KeyPosition = keyPositionANUMBER(anumber, keyentry)
            if isinstance(KeyPosition, float):
                return int(KeyPosition)

    return False


def edgeToAdjacency(edgeList, nodeCount="Auto"):  # Converts an edge list to an adjacency matrix

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


def concat_keyPosition(ParticipantName, key):  # This function is useful later on, after names have been concatenated
    # now check each key row
    for i in range(len(key)):

        # now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
        for j in range(len(key[i]) - 3):

            # Check the first name in the key
            concatenatedkeyname = str(key[i][j + 2]) + str(key[i][j + 3])

            if ParticipantName == concatenatedkeyname:

                CorrectIndex = int(key[i][1]) + int(1)

                return CorrectIndex

    # if the name was not already in the key (made it here), return true
    return 'NOPE'


def duplicates(key, ParticipantName):  # Finds duplicate rows in the key
    DuplicateRows = []
    for i in range(RowStart, len(key)):
        for j in range(len(key[0]) - 3):
            if key[i][j+2] == ParticipantName[0]:
                if key[i][j+3] == ParticipantName[1]:
                    DuplicateRows.append(i)

    return DuplicateRows

def removeDuplicatesFromKey(key):  # Removes duplicate rows from the key, consolidates nicknames if necessary
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
                            if key[newDuplicateCheck[i]][0] != ' undefined' or ParticipantNameRow[0] != 'undefined':
                                ANumberStringSim = lev(key[newDuplicateCheck[i]][0], ParticipantNameRow[0])
                            else:
                                ANumberStringSim = 0
                            if ANumberStringSim < 3:
                                DuplicateRows.append(key[newDuplicateCheck[i]])
                    newDuplicateCheck.insert(0, OriginalLocation)
                    DuplicateList.append(newDuplicateCheck)
    newList = []
    for a in range(len(DuplicateList)):
        if len(DuplicateList[a]) == 2:
            if DuplicateList[a][0] > DuplicateList[a][1]:
                newList.append(DuplicateList[a][0])
            else:
                newList.append(DuplicateList[a][1])
        if len(DuplicateList[a]) == 3:
            if DuplicateList[a][0] > DuplicateList[a][1] and DuplicateList[a][0] > DuplicateList[a][2]:
                newList.append(DuplicateList[a][0])
            if DuplicateList[a][1] > DuplicateList[a][0] and DuplicateList[a][1] > DuplicateList[a][2]:
                newList.append(DuplicateList[a][1])
            if DuplicateList[a][2] > DuplicateList[a][0] and DuplicateList[a][2] > DuplicateList[a][1]:
                newList.append(DuplicateList[a][2])

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

    print("There were", len(Remove), "rows removed from the key")
    return key


# END PRELIMINARY FUNCTIONS --------------------------------------------------------------------------------------------
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
        if not isinstance(anumber, float):
            if anumber[1] == "A" and len(anumber) == 10:
                firstcolumnsplit[i][0] = anumber[2] + anumber[3] + anumber[4] + anumber[5] + anumber[6] + \
                                                        anumber[7] + anumber[8] + anumber[9]

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

    global NewDuplicates
    NewDuplicates = []

    for names in Duplicates:
        newcolumns = names.split(' ', 1)
        NewDuplicates.append(newcolumns)

    NewDuplicates.append(['Matt', 'Jensen'])
    NewDuplicates.append(['Matthew', 'Jensen'])

    for i in range(len(NewDuplicates)):
        CombinedName = NewDuplicates[i][0] + NewDuplicates[i][1]
        NewDuplicates.append([CombinedName, ''])

    for rows in NewDuplicates:
        if rows in registry:
            registry.remove(rows)


    FinalRegistry = registry

    for i in range(len(NewDuplicates)):  # loop through the whole list of data
        for j in range(len(NewDuplicates[0])):  # loop through each element per row
            if isinstance(NewDuplicates[i][j], str):
                NewDuplicates[i][j] = NewDuplicates[i][j].lower()


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

    FinalRegistry.pop(RegistryRowStart - 2)


    global LengthofRegistry
    LengthofRegistry = len(FinalRegistry)


    for l in range(len(FinalRegistry)):
        for m in range(len(FinalRegistry[l]) - 1):

            FinalRegistry[l][2] = alphaStrip(FinalRegistry[l][2])

            Anumber = FinalRegistry[l][0]
            # identify the name to be checked for in the key
            ParticipantName = [FinalRegistry[l][1], FinalRegistry[l][2]]

            # now run the sub-routine to see if the name is in the key
            check = looper(ParticipantName, key)

            # If the name is not in the key, add the name to the key
            if check:
                key.append([Anumber, len(key), FinalRegistry[l][1], FinalRegistry[l][2]])

    key.pop(0)
    print("There are", key[len(key) - 1][1], "names in the registry that have been added to the key.")
    print("The length of the key after registry initialization is:", len(key))

    for i in range(len(key)):
        if isinstance(key[i][0], float):
            key[i][0] = ' undefined'

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
                for q in range(StrLen - 1):
                    NameList.append(Name[q + 1])
                stringreconstructed = ''.join(NameList)
                data[RowStart + i][ParticipantColumn] = stringreconstructed
            for p in range(len(data[RowStart + i][ParticipantColumn]) - 2):
                if data[RowStart + i][ParticipantColumn][p] == ' ':
                    if data[RowStart + i][ParticipantColumn][p + 1] == ' ':
                        newentry = data[RowStart + i][ParticipantColumn].replace(' ', '', 1)
                        data[RowStart + i][ParticipantColumn] = newentry
            if '(' not in data[RowStart + i][ParticipantColumn]:
            # In this case, the names are in the zero column. This will change depending on the survey data formatting.
                ParticipantNames.append([data[RowStart + i][ParticipantColumn], data[RowStart + i][NicknameColumn], data[RowStart + i][ANumberColumn]])
    # Split the participant Names into First Name/Last Name components

    dfParticipantNames = pd.DataFrame(ParticipantNames)
    dfParticipantNames[3] = dfParticipantNames[2]
    dfParticipantNames[2] = dfParticipantNames[1]
    dfSplit = dfParticipantNames[0].str.split(' ', n=1, expand=True)
    dfParticipantNames[0] = dfSplit[0]
    dfParticipantNames[1] = dfSplit[1]
    ParticipantNames = dfParticipantNames.values.tolist()

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
                if ParticipantNames[i][newNicknameColumn][1] == "o":
                    if ParticipantNames[i][newNicknameColumn][2] == "n":
                        if ParticipantNames[i][newNicknameColumn][3] == "e":
                            ParticipantNames[i][newNicknameColumn] = 'none'

    SingleNameList = []
    AnumberCheck = ['filler', False]
    for l in range(len(ParticipantNames)):
        AnumberCheck = [ParticipantNames[l][newANumberColumn], False]
        for m in range(len(ParticipantNames[0]) - 1):
            ParticipantName = [ParticipantNames[l][0], ParticipantNames[l][1]]
            ANUMBER = ParticipantNames[l][newANumberColumn]
            nickname = ParticipantNames[l][newNicknameColumn]
            if ParticipantName[0] != '' and ParticipantName[1] != None and ParticipantName[1] != '':
                DuplicateCheck = DuplicateKeyLooper(ParticipantName, NewDuplicates)
                adam = 0
                if DuplicateCheck == 'No':
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

                                                key[len(key) - 1].append(ParticipantName[0])
                                                key[len(key) - 1].append(ParticipantNames[l][1])
                                            else:
                                                #AnumberCheck = [ANUMBER, True]
                                                key[len(key) - 1].append(SplitCommaSpace[0])
                                                key[len(key) - 1].append(SplitCommaSpace[1])

                                                key[len(key) - 1].append(ParticipantName[0])
                                                key[len(key) - 1].append(ParticipantNames[l][1])
                                        else:
                                            #AnumberCheck = [ANUMBER, True]
                                            key[len(key) - 1].append(name)
                                            key[len(key) - 1].append(ParticipantNames[l][m + 1])

                                            key[len(key) - 1].append(ParticipantName[0])
                                            key[len(key) - 1].append(ParticipantNames[l][1])
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

                                                key[len(key) - 1].append(ParticipantName[0])
                                                key[len(key) - 1].append(ParticipantNames[l][1])
                                            else:
                                                #AnumberCheck = [ANUMBER, True]
                                                key[len(key) - 1].append(SplitOrSpace[0])
                                                key[len(key) - 1].append(SplitOrSpace[1])

                                                key[len(key) - 1].append(ParticipantName[0])
                                                key[len(key) - 1].append(ParticipantNames[l][1])
                                        else:
                                            #AnumberCheck = [ANUMBER, True]
                                            key[len(key) - 1].append(name)
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                            key[len(key) - 1].append(ParticipantName[0])
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

                                                        key[len(key) - 1].insert(6, ParticipantName[0])
                                                        key[len(key) - 1].insert(7, ParticipantName[1])

                                                    else:
                                                        key[len(key) - 1].insert(4, SplitSpace[0])
                                                        key[len(key) - 1].insert(5, ParticipantName[1])
                                                        key[len(key) - 1].insert(6, SplitSpace[1])
                                                        key[len(key) - 1].insert(7, ParticipantName[1])
                                                        key[len(key) - 1].insert(8, ParticipantName[0])
                                                        key[len(key) - 1].insert(9, ParticipantName[1])
                        else:
                            if not AnumberCheck[1]:
                                AnumberCheck = [ANUMBER, True]
                                location = int(registrarData(ANUMBER, key, ParticipantNames)) - 1
                                ColumnLocationList = []
                                for i in range(len(key[location])):
                                    if key[location][i] == "none":
                                        ColumnLocation = i
                                        ColumnLocationList.append(ColumnLocation)
                                if ColumnLocationList:
                                    ActualColumnLocation = min(ColumnLocationList)
                                if not ColumnLocationList:
                                    ActualColumnLocation = 2
                                if not isinstance(ParticipantNames[l][newNicknameColumn], float):
                                    if "," in ParticipantNames[l][newNicknameColumn]:
                                        SplitComma = ParticipantNames[l][newNicknameColumn].split(",")
                                        for i in range(len(SplitComma)):
                                            SplitComma[i] = SplitComma[i].replace(" ", "")
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

                                                        key[location].insert(ActualColumnLocation + 6, ParticipantName[0])
                                                        key[location].insert(ActualColumnLocation + 7,
                                                                             ParticipantNames[l][1])

                                                    else:
                                                        key[location].insert(ActualColumnLocation, SplitCommaSpace[0])
                                                        key[location].insert(ActualColumnLocation + 1, SplitCommaSpace[1])

                                                        key[location].insert(ActualColumnLocation + 2, ParticipantName[0])
                                                        key[location].insert(ActualColumnLocation + 3,
                                                                             ParticipantNames[l][1])
                                                else:
                                                    key[location].insert(ActualColumnLocation, name)
                                                    key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                                                    key[location].insert(ActualColumnLocation + 2, ParticipantName[0])
                                                    key[location].insert(ActualColumnLocation + 3,
                                                                         ParticipantNames[l][1])

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

                                                        key[location].insert(ActualColumnLocation + 6, ParticipantName[0])
                                                        key[location].insert(ActualColumnLocation + 7,
                                                                             ParticipantNames[l][1])
                                                    else:
                                                        key[location].insert(ActualColumnLocation, SplitOrSpace[0])
                                                        key[location].insert(ActualColumnLocation + 1, SplitOrSpace[1])

                                                        key[location].insert(ActualColumnLocation + 2, ParticipantName[0])
                                                        key[location].insert(ActualColumnLocation + 3,
                                                                             ParticipantNames[l][1])
                                                else:
                                                    key[location].insert(ActualColumnLocation, name)
                                                    key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                                                    key[location].insert(ActualColumnLocation + 2, ParticipantName[0])
                                                    key[location].insert(ActualColumnLocation + 3,
                                                                         ParticipantNames[l][1])

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
                                                    key[location].insert(ActualColumnLocation + 4, ParticipantName[0])
                                                    key[location].insert(ActualColumnLocation + 5,
                                                                         ParticipantNames[l][1])
                                                if ' ' in ParticipantNames[l][newNicknameColumn]:
                                                    SplitSpace = ParticipantNames[l][newNicknameColumn].split(' ')
                                                    if SplitSpace[1] == ParticipantName[1]:
                                                        key[location].insert(ActualColumnLocation, SplitSpace[0])
                                                        key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                                        key[location].insert(ActualColumnLocation + 2, ParticipantName[0])
                                                        key[location].insert(ActualColumnLocation + 3,
                                                                             ParticipantNames[l][1])
                                                    else:
                                                        key[location].insert(ActualColumnLocation, SplitSpace[0])
                                                        key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                                        key[location].insert(ActualColumnLocation + 2, SplitSpace[1])
                                                        key[location].insert(ActualColumnLocation + 3, ParticipantName[1])
                                                        key[location].insert(ActualColumnLocation + 4, ParticipantName[0])
                                                        key[location].insert(ActualColumnLocation + 5,
                                                                             ParticipantNames[l][1])
                                    else:
                                        key[location].insert(ActualColumnLocation, ParticipantName[0])
                                        key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                                else:
                                    key[location].insert(ActualColumnLocation, ParticipantName[0])
                                    key[location].insert(ActualColumnLocation + 1, ParticipantName[1])

        # --------------------------------------------------------------------------------------------------------------
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
                            location = keyPosition(ParticipantName, key)
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

                                                key[len(key) - 1].append(ParticipantName[0])
                                                key[len(key) - 1].append(ParticipantNames[l][1])
                                            else:
                                                #AnumberCheck = [ANUMBER, True]
                                                key[len(key) - 1].append(SplitCommaSpace[0])
                                                key[len(key) - 1].append(SplitCommaSpace[1])

                                                key[len(key) - 1].append(ParticipantName[0])
                                                key[len(key) - 1].append(ParticipantNames[l][1])
                                        else:
                                            #AnumberCheck = [ANUMBER, True]
                                            key[len(key) - 1].append(name)
                                            key[len(key) - 1].append(ParticipantNames[l][m + 1])

                                            key[len(key) - 1].append(ParticipantName[0])
                                            key[len(key) - 1].append(ParticipantNames[l][1])
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

                                                key[len(key) - 1].append(ParticipantName[0])
                                                key[len(key) - 1].append(ParticipantNames[l][1])
                                            else:
                                                #AnumberCheck = [ANUMBER, True]
                                                key[len(key) - 1].append(SplitOrSpace[0])
                                                key[len(key) - 1].append(SplitOrSpace[1])

                                                key[len(key) - 1].append(ParticipantName[0])
                                                key[len(key) - 1].append(ParticipantNames[l][1])
                                        else:
                                            #AnumberCheck = [ANUMBER, True]
                                            key[len(key) - 1].append(name)
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                            key[len(key) - 1].append(ParticipantName[0])
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
                                                        key[len(key) - 1].insert(6, ParticipantName[0])
                                                        key[len(key) - 1].insert(7, ParticipantName[1])
                                                    else:
                                                        key[len(key) - 1].insert(4, SplitSpace[0])
                                                        key[len(key) - 1].insert(5, ParticipantName[1])
                                                        key[len(key) - 1].insert(6, SplitSpace[1])
                                                        key[len(key) - 1].insert(7, ParticipantName[1])
                                                        key[len(key) - 1].insert(8, ParticipantName[0])
                                                        key[len(key) - 1].insert(9, ParticipantName[1])
                            else:
                                key.append([' undefined', len(key) + 1, ParticipantName[0], ParticipantName[1]])
                else:
                    adam += 1
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

    keybeforeduplicates = key
    # Remove duplicates from the key if they have the same name
    key = removeDuplicatesFromKey(key)

    for i in range(len(NewDuplicates)):
        DuplicateName = [NewDuplicates[i][0], NewDuplicates[i][1]]
        DuplicateCheck = looper(DuplicateName, key)
        if not DuplicateCheck:
            Position = keyPosition(DuplicateName, key)
            key.remove(key[Position])

    for i in range(len(key)):
        for j in range(len(key[i]) - 2):
            if isinstance(key[i][j+2], str):
                key[i][j+2] = alphaStrip(key[i][j+2])

    print("The total size index of the key after being initialized is:", key[len(key) - 1][1])
    print("However, the total length of the high-confidence key is:", len(key))

    import csv

    mypath = 'output/Iteration' + str(testNumber) + '/'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    with open(mypath + 'KeyAfterParticipantNames' + str(testNumber) + '.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(key)

    with open(mypath + 'KeyBeforeDuplicateRemoval' + str(testNumber) + '.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(keybeforeduplicates)

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
                if j != ANumberColumn:
                    data[i][j] = alphaStrip(data[i][j])

    # Now, make the key all lowercase so that matching will work in the following logic
    for a in range(len(key)):
        for b in range(len(key[0])):
            if isinstance(key[a][b], str):
                key[a][b] = key[a][b].lower()

    # Loop through the key and data and replace accordingly
    resolvedcount = 0

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

    if PeerColumnGroup2 != 0:
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
    b = 0
    for i in range(RowStart, len(data)):

        Location = concat_keyPosition(data[i][ParticipantColumn], key)

        if str(Location).isnumeric():
            data[i][ParticipantColumn] = int(Location) - int(1)
        else:
            ANumber = data[i][ANumberColumn]
            if not isinstance(ANumber, float):
                if len(ANumber) == 9:
                    data[i][ANumberColumn] = ANumber[1] + ANumber[2] + ANumber[3] + ANumber[4] + ANumber[
                        5] + ANumber[6] + ANumber[7] + ANumber[8]
                if len(ANumber) == 8:
                    data[i][ANumberColumn] = ANumber[1] + ANumber[2] + ANumber[3] + ANumber[4] + ANumber[
                        5] + ANumber[6] + ANumber[7]
            ANumber = data[i][ANumberColumn]
            NumberCheck = keyPositionANUMBER(str(ANumber), key)
            if isinstance(NumberCheck, float):
                data[i][ParticipantColumn] = int(NumberCheck)
                b += 1

    print("The number of first-name references resolved via school-number consolidation is:", b)
    print("The number of references in the data resolved in the exact replacement stage is (without length of key):", resolvedcount)

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
    f = 0

    for o in range(len(data) - RowStart):
        for columns in PeerList:  # This is the number of columns of interaction data containing peer names divided by 2

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

                                f += 1
                                data[o+RowStart][columns] = key[i][1]
                                data[o+RowStart][columns + 1] = key[i][1]


    print("There were", f, "name variants consolidated")

    # Put titles on the "CompareList" sheet
    CompareList.insert(0, ["Key First Name", "Key Last Name", "Ambiguous First Name",
                           "Ambiguous Last Name", "First Name: LD", "First Name: Metaphone",
                           "Last Name: LD", "Last Name: Metaphone"])

    # Write the "CompareList" to a csv file
    import csv
    mypath = 'output/Iteration'+str(testNumber)+'/'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)

    with open(mypath+'CompleteTrialIteration'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(CompareList)

    with open(mypath+'FullyResolvedParticipantKey'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    return [CompareList, data]


def remainingAmbiguousNames(keyLocation, dataFileLocation):

    import pandas as pd

    key = pd.read_csv(keyLocation, header=None)
    key.fillna('none', inplace=True)
    key = key.values.tolist()

    # read in the data file of interest to a list
    data = pd.read_csv(dataFileLocation, header=None)
    data = data.values.tolist()

    List1 = list(range(PeerColumnGroup1[0], PeerColumnGroup1[1], 2))
    if PeerColumnGroup2 != 0:
        List2 = list(range(PeerColumnGroup2[0], PeerColumnGroup2[1], 2))
        PeerList = List1 + List2
    else:
        PeerList = List1
    FullNameAmbiguousKey = ambiguousKey(data, key)

    print("There are", len(FullNameAmbiguousKey), "full-name non-participant references in the key")

    v = 0
    for i in range(RowStart, len(data)):
        for columns in PeerList:
            FullNameCheck = ambiguouskeylooper([data[i][columns], data[i][columns + 1]], FullNameAmbiguousKey)
            if isinstance(FullNameCheck, int):
                data[i][columns] = FullNameCheck
                data[i][columns + 1] = FullNameCheck
                v += 1

    print("There were", v, "full-name references resolved with the low-confidence key")

    FirstNameList = []
    ParticipantFirstNameList = [['placeholder', 999999]]
    import numpy as np
    m = 1

    # PLEASE NOTE:

    # The following code is rendered obsolete due to the checks we enforced on it. In previous iterations, we used
    # this code to filter names. However, we decided that names that leaked through the code (0.2% of references)
    # were better left to manual disambiguation for best results.


    RemainingParticipantNameList = []
    for n in range(RowStart, len(data)):
        AmbiguousNumber = FullNameAmbiguousKey[len(FullNameAmbiguousKey) - 1][0] + m
        if isinstance(data[n][ParticipantColumn], str):
            RemainingParticipantNameList.append(data[n][ParticipantColumn])
            if not data[n][ParticipantColumn].isnumeric():
                Check = np.where(np.array(ParticipantFirstNameList) == str(data[n][ParticipantColumn]))
                if Check[0].size == 0:
                    NamesSplit = []
                    NewList = []
                    for names in RemainingParticipantNameList:
                        if ' ' in names:
                            newcolumns = names.split(' ', 1)
                            NewList.append(newcolumns)
                        else:
                            NewList.append([names, ''])
                        NamesSplit = NewList
                    for i in range(len(NamesSplit)):
                        ParticipantName = NamesSplit[i]
                        DuplicateCheck = DuplicateKeyLooper(ParticipantName, NewDuplicates)
                        DuplicateCounter = 0
                        if DuplicateCheck == 'No':
                            Check1 = np.where(np.array(ParticipantFirstNameList) == str(AmbiguousNumber))
                            if Check1[0] != []:
                                ParticipantFirstNameList.append([data[n][ParticipantColumn], AmbiguousNumber])
                                data[n][ParticipantColumn] = AmbiguousNumber
                                m += 1
                        else:
                            DuplicateCounter += 1
                else:
                    data[n][ParticipantColumn] = int(ParticipantFirstNameList[Check[0][0]][1])

    h = 0
    for o in range(RowStart, len(data)):
        if str(data[o][ParticipantColumn]) != 'nan':
            h += 1

    o = 0
    for k in range(RowStart, len(data)):
        for columns in PeerList:
            NewAmbiguousNumber = AmbiguousNumber + o
            Name = [data[k][columns], data[k][columns + 1]]
            c_one = str(Name[0]).isalpha()
            if isinstance(Name[0], str):
                if c_one:
                    if str(Name[1]) == 'nan':
                        FirstNameList.append([Name[0], NewAmbiguousNumber])
                        data[k][columns] = NewAmbiguousNumber
                        data[k][columns + 1] = NewAmbiguousNumber
                        o += 1

    print("There are:", h, "valid participant responses in the data")
    print("There are:", len(FirstNameList), "first-name only ambiguous references in the data")
    print("There are:", len(ParticipantFirstNameList), "first-name only ambiguous references in the data")

    EdgeList = []

    for i in range(RowStart, len(data)):
        for columns in PeerList:
            if str(data[i][columns]) != 'nan':
                EdgeList.append([data[i][ParticipantColumn], data[i][columns]])

    print("The total number of ambiguous references are:", len(EdgeList))
    import os
    import csv
    mypath = 'output/Iteration' + str(testNumber) + '/'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)

    with open(mypath+'DeIdentifiedData'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    with open(mypath+'FullNameAmbiguousKey'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(FullNameAmbiguousKey)

    with open(mypath+'FirstNameOnlyAmbiguousKey'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(FirstNameList)

    with open(mypath+'ParticipantsOwnAmbiguous'+str(testNumber)+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(ParticipantFirstNameList)

    return [data]  # AdjacencyMatrix]


########################################### MAIN FUNCTION LOGIC ########################################################

mypath = 'output/Iteration'+str(testNumber)+'/'

# Check if the output files exist (due to the testNumber already being used) If so, delete prior to writing new files
if os.path.isdir(str('Key_Registry'+str(testNumber)+'.csv')):
    
    os.remove(str('Key_Registry'+str(testNumber)+'.csv'))
    os.remove(str('KeyAfterParticipantNames'+str(testNumber)+'.csv'))
    os.remove(str('DataforComparison'+str(testNumber)+'.csv'))
    os.remove(str('DeIdentifiedData'+str(testNumber)+'.csv'))
    
#rite the output files to the working directory of main()
key = addRegistryNames(registryLocation)

keyLocation = str(mypath+'Key_Registry'+str(testNumber)+'.csv')

key = addParticipantsNames(keyLocation, dataFileLocation)

keyLocation = str(mypath+'KeyAfterParticipantNames'+str(testNumber)+'.csv')

data = replacingFunc(dataFileLocation, keyLocation)

dataFileLocation = str(mypath+'DataforComparison'+str(testNumber)+'.csv')

output = compareKeytoData(keyLocation, dataFileLocation)

dataFileLocation = str(mypath+'FullyResolvedParticipantKey'+str(testNumber)+'.csv')

FinalOutput = remainingAmbiguousNames(keyLocation, dataFileLocation)
