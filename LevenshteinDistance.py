from Levenshtein import distance as lev

KeyName = 'johndeer'
AmbiguousName = 'jondeere'

LevenshteinDistance = lev(KeyName, AmbiguousName)
print(LevenshteinDistance)

import phonetics

PhoneticCode = phonetics.dmetaphone('lindseyreich')
print(PhoneticCode)





