    # loop through each of the raw data rows
    for l in range(len(ParticipantNames)):

        # loop through each raw data column (set of names) corresponding to a given name not,
        # first names are in cols 1,3,5,... last names col. 2,4,6,...
        for m in range(len(ParticipantNames[0]) - 1):

            # identify the name to be checked for in the key
            ParticipantName = [ParticipantNames[l][0], ParticipantNames[l][1]]
            ANUMBER = ParticipantNames[l][newANumberColumn]

# ==================================================NICKNAMES========================================================= #


            if ParticipantNames[l][newNicknameColumn] != "N/A" or "NA" or "na" or "n/a" or "none" or "None" or "Nope":
                if not isinstance(ParticipantNames[l][newNicknameColumn], float):
# --------------------------------------------- SEPARATED BY COMMA -----------------------------------------------------
                    if "," in ParticipantNames[l][newNicknameColumn]:

                        ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].replace(", ", ",")
                        SplitComma = ParticipantNames[l][newNicknameColumn].split(",")

                        locationtwo = registrarData(ANUMBER, ParticipantNames[l], key, ParticipantNames)

                        #check = looper(ParticipantName, key)
                        anumberlocation = keyPosition(ParticipantName, key)

                        print("splitcomma", SplitComma)
                        print("location", location)

                        if location:

                            print("what about here")
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
                                    print("HERE?", name)

                                    if " " in name:
                                        SplitCommaSpace = name.split(" ")
                                        if SplitCommaSpace[1] != ParticipantNames[l][1]:

                                            print("name got down here", name)

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

                                        print("zac your ANUMBER is", ANUMBER)
                                        print("zac are you here", name)
                                        print("zac your location is", location)
                                        key[location].insert(ActualColumnLocation, name)
                                        key[location].insert(ActualColumnLocation + 1, ParticipantNames[l][1])


                        else:

                            if locationtwo:

                                ColumnLocationList = []
                                for i in range(len(key[locationtwo])):
                                    if key[locationtwo][i] == "none":
                                        ColumnLocation = i
                                        ColumnLocationList.append(ColumnLocation)
                                if ColumnLocationList:
                                    ActualColumnLocation = min(ColumnLocationList)

                                if not ColumnLocationList:
                                    ActualColumnLocation = 1

                                if ParticipantNames[l][newNicknameColumn] not in key[locationtwo]:

                                    for name in SplitComma:
                                        print("HERE?", name)

                                        if " " in name:
                                            SplitCommaSpace = name.split(" ")
                                            if SplitCommaSpace[1] != ParticipantNames[l][1]:

                                                print("name got down here", name)

                                                key[locationtwo].insert(ActualColumnLocation, name)
                                                key[locationtwo].insert(ActualColumnLocation + 1, ParticipantNames[l][1])

                                                key[locationtwo].insert(ActualColumnLocation + 2, SplitCommaSpace[0])
                                                key[locationtwo].insert(ActualColumnLocation + 3, ParticipantNames[l][1])

                                                key[locationtwo].insert(ActualColumnLocation + 4, SplitCommaSpace[1])
                                                key[locationtwo].insert(ActualColumnLocation + 5, ParticipantNames[l][1])

                                            else:

                                                key[locationtwo].insert(ActualColumnLocation, SplitCommaSpace[0])
                                                key[locationtwo].insert(ActualColumnLocation + 1, SplitCommaSpace[1])

                                        else:

                                            print("zac your ANUMBER is", ANUMBER)
                                            print("zac are you here", name)
                                            print("zac your location is", location)
                                            key[locationtwo].insert(ActualColumnLocation, name)
                                            key[locationtwo].insert(ActualColumnLocation + 1, ParticipantNames[l][1])
                            else:

                                print("here")

                                key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])

                                for name in SplitComma:

                                    if " " in name:
                                        SplitCommaSpace = name.split(" ")

                                        if SplitCommaSpace[1] != ParticipantNames[l][1]:

                                            key[len(key) - 1].append(name)
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                            key[len(key) - 1].append(SplitCommaSpace[0])
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                            key[len(key) - 1].append(SplitCommaSpace[1])
                                            key[len(key) - 1].append(ParticipantNames[l][1])

                                        else:

                                            key[len(key) - 1].append(SplitCommaSpace[0])
                                            key[len(key) - 1].append(SplitCommaSpace[1])

                                    else:

                                        key[len(key) - 1].append(name)
                                        key[len(key) - 1].append(ParticipantNames[l][m + 1])

    # -------------------------------------------- SEPARATED BY AN OR ------------------------------------------------------

                    if "or" in ParticipantNames[l][newNicknameColumn]:

                        location = registrarData(ANUMBER, ParticipantNames[l], key, ParticipantNames)
                        ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].replace(" or ", "or")
                        SplitOr = ParticipantNames[l][newNicknameColumn].split('or')

                        #check = looper(ParticipantName, key)
                        #location = keyPosition(ParticipantName, key)

                        if location:

                            key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])

                            for name in SplitOr:

                                if " " in name:
                                    SplitOrSpace = name.split(" ")

                                    if SplitOrSpace[1] != ParticipantNames[l][1]:

                                        key[len(key) - 1].append(name)
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                        key[len(key) - 1].append(SplitOrSpace[0])
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                        key[len(key) - 1].append(SplitOrSpace[1])
                                        key[len(key) - 1].append(ParticipantNames[l][1])

                                    else:
                                        key[len(key) - 1].append(SplitOrSpace[0])
                                        key[len(key) - 1].append(SplitOrSpace[1])

                                else:

                                    key[len(key) - 1].append(name)
                                    key[len(key) - 1].append(ParticipantNames[l][1])

                        else:

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

                        ParticipantNames[l][newNicknameColumn] = ParticipantNames[l][newNicknameColumn].replace("or", " or ")

    #  ------------------------------------JUST ONE NICKNAME-----------------------------------------------------------#

                    if "," not in ParticipantNames[l][newNicknameColumn] and " " not in ParticipantNames[l][newNicknameColumn]:

                        check = looper(ParticipantName, key)
                        location = keyPosition([ParticipantNames[l][m], ParticipantNames[l][m + 1]], key)

                        checktwo = looper([ParticipantNames[l][newNicknameColumn], ParticipantName[1]], key)
                        locationtwo = keyPosition([ParticipantNames[l][newNicknameColumn], ParticipantName[1]], key)

                        checkthree = registrarData(ANUMBER, ParticipantNames[l], key, ParticipantNames)

                        if not checkthree: # if A-number matches and

                            if not check: # if name is in the key, but ...

                                if checktwo: # ... nickname is not in the key

                                    ColumnLocationList = []
                                    for i in range(len(key[location])):
                                        if key[location][i] == "none":
                                            ColumnLocation = i
                                            ColumnLocationList.append(ColumnLocation)
                                        else:
                                            ActualColumnLocation = 3
                                    if ColumnLocationList != []:
                                        ActualColumnLocation = min(ColumnLocationList)

                                    print(ParticipantNames[l][0])
                                   # print(ParticipantNames[l][1])
                                   # print(locationtwo)
                                    print(location)

                                    if not isinstance(location, float):
                                       # print("LOCATION IS", location)
                                        key[location].insert(ActualColumnLocation, ParticipantNames[l][newNicknameColumn])
                                        key[location].insert(ActualColumnLocation + 1, ParticipantName[1])
                            ##############
                        if checkthree: # if A-number does not match (yet, at least)

                            if check: # if name is NOT in the key, but ...

                                if not checktwo: # ... nickname IS in the key

                                    ColumnLocationList = []
                                    for i in range(len(key[locationtwo])):
                                        if key[locationtwo][i] == "none":
                                            ColumnLocation = i
                                            ColumnLocationList.append(ColumnLocation)
                                        else:
                                            ActualColumnLocation = 3
                                    if ColumnLocationList != []:
                                        ActualColumnLocation = min(ColumnLocationList)

                                    if not isinstance(locationtwo, float):
                                       # print("LOCATION IS", location)
                                        key[locationtwo].insert(ActualColumnLocation, ParticipantNames[l][m])
                                        key[locationtwo].insert(ActualColumnLocation + 1, ParticipantName[1])
                                        #########
                        else: # if A-number does not match
                            if checktwo: # if nickname is not in the key
                                if check: # AND the name is not already in the key
                                    key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1],
                                           ParticipantNames[l][newNicknameColumn], ParticipantNames[l][1]])

# ===============================================END NICKNAME========================================================= #

           # check = looper(ParticipantName, key)
          #  checkthree = registrarData(ANUMBER, ParticipantNames[l], key, ParticipantNames)

           # if not isinstance(ParticipantNames[l][newNicknameColumn], float):
           #     if "," not in ParticipantNames[l][newNicknameColumn] and " " not in ParticipantNames[l][newNicknameColumn]:
           #         checktwo = looper([ParticipantNames[l][newNicknameColumn], ParticipantNames[l][1]], key)
           #     else:
           #         checktwo = True
          #  else:
           #     checktwo = True
            # If the name is not in the key, add the name to the key
          #  if check and checktwo and checkthree:
           #     key.append([len(key) + 1, ParticipantNames[l][m], ParticipantNames[l][m + 1]])