# Looper function

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

# If we want to export the duplicate names, we have to do it here (duplicates list is cleared on Line 40)
# Remove any names that had duplicates using the duplicates list and the NewRegistry
    FinalRegistry = [x for x in NewRegistry if not x in Duplicates or Duplicates.remove(x)]

    for l in range(len(FinalRegistry)):
        for m in range(len(FinalRegistry[l]) - 1):

            # identify the name to be checked for in the key
            ParticipantName = [FinalRegistry[l][m], FinalRegistry[l][m + 1]]

            # now run the sub-routine to see if the name is in the key
            check = looper(ParticipantName, key)

            # If the name is not in the key, add the name to the key
            if check:
                key.append([len(key) + 1, FinalRegistry[l][m], FinalRegistry[l][m + 1]])
    print(key)

    import csv
    with open('AddingRegistryNamesFall2022Iteration2.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(key)

    # spit the key out
    return key

# File location on the computer of the key (has to be .csv format)
keyLocation = '/Users/adamweaver/Desktop/SNA/SyntheticKey.csv'

# This should be the absolute path file location of the registry data file
registryLocation = '/Users/adamweaver/Desktop/SNA/SyntheticRegistry.csv'

key = addRegistryNames(keyLocation, registryLocation)