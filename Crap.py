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
    print("Original length is", length)
    for l in range(len(key[:])):
        NewKey.append([key[l][1]])
        for m in range(len(key[l]) - 1):
            for a in range(len(registry)):
                for b in range(len(registry[0])):

                    NewName = '' + str(registry[a][0]) + ''
                    print("New Names are", NewName)

                    if NewName in key[l][1]:
                        continue
                    elif NewName == key[l][1]:
                        continue
                    else:
                        print("Registry is...", registry)
                        print("The registry value is...", NewName)
                        print("The key value is...", key[l][1])
                        print("First column of key is...", str(key[l][1]))
                        print(key)
                        if NewName not in NewNameList:
                                print("The length is,", len(NewNameList))
                                key.insert(m+2, [length-(LengthOfKey-3)-(len(NewNameList)), str(NewName)])
                                NewNameList.append(NewName)

    RevisedNewNameList = []
    for o in NewNameList:
        if o not in RevisedNewNameList:
            print("Is this working?")
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