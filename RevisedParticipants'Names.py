def addParticipantsNames(keyLocation, dataFileLocation):
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

    ParticipantNames = []
    for i in range(len(data)-1):
        # In this case, the names are in the zero column. This will change depending on the survey data formatting.
        ParticipantNames.append([data[1+i][0]])

    # Split the participant Names into First Name/Last Name components
    print(ParticipantNames)
    dfParticipantNames = pd.DataFrame(ParticipantNames)
    dfParticipantNames[[0, 1]] = dfParticipantNames[0].str.split(' ', expand=True)
    ParticipantNames = dfParticipantNames.values.tolist()
    print(ParticipantNames)

    for i in range(len(key)):
        for j in range(len(key[0])-2):

            # now that we are at each data list element, check the key value rows
            for l in range(len(ParticipantNames)):

                # now in each row, check each column in the key, starting after the numeric value
                for m in range(len(ParticipantNames[l])-1):

                    if key[i][j+1] != ParticipantNames[l][m]:
                        if key[i][j+2] != ParticipantNames[l][m+1]:
                            key.append([ParticipantNames[l][m], ParticipantNames[l][m+1]])
    print(key)

                    # Check if the key value matches the data value, if so reassign, if not contnue
                  #  if data[i][j] == key[l][m]:
                #        data[i][j] = key[l][0]


    # Create a set out of the registry data
    ParticipantSet = set()

    # Fill the registry set with values from the FinalRegistry list created above
  #  for Names in ParticipantNames:
     #   ParticipantSet.update(Names)

    # Create a set out of the key
  #  KeySet = set()
  #  for j in key:
   #     KeySet.update(j)

    # Find the values that need to be added to the key
  #  NewSet = ParticipantSet - KeySet

    # For each name in the new set, add it to the key, with the corresponding number
   # for Name in NewSet:
    #    key.append([len(key) + 1, Name])

    # Convert the key into a Pandas DataFrame to make it easier to work with
   # dfKey = pd.DataFrame(key)

    # Split the 1 column of the key into two columns at the whitespace
   # dfKey[[1, 2]] = dfKey[1].str.split(' ', expand=True)

    # Covert the DataFrame back into a regular python 2d list
   # key = dfKey.values.tolist()

    # Import csv that will write the key to a spreadsheet
    import csv
    with open('AddingParticipantsOwnNames15.csv', 'w', encoding='UTF8', newline='') as f:
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

# 1:23-


# IDEAS:
# Create a 2d list from the interaction data with every row reflecting a first name (column 0) and a last name (column 1)
# Iterate through the participant names list AND interaction data list to find matches. Then, I would (ACTUALLY THIS JUST ADDS AN EXTRA STEP)

# NEW IDEA:
# Search for the same first name in the interaction data
# If it matches, use the very next column value (on the same row), to search for the very next column value (same row) in the interaction data
# If that matches, then the name is a match. Replace both instances with the key value number

# Search fo the same first name in the key
# If it does not match, use the very next column value ( on the same row), to search for a match in the very  next column value (same row) in the key
# If this does not match either, then we can add both the first and last name components to the key (with a new key value)
# all lowercase, remove special characters
# remove triple name instances
#