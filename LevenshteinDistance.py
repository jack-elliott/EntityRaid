# Import the respective libraries
from Levenshtein import distance as lev
import phonetics

# Right now, I choose these values. The code is based on contrasting two string values
# Eventually, I will need to import these values from the key and interaction data
KeyName = 'christianboss'
AmbiguousName = 'chrisboss'

# This is a simple Levenshtein Distance calculation from the library. I print this value to confirm its validity
LevenshteinDistance = lev(KeyName, AmbiguousName)
print(LevenshteinDistance)

# This calculates the phonetic key according to the double metaphone for the KEY name
PhoneticCodeKey = phonetics.dmetaphone(KeyName)
print(PhoneticCodeKey)

# This calculates the phonetic key according to the double metaphone for the AMBIGUOUS name
PhoneticCodeAmbiguous = phonetics.dmetaphone(AmbiguousName)
print(PhoneticCodeAmbiguous)

# This if statement serves as the consolidation parameters.
# Eventually, I want to confirm the effectiveness of these measures through reading related research
if PhoneticCodeKey == PhoneticCodeAmbiguous or LevenshteinDistance == 1:
    print("Consolidate")

# If the name doesn't meet our consolidation parameters, it will get send to a clustering process, right?
else:
    print("Send to hierarchical clustering??")

# QUESTIONS:
# 1. The Levenshtein Distance is great, but doesn't account for potential nicknames
#              -We could use a double Levenshtein Distance calculation. This would include:
#                   Comparing last names with a Levenshtein Distance, then
#                   If this yields a distance of one, save these string values in a list
#                   We then could compare just the first letter of the first name to see if they match
#                   ...if they do, we could either:
#                           -Consolidate
#                           -Use this information in the clustering process?




