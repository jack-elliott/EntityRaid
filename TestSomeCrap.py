name = ['bob', 'weaver-nielson']

def hyphenDetector(string):
    for i in range(0, len(string)):
        if string[i] == '-':
            return True

bob = hyphenDetector(name[1])
if bob:
    print("This is working")
