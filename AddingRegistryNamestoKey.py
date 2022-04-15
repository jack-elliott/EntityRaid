def addRegistryNames(dataFileLocation, keyLocation, registryLocation):
    import pandas as pd
    from collections import Counter

    data = pd.read_csv(dataFileLocation, header=None)
    data = data.values.tolist()

    # read in the key file to a list
    key = pd.read_csv(keyLocation, header=None)
    key = key.values.tolist()

    registry = pd.read_csv(registryLocation, header=None)
    registry = registry.values.tolist()

    for i in range(len(data)):
        for j in range(6):
            data[i][1 + j] = str(data[i][1 + j]) + str(data[i][2 + j])
            del data[i][2 + j]

    for i in range(len(data)):  # loop through the whole list of data
        for j in range(len(data[0])):  # loop through each element per row
            if isinstance(data[i][j], str):  # check if each element is a string, if so convert to upper and remove whitespace
                data[i][j] = data[i][j].lower()
                data[i][j] = data[i][j].replace(" ", "")

    for a in range(len(registry)):
        registry[a][0] = str(registry[a][0]) + str(registry[a][1])
        registry[a].pop()

    for a in range(len(registry)):
        for b in range(len(registry[0])):
            if isinstance(registry[a][b], str):
                registry[a][b] = registry[a][b].lower()
                registry[a][b] = registry[a][b].replace(" ", "")
    print(len(registry))
    LengthOfKey = len(key[:])
    print(LengthOfKey)

    NewKey = []
    NewNameList = []
    length = len(registry)
    print("originial length is", length)
    for l in range(len(key[:])):
        NewKey.append([key[l][1]])
        # now in each row, check each column in the key, starting after the numeric value
        for m in range(len(key[l]) - 1):
            for a in range(len(registry)):
        # len(Registry[0]) shows how many columns there are (in this case...it's 1)
                for b in range(len(registry[0])):
            # now that we are at each data list element, check the key value rows
                    mCheck = m + 1  # make sure to skip the first value
                    # Check if the key value matches the data value, if so reassign, if not continue
                    if registry[a][0] != key[l][1]:
                        NewName = str(registry[a][0])
                        print("Registry is...", registry)
                        print("First column of key is...", key[l][1])
                        if NewName not in NewNameList:
                                print("The length is,", len(NewNameList))
                                key.insert(m+2, [length-(LengthOfKey-3)-(len(NewNameList)), str(NewName)])
                                NewNameList.append(NewName)


    RevisedNewNameList = []
    #Split the revised new name list into multiple rows
    #Append to the key in column number 1 (see above to see how to do that)
    # or, add each individual name to key instead of creating a new list?
    for o in NewNameList:
        if o not in RevisedNewNameList:
            print("I hate my life")
    print("Revised New Name List is, ", RevisedNewNameList)
    print("Key is", key)

    #key.append(RevisedNewNameList)
    #I'm going to need some break statments here!
    import csv
    with open('AddingRegistryNamesfromInteractionDatatoKey53.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(key)

        # spit these out so we can check to make sure deals work
    return key, data


# This should be the absolute path file location of the qualtrics data file
dataFileLocation = '/Users/adamweaver/Desktop/SNA/SyntheticInteractionData.csv'

# This should be the file location on your computer of the key .csv
keyLocation = '/Users/adamweaver/Desktop/SNA/SyntheticKey.csv'

# This should be the absolute path file location of the registry data file
registryLocation = '/Users/adamweaver/Desktop/SNA/SyntheticRegistry.csv'

# this will just run the script
key, data = addRegistryNames(dataFileLocation, keyLocation, registryLocation)

# 7:55-