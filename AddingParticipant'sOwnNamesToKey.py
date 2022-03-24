def addParticipantsNames(keyLocation, dataFileLocation):
    # import respective libraries
    import pandas as pd

    # read in the key file to a list
    key = pd.read_csv(keyLocation, header=None)
    key = key.values.tolist()

    # read in the data file of interest to a list
    data = pd.read_csv(dataFileLocation, header=None)
    data = data.values.tolist()

    # Concatenate the first and last names
    for i in range(len(data)):
        for p in range(6):
            data[i][1 + p] = str(data[i][1 + p]) + str(data[i][2 + p])
            del data[i][2 + p]

    # Convert all of the data strings to just lowercase and remove all white space to make life easier
    for i in range(len(data)):  # loop through the whole list of data
        for j in range(len(data[0])):  # loop through each element per row
            if isinstance(data[i][j],
                          str):  # check if each element is a string, if so convert to upper and remove whitespace
                data[i][j] = data[i][j].lower()
                data[i][j] = data[i][j].replace(" ", "")

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
        key.append([len(key) + 1, Name])

    # Import csv that will write the key to a spreadsheet
    import csv
    with open('AddingRegistryNamesfromInteractionDatatoKey59.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(key)

    # spit the key out
    return key


# This should be the file location on your computer of the key .csv
keyLocation = '/Users/adamweaver/Desktop/SNA/SyntheticKey.csv'

# This should be the absolute path file location of the qualtrics data file
dataFileLocation = '/Users/adamweaver/Desktop/SNA/SyntheticInteractionData.csv'

# Run the script
key = addParticipantsNames(keyLocation, dataFileLocation)