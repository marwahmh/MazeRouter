class DIEAREA:
    def __init__(self, llxy, urxy):  # lower left x|y, upper right x|y
        self.llxy = llxy
        self.urxy = urxy


class TRACKS:  # list
    def __init__(self, orientation, start, numTracks, step, layer):
        self.orientation = orientation
        self.start = start
        self.numTracks = numTracks
        self.step = step
        self.layer = layer


class COMPONENT:  # list
    def __init__(self, name, modName, placed, orientation):
        self.name = name  # component name
        self.modName = modName  # model name
        self.placed = placed  # coordinates
        self.orientation = orientation


class PIN:  # list
    def __init__(self, name, layerName, layerSpacing, layerWidth, placed, orientation):
        self.name = name
        self.layerName = layerName
        self.layerSpacing = layerSpacing
        self.layerWidth = layerWidth
        self.placed = placed
        self.orientation = orientation


class NET:  # list
    def __init__(self, name, connectionsL, special):
        self.name = name
        self.connectionsL = connectionsL
        self.special = special
        # since SPECIALNETS has the same format we will just add a bool

    def addConnection(self, connection):
        self.connectionsL.append(connection)


listTRACKS = []
listCOMPONENTS = []
listPINS = []
listNETS = []

deff = open("crc32.def", "rt")
contents = deff.readlines()
deff.close()

for line in contents:
    if line.find("UNITS") != -1:
        UNITS = int(line.split()[-2])
        # print(UNITS)

    if line.find("DIEAREA") != -1:
        tempDieArea = line.split()
        tempLLX = tempDieArea[2] + " " + tempDieArea[3]
        # print(tempLLX)
        tempLLY = tempDieArea[6] + " " + tempDieArea[7]
        # print(tempLLY)
        diearea = DIEAREA(tempLLX, tempLLY)

    if line.find("TRACKS") != -1:
        tempTrack = line.split()
        tempOrientation = tempTrack[1]  # x|y
        tempStart = tempTrack[2]  # point on x|y
        tempNumTracks = tempTrack[4]  # number of tracks
        tempStep = tempTrack[6]  # step
        tempTrackLayer = tempTrack[8]  # layer
        listTRACKS.append(TRACKS(tempOrientation, tempStart, tempNumTracks, tempStep, tempTrackLayer))

    if line.find("COMPONENTS") != -1 and line.find("END COMPONENTS") == -1:
        Ccount = int(line.split()[1])
        for x in range(1, Ccount):
            tempComponents = contents[contents.index(line) + x].split()
            tempCName = tempComponents[1]
            tempMName = tempComponents[2]
            tempPlaced = tempComponents[6] + " " + tempComponents[7]
            tempOrientation = tempComponents[9]
            # print(tempName)
            # print(tempMName)
            # print(tempPlaced)
            # print(tempOrientation)
            # print(" ")
            listCOMPONENTS.append(COMPONENT(tempCName, tempMName, tempPlaced, tempOrientation))

    if line.find("PINS") != -1 and line.find("END PINS") == -1:
        pinCount = int(line.split()[1])
        # print(pinCount)
        for x in range(1, pinCount * 3, 3):
            tempPinName = contents[contents.index(line) + x].rstrip("\n")
            tempPinName = tempPinName[tempPinName.find("NET") + 4:]
            # print(tempPinName)
            tempPinLayer = contents[contents.index(line) + x + 1].rstrip("\n")
            tempPinLayer = tempPinLayer.split()
            tempPinLName = tempPinLayer[2]
            tempPinLSpacing = tempPinLayer[4] + " " + tempPinLayer[5]
            tempPinLWidth = tempPinLayer[8] + " " + tempPinLayer[9]
            # print(tempPinLWidth)
            tempPinPlaced = contents[contents.index(line) + x + 2].rstrip("\n")
            tempPinPlaced = tempPinPlaced.split()
            tempPinOrientation = tempPinPlaced[6]
            # print(tempPinOrientation)
            tempPinPlaced = tempPinPlaced[3] + " " + tempPinPlaced[4]
            # print(tempPinPlaced)
            listPINS.append(
                PIN(tempPinName, tempPinLName, tempPinLSpacing, tempPinLWidth, tempPinPlaced, tempPinOrientation))

    if line.find("NETS") != -1 and line.find("END NETS") == -1 and line.find("SPECIALNETS") == -1:
        netCount = int(line.split()[1])
        # print(netCount)
        x = 1
        appended = False
        tempCList = []
        while True:
            if contents[contents.index(line) + x].strip() == "END NETS":
                break
            else:
                if contents[contents.index(line) + x][0] == "-":
                    # net name
                    tempNetName = contents[contents.index(line) + x].split()[1]
                    # print(tempNetName)
                if contents[contents.index(line) + x + 1][0] == "+":
                    if not appended:
                        listNETS.append(NET(tempNetName, tempCList, False))
                        appended = True
                    tempCList = []
                    while True:
                        if contents[contents.index(line) + x].split()[-1] != ";":
                            x += 1
                            continue
                        else:
                            appended = False
                            break
                else:
                    tempConnection = contents[contents.index(line) + x + 1].split()[1] + " " + \
                                     contents[contents.index(line) + x + 1].split()[2]
                    # print(tempConnection)
                    tempCList.append(tempConnection)
                    # print(tempCList[0])
                    # listNETS.append(NET(NET.addConnection(tempConnection)))
                x += 1

# TESTING
# print(diearea.llxy)
# print(diearea.urxy)

# for obj in listTRACKS:
#     print(obj.orientation)
#     print(obj.start)
#     print(obj.numTracks)
#     print(obj.step)
#     print(obj.layer)

# for obj in listCOMPONENTS:
#     print(obj.name)
#     print(obj.modName)
#     print(obj.placed)
#     print(obj.orientation)

# for obj in listPINS:
#     print(obj.name)
#     print(obj.layerName)
#     print(obj.layerSpacing)
#     print(obj.layerWidth)
#     print(obj.placed)
#     print(obj.orientation)

# for obj in listNETS:
#     print(obj.name)
#     print(obj.connectionsL)
#

# split connections and check highest layer
