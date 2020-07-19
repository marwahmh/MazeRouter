# this file will only read MACRO of class CORE
class MACRO:
    def __init__(self, name, pins):
        self.name = name
        self.pins = pins


class PIN:
    def __init__(self, name, direction, layerName):
        self.name = name
        self.direction = direction
        self.layerName = layerName


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
                    listPINS.append(PIN(tempPinName, tempPinDirection, tempPinLName))
                else:
                    x += 1

# for obj in listMACROS:
#     print(obj.name)
#     for x in obj.pins:
#         print(x.name)
#         print(x.direction)
#         print(x.layerName)
