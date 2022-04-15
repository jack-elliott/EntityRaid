def addRegistryNames(keyLocation, registryLocation):

    # import respective libraries
    import pandas as pd

    # read in the key file to a list
    key = pd.read_csv(keyLocation, header=None)
    key = key.values.tolist()

    # read the registry file to a list
    registry = pd.read_csv(registryLocation, header=None)
    registry = registry.values.tolist()

    # concatenate registry data, add a space between the first and last names, and pop it to a column
    for a in range(len(registry)):
        registry[a][0] = str(registry[a][0]) + ' ' + str(registry[a][1])
        registry[a].pop()

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

# Create a set out of the registry data
    RegistrySet = set()

# Fill the registry set with values from the FinalRegistry list created above
    for i in FinalRegistry:
        RegistrySet.update(i)

# Create a set out of the key
    KeySet = set()
    for j in key:
        KeySet.update(j)

# Find the values that need to be added to the key
    NewSet = RegistrySet - KeySet

# For each name in the new set, add it to the key, with the corresponding number
    for Name in NewSet:
        key.append([len(key)+1, Name])

# Convert the key into a Pandas DataFrame to make it easier to work with
    dfKey = pd.DataFrame(key)

# Split the 1 column of the key into two columns at the whitespace
    dfKey[[1, 2]] = dfKey[1].str.split(' ', expand=True)

# Covert the DataFrame back into a regular python 2d list
    key = dfKey.values.tolist()
    print(key)

# Import csv that will write the key to a spreadsheet
    import csv
    with open('AddingRegistryNamesfromInteractionDatatoKey69.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(key)

    # spit the key out
    return key

# File location on the computer of the key (has to be .csv format)
keyLocation = '/Users/adamweaver/Desktop/SNA/SyntheticKey.csv'

# This should be the absolute path file location of the registry data file
registryLocation = '/Users/adamweaver/Desktop/SNA/SyntheticRegistry.csv'

# Run the script
key = addRegistryNames(keyLocation, registryLocation)

# 4:47-