# this file will only read MACRO of class CORE
class MACRO:
    def __init__(self, name, pins):
        self.name = name
        self.pins = pins


class PIN:
    def __init__(self, name, direction, layerName, x1y1, x2y2):
        self.name = name
        self.direction = direction
        self.layerName = layerName
        self.x1y1 = x1y1
        self.x2y2 = x2y2


listMACROS = []
listPINS = []
appended = True

lef = open("osu035.lef", "rt")
contents = lef.readlines()
lef.close()

for line in contents:
    if line.split() and line.split()[0] == "MACRO":
        # print(line.split()[1])
        if not appended:
            listMACROS.append(MACRO(tempMacroName, listPINS))
            listPINS = []
            appended = True
        if line.split()[1] != "FILL" and "PAD" not in line:
            appended = False
            tempMacroName = line.split()[1]
            # print("MACRO " + tempMacroName)
            x = 7  # assume there are 7 lines between MACRO and PIN
            while True:
                first = True
                # print(contents[contents.index(line) + x].strip())
                if "RECT" not in contents[contents.index(line) + x] and "END" not in contents[contents.index(line) + x]:
                    if contents[contents.index(line) + x].split()[1] == "gnd" or \
                            contents[contents.index(line) + x].split()[1] == "vdd" or \
                            contents[contents.index(line) + x].split()[1] == "CLK":
                        break
                    tempPinName = contents[contents.index(line) + x].split()[1]
                    # print("PIN " + tempPinName)
                    x += 1
                    tempPinDirection = contents[contents.index(line) + x].split()[1]
                    # print(tempPinDirection)
                    x += 2
                    tempPinLName = contents[contents.index(line) + x].split()[1]
                    # print(tempPinLName)
                    x += 1
                    # listPINS.append(PIN(tempPinName, tempPinDirection, tempPinLName))
                elif "RECT" in contents[contents.index(line) + x] and first:
                    tempx1y1 = contents[contents.index(line) + x].split()[1] + " " + \
                               contents[contents.index(line) + x].split()[2]
                    tempx2y2 = contents[contents.index(line) + x].split()[3] + " " + \
                               contents[contents.index(line) + x].split()[4]
                    # print(tempx1y1)
                    # print(tempx2y2)
                    listPINS.append(PIN(tempPinName, tempPinDirection, tempPinLName, tempx1y1, tempx2y2))
                    first = False
                    x += 1
                else:
                    x += 1

# for obj in listMACROS:
#     print(obj.name)
#     for x in obj.pins:
#         print(x.name)
#         print(x.direction)
#         print(x.layerName[-1])
#         print(x.x1y1)
#         print(x.x2y2)
#         print(" ")
#

import readDef

output = open("generated_input.txt", "w")

for net in readDef.listNETS:
    tempNetName = net.name
    tuple = tempNetName
    # NET connections in DEF
    for x in net.connectionsL:
        # COMPONENTS in DEF
        for comp in readDef.listCOMPONENTS:
            if comp.name == x.split()[0]:
                # COMPONENT models in MACRO in LEF
                for macro in listMACROS:
                    if comp.modName == macro.name:
                        # compare NET PIN with MACRO PIN
                        for y in macro.pins:
                            if x.split()[1] == y.name:
                                tempLayer = y.layerName
                                tempPinx = float(y.x1y1.split()[0]) + float(comp.placed.split()[0])
                                tempPiny = float(y.x1y1.split()[1]) + float(comp.placed.split()[1])
        tuple += " (" + tempLayer[-1] + ", " + str(tempPinx) + ", " + str(tempPiny) + ")"
    output.write(tuple+"\n")
