def numberDetector(string):
    for i in range(len(string)):
        if not string[i].isalpha():

            return string

name = "sithmobias1"

check = numberDetector(name)
print(check)