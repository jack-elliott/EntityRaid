"""
Notes for improvement:
    let's put notes up here in this format for future iterations to start:
    1 - raw data names need to have odd/even iterables according to first/last name. 
        check the looper key iterables for ideas
    
    
"""

#def addParticipantsNames(keyLocation, dataFileLocation):
# import respective libraries
import pandas as pd


keyLocation = 'SyntheticKey.csv'#Local files don't need full path, so we'll keep these in the github folder now
dataFileLocation = 'SyntheticInteractionData.csv'

"""A function to check a given participants' name for whether it is already in a key or not"""
def looper(ParticipantName,key):
        
    #now check each key row
    for i in range(len(key)):
        
        #now check each key column, first names are in cols 1,3,5,... last names col. 2,4,6,...
        for j in range(len(key[i])-2):
                       
            #Check the first name in the key
            if ParticipantName[0] == key[i][j+1]:
                
                #Check the second name IF the first name matches
                if ParticipantName[1] == key[i][j+2]:
                    
                    #If the name is already in the key, return false (makes sense later)
                    return False
                
    #if the name was not already in the key (made it here), return true
    return True     
    
"""A function for pulling registry data and identifying names not yet in the key, then adding those names to the key"""
def addParticipantsNames(keyLocation, dataFileLocation):
    
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
    dfParticipantNames = pd.DataFrame(ParticipantNames)
    dfParticipantNames[[0, 1]] = dfParticipantNames[0].str.split(' ', expand=True)
    ParticipantNames = dfParticipantNames.values.tolist()
    
    #loop through each of the raw data rows
    for l in range(len(ParticipantNames)):
        
        #loop through each raw data column (set of names) corresponding to a given name not, first names are in cols 1,3,5,... last names col. 2,4,6,...
        for m in range(len(ParticipantNames[l]) - 1):
        
                #identify the name to be checked for in the key
                ParticipantName = [ParticipantNames[l][m], ParticipantNames[l][m+1]]
                
                #now run the sub-routine to see if the name is in the key
                check = looper(ParticipantName,key)
            
                #If the name is not in the key, add the name to the key
                if check:
                    key.append([len(key)+1, ParticipantNames[l][m], ParticipantNames[l][m+1]])
    print(key)
    #return the new key (unique new names added)
    return key

key = addParticipantsNames(keyLocation, dataFileLocation)













                    # Check if the key value matches the data value, if so reassign, if not contnue
                  #  if data[i][j] == key[l][m]:
                #        data[i][j] = key[l][0]


    # Create a set out of the registry data
   # ParticipantSet = set()

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

# =============================================================================
#     # Import csv that will write the key to a spreadsheet
#     import csv
#     with open('AddingParticipantsOwnNames17.csv', 'w', encoding='UTF8', newline='') as f:
#         writer = csv.writer(f)
# 
#         # write the .csv
#         writer.writerows(key)
# 
# =============================================================================



# =============================================================================
# # This should be the file location on your computer of the key .csv
# #keyLocation = '/Users/adamweaver/Desktop/SNA/SyntheticKey.csv'
# keyLocation = 'SyntheticKey.csv'#Local files don't need full path, so we'll keep these in the github folder now
# 
# # This should be the absolute path file location of the qualtrics data file
# #dataFileLocation = '/Users/adamweaver/Desktop/SNA/SyntheticInteractionData.csv'
# dataFileLocation = 'SyntheticInteractionData.csv'
# =============================================================================



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
