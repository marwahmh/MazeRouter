# A star algorithm program that receives different nets to be routed, and finds paths to connect pins that belong to the same net together

import numpy as np
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# class representing a cell and all of it's attributes
class Cell:
    def __init__(self, L, X, Y, taken=0):
        self.taken = taken  # 0 or 1
        self.point = (X, Y, L)
        self.H = 0
        self.G = 0
        self.F = 0
        self.parent = None
        self.children = []

    def setF(self):
        self.F = self.H + self.G


def generateInput():
    output = open("generated_input.txt", "w")
    maxList = []
    tuple = ""
    import readDef
    import readLef

    for net in readDef.listNETS:
        maxLayer = 1
        tempNetName = net.name
        tuple += tempNetName
        # NET connections in DEF
        for con in net.connectionsL:
            # COMPONENTS in DEF
            for comp in readDef.listCOMPONENTS:
                if comp.name == con.split()[0]:
                    # COMPONENT models in MACRO in LEF
                    for macro in readLef.listMACROS:
                        if comp.modName == macro.name:
                            # compare NET PIN with MACRO PIN
                            for pin in macro.pins:
                                if con.split()[1] == pin.name:
                                    tempLayer = pin.layerName[-1]
                                    tempPinx = float(pin.x1y1.split()[0]) + float(
                                        comp.placed.split()[0]) / readDef.UNITS
                                    tempPiny = float(pin.x1y1.split()[1]) + float(
                                        comp.placed.split()[1]) / readDef.UNITS
                                    if float(tempLayer) > maxLayer:
                                        maxLayer = float(tempLayer)
            tuple += " (" + tempLayer[-1] + ", " + str(tempPinx) + ", " + str(tempPiny) + ")"
        # print(tuple)
        tuple += "\n"
        maxList.append(maxLayer)
    # here the tuple is arranged so that the highest layer is placed first
    tupleList = [y for y in (x.strip() for x in tuple.splitlines()) if y]
    zipped = sorted(zip(maxList, tupleList), reverse=True)
    sorted_output = [x for y, x in zipped]
    for line in sorted_output:
        output.write(line + "\n")


def MazeRouter(inFile, outFile):
    'instantiate 3d grid of type cell, reads input file and extract the needed information, calls findPath function and receives the paths of the nets, and saves them to output file'

    # reading input file
    infile = open(inFile)
    content = infile.read()
    infile.close()
    lines = content.split('\n')
    nets = []
    nets2 = []
    h = []
    maxLayer = 0

    for i in lines:
        nets.append(re.findall(r'\((.+?)\)', i, re.DOTALL))
    for i in range(len(nets)):
        nets2.clear()
        for j in nets[i]:
            h.clear()
            h = j.split(', ')
            for k in range(len(h)):
                h[k] = int(h[k])
            nets2.append(tuple(h))
            n = tuple(nets2)
        nets[i] = n
        pp = list(nets[i])
        pp.sort(key=lambda x: x[0])  # sort the nets ascendingly by the layer number
        nets[i] = tuple(pp)
        if nets[i][-1][0] > maxLayer:
            maxLayer = nets[i][-1][0]

    # constants
    print(maxLayer)
    layers = maxLayer + 3
    # layers = int(input('Please enter the max number of layers: ')) #get maximum number of layers needed
    width = 1000
    height = 1000
    viaCost = 10
    # 3d list representing the grid
    grid = [[[0 for k in range(layers)] for j in range(height)] for i in range(width)]

    # covert 3d entries to cells
    for i in range(width):
        for j in range(height):
            for k in range(layers):
                grid[i][j][k] = Cell(k, i, j, 0)

    # Getting paths between pins and writing to the file and plotting nets
    outfile = open(outFile, 'w')
    s = ''
    tempList = []
    ax = plt.gca(projection="3d")
    netsColors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    netsNames = []
    c = 0
    for i in range(len(nets)):
        # print('hi')
        outfile.write('Path for net' + str(i + 1) + ' : ')
        netsNames.append('net' + str(i + 1))
        for j in range(len(nets[i]) - 1):
            tempList += findPath(nets[i][j][0], nets[i][j][1], nets[i][j][2], nets[i][j + 1][0], nets[i][j + 1][1],
                                 nets[i][j + 1][2], grid)  # every target becomes a source
        pltList = list(zip(*tempList))
        ax.scatter(pltList[1], pltList[2], pltList[0], c=netsColors[c], s=1)
        ax.plot(pltList[1], pltList[2], pltList[0], color=netsColors[c], linewidth=1, marker='o', markersize=1)
        if c == 7:
            c = 0
        else:
            c += 1
        s = str(tempList)
        outfile.write(s)
        outfile.write('\n\n')
        tempList.clear()
        pltList.clear()
    plt.legend(netsNames, loc='upper right')
    plt.title('nets')
    plt.show()

    outfile.close()
    print('done')


def HeuristicF(sourcePoint, targetPoint, parentL):
    'calculates the manhattan ditance + the cost of vias between the layers'

    xDist = abs(targetPoint[0] - sourcePoint[0])  # horizontal distance
    yDist = abs(targetPoint[1] - sourcePoint[1])  # vertical distance
    LayerDist = abs(targetPoint[2] - sourcePoint[2])  # distance between layers

    if LayerDist == 0 and (xDist != 0 or yDist != 0) and parentL == sourcePoint[
        2]:  # special case where we have the two points on the same layer but we have to move horizontally on one layer and vertically on another layer, and use two vias
        zDist = 20
    else:
        zDist = LayerDist * 10  # normal cases, multiply layer difference by the cost 10

    return xDist + yDist + zDist


def findPath(L1, x1, y1, L2, x2, y2, grid):
    'returns a path between the two points in the list format : [(L1,x1,y1),(L2,x2,y2)..]'

    path = []
    pathx = []
    pathy = []
    pathz = []

    grid[x1][y1][L1].taken = 1
    startCell = grid[x1][y1][L1]
    targetCell = grid[x2][y2][L2]
    currentCell = startCell

    # append the start pin
    path.append((currentCell.point[2], currentCell.point[0], currentCell.point[1]))

    while True:  # stops inside and returns the path once we meet the target, or breaks if there aren't any possible ways

        x_1 = currentCell.point[0]
        y_1 = currentCell.point[1]
        L_1 = currentCell.point[2]

        if currentCell.point == targetCell.point:
            return path
            break

        # check all posible next cells

        # if int(L_1)%2 != 0: #odd layers M1,M3,M5... Horizontal
        if grid[x_1 + 1][y_1][L_1].taken == 0 and x_1 < 999:
            currentCell.children.append(grid[x_1 + 1][y_1][L_1])  # right cell
        if grid[x_1 - 1][y_1][L_1].taken == 0 and x_1 > 0:
            currentCell.children.append(grid[x_1 - 1][y_1][L_1])  # left cell
        # else: #even layers M2,M4... Vertical
        if grid[x_1][y_1 + 1][L_1].taken == 0 and y_1 < 999:
            currentCell.children.append(grid[x_1][y_1 + 1][L_1])  # north cell
        if grid[x_1][y_1 - 1][L_1].taken == 0 and y_1 > 0:
            currentCell.children.append(grid[x_1][y_1 - 1][L_1])  # south cell
        if grid[x_1][y_1][L_1 + 1].taken == 0:
            currentCell.children.append(grid[x_1][y_1][L_1 + 1])  # up cell
        if grid[x_1][y_1][L_1 - 1].taken == 0:
            currentCell.children.append(grid[x_1][y_1][L_1 - 1])  # down cell

        Fmin = 2000  # initial value for F minimum

        if (len(currentCell.children) != 0):  # if there are valid cells to move to next

            parent = currentCell  # the parent of the next cells is the current cell

            for cell in currentCell.children:  # loop on the cells

                cell.parent = parent  # set the parent of the cell

                cell.H = HeuristicF(cell.point, targetCell.point, cell.parent.point[2])  # calculate H

                # calculate G
                if cell.point[2] == currentCell.point[2]:  # if the child cell is in the same layer
                    # if it is placed horizontally in M1,M3,.. and vertically in M2,M4 , add cost of 1
                    if (cell.point[0] - parent.point[0] != 0 and cell.point[2] % 2 != 0) or (
                            cell.point[1] - parent.point[1] != 0 and cell.point[2] % 2 == 0):
                        cell.G = cell.parent.G + 1  # if I am in the same layer the cost is 1
                    else:  # if it is opposite the specified direction, add very high cost (30)
                        cell.G = cell.parent.G + 30
                else:  # if the cell is in different layer, add the cost of the via (10)
                    cell.G = cell.parent.G + 10  # I add a via to move to other layer

                # update F
                cell.setF()

                # update the current cell every time a smaller F is found so at the end we chose the cell with min F
                if cell.F < Fmin:
                    Fmin = cell.F
                    currentCell = cell

            currentCell.taken = 1  # mark the chosen one as taken
            x_1 = currentCell.point[0]
            y_1 = currentCell.point[1]
            L_1 = currentCell.point[2]

            grid[x_1][y_1][L_1] = currentCell  # update the grid

            grid[parent.point[0]][parent.point[1]][parent.point[
                2]].children = []  # reset the children set of the parent (to avoid redundancy in future use)

            path.append((currentCell.point[2], currentCell.point[0], currentCell.point[1]))  # add the cell to the path

        else:  # if there aren't any valid next cells (children), mark current as no valid (same usage as taken) and go one step back

            del path[-1]
            x_1 = currentCell.point[0]
            y_1 = currentCell.point[1]
            L_1 = currentCell.point[2]

            grid[x_1][y_1][L_1].taken = 1

            currentCell = currentCell.parent

            if currentCell.point == None:  # if we reach the starting point again, it means it faild to find a path
                return path
                break

    grid[x2][y2][L2].taken = 0


generateInput()
MazeRouter('input file 1.txt', 'out file 1.txt')
MazeRouter('input file 2.txt', 'out file 2.txt')
