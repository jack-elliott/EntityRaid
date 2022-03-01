"""
This code will take 2 .csv files for deidentification and return a de-identified (by the second) version of the first
file 1 is a .csv formatted like qualtrics outputs of survey responses
file 2 is a .csv with 1 column of key numeric values, and following columns with names (row matches key numeric value)
make a change
make a second change
"""

#define the main function
def replacingFunc(dataFileLocation,keyLocation,outputFileName):
    
    #import libraries necessary and assign aliases
    import pandas as pd

    #read in the data file of interest to a list
    data = pd.read_csv(dataFileLocation, header = None)
    data = data.values.tolist()
    
    #read in the key file to a list
    key = pd.read_csv(keyLocation, header = None)
    key = key.values.tolist()

    #concatenate the names in the open responses
    for i in range(len(data)):
        
        #concatenate the names and then delate the column value of the last name for the first 10 responses
        for p in range(10):
            data[i][25+p] = str(data[i][25+p]) + str(data[i][26+p])
            del data[i][26+p]
            
        #concatenate the names and then delate the column value of the last name for the second 10 responses
        for p in range(10):
            data[i][66+p] = str(data[i][66+p]) + str(data[i][67+p])
            del data[i][67+p]
    
    #Convert all of the data strings to just lowercase and remove all white space to make life easier
    for i in range(len(data)): #loop through the whole list of data
        for j in range(len(data[0])): #loop through each element per row
            if isinstance(data[i][j],str): #check if each element is a string, if so convert to upper and remove whitespace
                data[i][j] = data[i][j].lower()
                data[i][j] = data[i][j].replace(" ","")
                
    #Now loop through the entier list of data, and replace values in the key with the numeric values in the first index of each row
    for i in range(len(data)):
        for j in range(len(data[0])):

            #now that we are at each data list element, check the key value rows
            for l in range(len(key)):
        
                #now in each row, check each column in the key, starting after the numeric value
                for m in range(len(key[l]) - 1):
                    
                    mCheck =m + 1 #make sure to skip the first value
                    
                    #Check if the key value matches the data value, if so reassign, if not contnue
                    if data[i][j] == key[l][mCheck]:
                        data[i][j] = key[l][0]
                        
    #write the data file to a .csv
    import csv
    with open('Tester.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
    
        # write the .csv
        writer.writerows(data)

    #spit these out so we can check to make sure deals work
    return(key,data)
    
#This should be the absolute path file location of the qualtrics data file
dataFileLocation = "C:/Users/Elliott/Desktop/Primary+Name+Generator+Survey_September+13,+2021_18.53 (1).csv"

#This should be the file location on your computer of the key .csv
keyLocation = "C:/Users/Elliott/Desktop/Key.csv"

#Define the output name of interest
outputFileName = "Test1"

#this will just run the script
key,data = replacingFunc(dataFileLocation,keyLocation,outputFileName)










































