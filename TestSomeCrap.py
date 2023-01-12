import pandas as pd

ParticipantNames = [['rachel', 'didericksen', 'rach', '02341406'], ['alex', 'Palmer', 'allie', '01690589'], ['rachel', 'didericksen', 'racheypoo, rachey', '02341406'], ['abigail', 'englund', 'abby', '02350686'], ['rachel', 'didericksen', 'rachelly or rachell', '02341406'], ['aspen', 'norton', 'aspen', '02361299'], ['spencer', 'wagner', 'spenc', '02285221'], ['alex', 'white', 'none', '02276108'], ['crystal', 'tingle', 'crystal', '02273709'], ['ryan', 'kirby', 'nan', '2021926'], ['kathryn', 'stuart', 'kate', '02268447'], ['scott', 'mershon', 'na', '02273856'], ['emmaline', 'haderlie', 'na', '02341727'], ['andrew', 'crook', 'na', '02214585'], ['alyson', 'cinq-mars', 'aly', '02308935'], ['adam', 'murdock', 'na', '02244656'], ['marshall', 'burrows', 'na', '02334079'], ['jarik', 'young', 'na', '02355577'], ['avery', 'mitchell', 'aveman', '02269380'], ['daniela', 'medina', 'dani', '02315251']]
newANumberColumn = 3
newNicknameColumn = 2
newParticipantNamesColumns = [0, 1]
key = [['02288811', '1', 'adam', 'weaver', 'none', 'none'], ['02341406', '2', 'rachel', 'didericksen', 'none', 'none']]
keyentry = key

def keyPositionANUMBER(Anumber, key):
    # now check each key row
    for i in range(len(key)):

        # Check the first name in the key
        if Anumber == key[i][0]:

            return float(i + 1)

    # if the name was not already in the key (made it here), return true
    return True

def registrarData(ANumber, keyentry, ParticipantNameList):
    # now check each key row

    for i in range(len(ParticipantNameList)):

        anumber = ParticipantNameList[i][newANumberColumn]
        if not isinstance(anumber, float):
            if anumber[0] == "a" and len(anumber) == 9:
                ParticipantNameList[i][newANumberColumn] = anumber[1] + anumber[2] + anumber[3] + anumber[4] + anumber[5] + anumber[6] + anumber[7] + anumber[8]

        if anumber == ANumber:
            KeyPosition = keyPositionANUMBER(ANumber, keyentry)

    if isinstance(KeyPosition, float):
        return int(KeyPosition)
    else:
        return False

AnumberCheck = ['filler', False]
for l in range(len(ParticipantNames)):
    for m in range(len(ParticipantNames[0]) - 1):
        ParticipantName = [ParticipantNames[l][0], ParticipantNames[l][1]]
        print(ParticipantName)
        ANUMBER = ParticipantNames[l][newANumberColumn]
        if not isinstance(ParticipantNames[l][newNicknameColumn], float):
            if not registrarData(ANUMBER, keyentry, ParticipantNames):
                AnumberCheck = [ANUMBER, True]
                if "," in ParticipantNames[l][newNicknameColumn]:
                    SplitComma = ParticipantNames[l][newNicknameColumn].split(",")
                    for i in range(len(SplitComma)):
                        SplitComma[i] = SplitComma[i].replace(" ", "")
                    key.append([ANUMBER, len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])
                    for name in SplitComma:
                        if " " in name:
                            SplitCommaSpace = name.split(" ")
                            if SplitCommaSpace[1] != ParticipantNames[l][1]:
                                AnumberCheck = [ANUMBER, True]
                                key[len(key) - 1].append(name)
                                key[len(key) - 1].append(ParticipantNames[l][1])

                                key[len(key) - 1].append(SplitCommaSpace[0])
                                key[len(key) - 1].append(ParticipantNames[l][1])

                                key[len(key) - 1].append(SplitCommaSpace[1])
                                key[len(key) - 1].append(ParticipantNames[l][1])
                            else:
                                AnumberCheck = [ANUMBER, True]
                                key[len(key) - 1].append(SplitCommaSpace[0])
                                key[len(key) - 1].append(SplitCommaSpace[1])
                        else:
                            AnumberCheck = [ANUMBER, True]
                            key[len(key) - 1].append(name)
                            key[len(key) - 1].append(ParticipantNames[l][m + 1])
                if "or" in ParticipantNames[l][newNicknameColumn]:
                    SplitOr = ParticipantNames[l][newNicknameColumn].split('or')
                    for i in range(len(SplitOr)):
                        SplitOr[i] = SplitOr[i].replace(" ", "")
                    key.append([ANUMBER, len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])
                    for name in SplitOr:
                        if " " in name:
                            SplitOrSpace = name.split(" ")
                            if SplitOrSpace[1] != ParticipantNames[l][1]:
                                AnumberCheck = [ANUMBER, True]
                                key[len(key) - 1].append(name)
                                key[len(key) - 1].append(ParticipantNames[l][1])

                                key[len(key) - 1].append(SplitOrSpace[0])
                                key[len(key) - 1].append(ParticipantNames[l][1])

                                key[len(key) - 1].append(SplitOrSpace[1])
                                key[len(key) - 1].append(ParticipantNames[l][1])
                            else:
                                AnumberCheck = [ANUMBER, True]
                                key[len(key) - 1].append(SplitOrSpace[0])
                                key[len(key) - 1].append(SplitOrSpace[1])
                        else:
                            AnumberCheck = [ANUMBER, True]
                            key[len(key) - 1].append(name)
                            key[len(key) - 1].append(ParticipantNames[l][1])
                if "," not in ParticipantNames[l][newNicknameColumn] and " " not in ParticipantNames[l][newNicknameColumn]:
                    key.append([ANUMBER, len(key) + 1, ParticipantName[0], ParticipantName[1]])
                    AnumberCheck = [ANUMBER, True]
                    if ParticipantNames[l][newNicknameColumn] != 'none':
                        if ParticipantNames[l][newNicknameColumn] != 'na':
                            if ParticipantNames[l][newNicknameColumn] != 'nan':
                                print("a", ParticipantNames[l][newNicknameColumn])
                                print("b", ParticipantNames[l][1])
                                key[len(key) - 1].insert(4, ParticipantNames[l][newNicknameColumn])
                                key[len(key) - 1].insert(5, ParticipantNames[l][1])
            if registrarData(ANUMBER, keyentry, ParticipantNames):
                print("Anumber check", AnumberCheck[1])
                if not AnumberCheck[1]:
                    if "," in ParticipantNames[l][newNicknameColumn]:
                        location = int(registrarData(ANUMBER, keyentry, ParticipantNames)) - 1
                        SplitComma = ParticipantNames[l][newNicknameColumn].split(",")
                        for i in range(len(SplitComma)):
                            SplitComma[i] = SplitComma[i].replace(" ", "")
                        ColumnLocationList = []
                        for i in range(len(key[location])):
                            if key[location][i] == "none":
                                ColumnLocation = i
                                ColumnLocationList.append(ColumnLocation)
                        if ColumnLocationList:
                            ActualColumnLocation = min(ColumnLocationList)
                        if not ColumnLocationList:
                            ActualColumnLocation = 1
                        if ParticipantNames[l][newNicknameColumn] not in key[location]:
                            for name in SplitComma:
                                if " " in name:
                                    SplitCommaSpace = name.split(" ")
                                    if SplitCommaSpace[1] != ParticipantNames[l][1]:
                                        key[location].insert(ActualColumnLocation, name)
                                        key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                                        key[location].insert(ActualColumnLocation + 2, SplitCommaSpace[0])
                                        key[location].insert(ActualColumnLocation + 3, ParticipantNames[l][1])

                                        key[location].insert(ActualColumnLocation + 4, SplitCommaSpace[1])
                                        key[location].insert(ActualColumnLocation + 5, ParticipantNames[l][1])
                                    else:
                                        key[location].insert(ActualColumnLocation, SplitCommaSpace[0])
                                        key[location].insert(ActualColumnLocation + 1, SplitCommaSpace[1])
                                else:
                                    key[location].insert(ActualColumnLocation, name)
                                    key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])
                    if "or" in ParticipantNames[l][newNicknameColumn]:
                        location = int(registrarData(ANUMBER, keyentry, ParticipantNames)) - 1
                        SplitOr = ParticipantNames[l][newNicknameColumn].split('or')
                        for i in range(len(SplitOr)):
                            SplitOr[i] = SplitOr[i].replace(" ", "")
                        ColumnLocationList = []
                        for i in range(len(key[location])):
                            if key[location][i] == "none":
                                ColumnLocation = i
                                ColumnLocationList.append(ColumnLocation)
                        if ColumnLocationList != []:
                            ActualColumnLocation = min(ColumnLocationList)
                        if ParticipantNames[l][newNicknameColumn] not in key[location]:
                            for name in SplitOr:
                                if " " in name:
                                    SplitOrSpace = name.split(" ")
                                    if SplitOrSpace[1] != ParticipantNames[l][1]:
                                        key[location].insert(ActualColumnLocation, name)
                                        key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                                        key[location].insert(ActualColumnLocation + 2, SplitOrSpace[0])
                                        key[location].insert(ActualColumnLocation + 3, ParticipantNames[l][1])

                                        key[location].insert(ActualColumnLocation + 4, SplitOrSpace[1])
                                        key[location].insert(ActualColumnLocation + 5, ParticipantNames[l][1])
                                    else:
                                        key[location].insert(ActualColumnLocation, SplitOrSpace[0])
                                        key[location].insert(ActualColumnLocation + 1, SplitOrSpace[1])
                                else:
                                    key[location].insert(ActualColumnLocation, name)
                                    key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                    if "," not in ParticipantNames[l][newNicknameColumn] and " " not in ParticipantNames[l][newNicknameColumn]:
                        location = int(registrarData(ANUMBER, keyentry, ParticipantNames)) - 1
                        ColumnLocationList = []
                        for i in range(len(key[location])):
                            if key[location][i] == "none":
                                ColumnLocation = i
                                ColumnLocationList.append(ColumnLocation)
                            else:
                                ActualColumnLocation = 4
                        if ColumnLocationList != []:
                            ActualColumnLocation = min(ColumnLocationList)
                        if not isinstance(location, float):
                            if ParticipantNames[l][newNicknameColumn] != 'none':
                                print("hello", ParticipantNames[l][newNicknameColumn])
                                print(ParticipantName[1])
                                key[location].insert(ActualColumnLocation, ParticipantNames[l][newNicknameColumn])
                                key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
print(key)