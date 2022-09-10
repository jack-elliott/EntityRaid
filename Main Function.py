#============================================ DEFINE FUNCTIONS =======================================================

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

def addRegistryNames(keyLocation, registryLocation):

    # import respective libraries
    import pandas as pd

    # read in the key file to a list
    key = pd.read_csv(keyLocation, header=None)
    key = key.values.tolist()

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
                key.append([len(key) + 1, FinalRegistry[l][m], FinalRegistry[l][m + 1]])

    import csv
    with open('Key_Registry13.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(key)

    # spit the key out
    return key

def addParticipantsNames(keyLocation, dataFileLocation):
    # read in the key file to a list

    import pandas as pd
    key = pd.read_csv(keyLocation, header=None)
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

    for i in range(len(data) - 1):
        # In this case, the names are in the zero column. This will change depending on the survey data formatting.
        ParticipantNames.append([data[1 + i][0]])

    # Split the participant Names into First Name/Last Name components
    dfParticipantNames = pd.DataFrame(ParticipantNames)
    dfParticipantNames[[0, 1]] = dfParticipantNames[0].str.split(' ', expand=True)
    ParticipantNames = dfParticipantNames.values.tolist()



    # loop through each of the raw data rows
    for l in range(len(ParticipantNames)):

        # loop through each raw data column (set of names) corresponding to a given name not, first names are in cols 1,3,5,... last names col. 2,4,6,...
        for m in range(len(ParticipantNames[l]) - 1):

            # identify the name to be checked for in the key
            ParticipantName = [ParticipantNames[l][m], ParticipantNames[l][m + 1]]

            # now run the sub-routine to see if the name is in the key
            check = looper(ParticipantName, key)

            # If the name is not in the key, add the name to the key
            if check:
                key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])

    for i in range(len(key)):
        for j in range(len(key[i])):
            if len(key[i]) < len(max(key, key=len)):
                for o in range(len(max(key, key=len))-len(key[i])):
                    key[i].append("none")

    print('There are', len(ParticipantNames[0]), "participant names (not in the registry) that have been added to the key.")
    print("The total size of the key after being initialized is", len(key))

    import csv
    with open('KeyAfterParticipantNames13.csv', 'w', encoding='UTF8', newline='') as f:
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

    # Convert all of the data strings to just lowercase and remove all white space to make life easier
    for i in range(len(data)):  # loop through the whole list of data
        for j in range(len(data[0])):  # loop through each element per row
            if isinstance(data[i][j],
                          str):  # check if each element is a string, if so convert to upper and remove whitespace
                data[i][j] = data[i][j].lower()
                data[i][j] = data[i][j].replace(" ", "")

    # Now, make the key all lowercase so that matching will work in the following logic
    for a in range(len(key)):
        for b in range(len(key[0])):
            if isinstance(key[a][b], str):
                key[a][b] = key[a][b].lower()

    # Loop through the key and data and replace accordingly
    resolvedcount = 0
    for i in range(len(data)):
        for j in range(0, len(data[0]) - 1):
            for l in range(len(key)):
                for m in range(len(key[l]) - 2):
                    if data[i][j] == key[l][m + 1]:
                        if data[i][j+1] == key[l][m + 2]:
                            resolvedcount += 1
                            data[i][j] = key[l][0]
                            data[i][j+1] = key[l][0]
    print("The number of names resolved in the exact replacement stage is:", resolvedcount)

    ambiguouscount = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if isinstance(data[i][j], str):
                ambiguouscount += 1

    print("The number of remaining names (ambiguous) is:", (ambiguouscount/2) - resolvedcount)
    # write the data file to a .csv
    import csv
    with open('DataforComparison13.csv', 'w', encoding='UTF8', newline='') as f:
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
    with open('CompleteTrialIteration13.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(CompareList)

    # spit these out so we can check to make sure deals work
    return CompareList

########################################### MAIN FUNCTION LOGIC ########################################################



# This should be the absolute path file location of the qualtrics data file
dataFileLocation = '/Users/adamweaver/Desktop/SNA/SyntheticInteractionData.csv'

# This should be the file location on your computer of the key .csv
keyLocation = '/Users/adamweaver/Desktop/SNA/SyntheticKey(Fall2022).csv'

# This should be the absolute path file location of the registry data file
registryLocation = '/Users/adamweaver/Desktop/SNA/SyntheticRegistry.csv'

# EVENTUALLY I NEED TO MAKE COPIES OF THE REAL DATA HERE

key = addRegistryNames(keyLocation, registryLocation)

keyLocation = 'Key_Registry13.csv'

key = addParticipantsNames(keyLocation, dataFileLocation)

keyLocation = 'KeyAfterParticipantNames13.csv'

data = replacingFunc(dataFileLocation, keyLocation)

dataFileLocation = 'DataforComparison13.csv'

compareKeytoData(keyLocation, dataFileLocation)

# NEED TO ADD COUNTERS:
        # THIS INCLUDES:
                # HOW MANY GET ADDED/RESOLVED AT EACH STAGE
                # HOW MANY NAMES TO NUMBERS ARE LEFT AFTER REPLACEFUNC IS FINISHED

# NEED TO ADD USER INPUT:
         # THIS INCLUDES:
                # LOCATIONS FOR DATA FILE, REGISTRY, AND KEY
                # COLUMN NUMBERS


# ASSUMPTIONS:
        # REGISTRY IS FORMATTED WITH FIRST AND LAST NAME IN THE 0th COLUMN WITH A SPACE IN BETWEEEN THEM