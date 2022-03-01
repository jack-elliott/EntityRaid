from Levenshtein import distance as lev
import phonetics

KeyName = 'johndeer'
AmbiguousName = 'jondeere'

LevenshteinDistance = lev(KeyName, AmbiguousName)
print(LevenshteinDistance)

PhoneticCodeKey = phonetics.dmetaphone(KeyName)
print(PhoneticCodeKey)

PhoneticCodeAmbiguous = phonetics.dmetaphone(AmbiguousName)
print(PhoneticCodeAmbiguous)

if PhoneticCodeKey == PhoneticCodeAmbiguous:
    print("Consolidate")








