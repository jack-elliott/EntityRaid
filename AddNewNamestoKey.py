def addNewNames(dataFileLocation, keyLocation, outputFileName):
    import pandas as pd

    data = pd.read_csv(dataFileLocation, header=None)
    data = data.values.tolist()

    # read in the key file to a list
    key = pd.read_csv(keyLocation, header=None)
    key = key.values.tolist()

    for i in range(len(data)):

        for p in range(10):
            data[i][25 + p] = str(data[i][25 + p]) + str(data[i][26 + p])
            del data[i][26 + p]

        # concatenate the names and then delate the column value of the last name for the second 10 responses
        for p in range(10):
            data[i][62 + p] = str(data[i][62 + p]) + str(data[i][63 + p])
            del data[i][63 + p]

        for p in range(5):
            data[i][120 + p] = str(data[i][120 + p]) + str(data[i][121 + p])

    for i in range(len(data)):  # loop through the whole list of data
        for j in range(len(data[0])):  # loop through each element per row
            if isinstance(data[i][j], str):  # check if each element is a string, if so convert to upper and remove whitespace
                data[i][j] = data[i][j].lower()
                data[i][j] = data[i][j].replace(" ", "")

    for i in range(len(data)):
        for j in range(len(data[0])):
            for l in range(len(key)):
                for m in range(len(key[l]) - 1):
                    if isinstance(data[i][j], str):
                        NewKey = []
                        for s in range(10):
                            if data[i][25 + s] != key[l][1]:
                                if data[i][j] != 'nannan':
                                    if data[i][j] != NewKey:
                                        NewKey.append(data[i][j])
                        for s in range(10):
                            if data[i][62 + s] != key[l][1]:
                                if data[i][j] != 'nannan':
                                    if data[i][j] != NewKey:
                                        NewKey.append(data[i][j])
                        for s in range(5):
                            if data[i][120 + s] != key[l][1]:
                                if data[i][j] != 'nannan':
                                    if data[i][j] != NewKey:
                                        NewKey.append(data[i][j])
                        print(NewKey)
    import csv
    with open('AddingNewNamesIteration12.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the .csv
        writer.writerows(NewKey)

        # spit these out so we can check to make sure deals work
    return (key, data)

# This should be the absolute path file location of the qualtrics data file
dataFileLocation = '/Users/adamweaver/Desktop/SNA/Primary Name Generator Survey_March 1, 2022_21.57.csv'

# This should be the file location on your computer of the key .csv
keyLocation = '/Users/adamweaver/Desktop/SNA/Key1.csv'

# Define the output name of interest
outputFileName = "BasicTest"

# this will just run the script
key, data = addNewNames(dataFileLocation, keyLocation, outputFileName)

# Ideas:
#   -I could append each instance on line 44 and append it to an empty list.
#    After this, I could count the strings in that list to see if it's really detecting every instance

#   -I tried both the len(m) and len(l), and they produced the same results
#    In these iterations, the third and forth columns in the key are marked as "nan"



# Comment the code more
# Create an artificial data set to work with
# Each part should have its own file
# fix outputFileName thingy

# STAGE 1 PART 1
# Just registry names
# *KEY IS BLANK
# Concatenate and space eliminate the data in the registry
# If two names match on the registry...DO NOT add to key
# Read in a registry, and any new values get added to the key (doesn't use matches)

# STAGE 1 PART 2
# Add any new of participants' own names (found in interaction data) to the key

# STAGE 1 PART 3
# In both cells, more than one character string

# Then, build main function

