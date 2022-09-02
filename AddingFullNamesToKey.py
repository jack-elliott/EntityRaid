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

def addFullNames(keyLocation, dataFileLocation):
    # import respective libraries
    import pandas as pd

    # read in the key file to a list
    key = pd.read_csv(keyLocation, header=None)
    key = key.values.tolist()

    # read in the data file of interest to a list
    data = pd.read_csv(dataFileLocation, header=None)
    data = data.values.tolist()

    # Convert all of the data strings to just lowercase and remove all white space to make life easier
    for i in range(len(data)):  # loop through the whole list of data
        for j in range(len(data[0])):  # loop through each element per row
            if isinstance(data[i][j], str):
                data[i][j] = data[i][j].lower()




    #for i in range(len(data)):
     #   for p in range(6):
      #      data[i][1 + p] = str(data[i][1 + p]) + ' ' + str(data[i][2 + p])
       #     del data[i][2 + p]

  #  FullNames = []
  #  for i in range(len(data)-1):
   #     for j in range(len(data)-1):
        # In this case, the names are in the zero column. This will change depending on the survey data formatting.
   #         FullNames.append([data[1+i][1+j]])
  #  print(FullNames)

    # Create a set out of the registry data
   # FullNamesSet = set()

    # Fill the registry set with values from the Full Names list created above
   # for Names in FullNames:
   #     FullNamesSet.update(Names)

    # Create a set out of the key
   # KeySet = set()
   # for j in key:
   #     KeySet.update(j)

    # Find the values that need to be added to the key
    #NewSet = FullNamesSet - KeySet

    # For each name in the new set, add it to the key, with the corresponding number
   # for Name in NewSet:
      #  key.append([len(key) + 1, Name])

    # Convert the key into a Pandas DataFrame to make it easier to work with
   # dfKey = pd.DataFrame(key)

    # Split the 1 column of the key into two columns at the whitespace
   # dfKey[[1, 2]] = dfKey[1].str.split(' ', expand=True)

    # Covert the DataFrame back into a regular python 2d list
   # key = dfKey.values.tolist()

    # Import csv that will write the key to a spreadsheet
    import csv
    with open('AddingFullNames.csv', 'w', encoding='UTF8', newline='') as f:
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
key = addFullNames(keyLocation, dataFileLocation)