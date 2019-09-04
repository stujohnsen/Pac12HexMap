import time, json, random
from fractions import Fraction
from collections import defaultdict

# import cairosvg
import xml.etree.ElementTree as ET

base_control = 'base'

class Coord:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.row == other.row) and (self.col == other.col)
        else:
            return False

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return '(' + repr(self.row) + ', ' + repr(self.col) + ')'

    def __str__(self):
        return '(' + repr(self.row) + ', ' + repr(self.col) + ')'

class Tile:
    coord = Coord(None, None)
    control = None
    neighbors = None

    def __init__(self, row, col, control=None, neighbors=None):
        self.coord = Coord(row, col)
        self.control = control
        self.neighbors = Neighbors()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.coord == other.coord)
        else:
            return False

    def __hash__(self):
        return hash((self.coord.row, self.coord.col, self.control))

    def __str__(self):
        return 'Coord: ' + repr(self.coord) + ', Control: ' + self.control

    def __repr__(self):
        return repr(self.coord) + ', ' + self.control

class Neighbors:
    top_left     = Coord(None, None)
    top_right    = Coord(None, None)
    right        = Coord(None, None)
    bottom_right = Coord(None, None)
    bottom_left  = Coord(None, None)
    left         = Coord(None, None)

def BuildTilesFromGroup(inGroup, inGroupStartCoords, inGroupStartWeights):

    lGroupTiles = {}

    for SVGTile in inGroup:
        row = int(SVGTile.attrib.get('row'))
        col = int(SVGTile.attrib.get('col'))
        tile = Tile(row, col)
        
        tile.neighbors.top_left     = Coord(row - 1, col - (row % 2))
        tile.neighbors.top_right    = Coord(row - 1, col + (row % 2))
        tile.neighbors.right        = Coord(row    , col + 1)
        tile.neighbors.bottom_right = Coord(row + 1, col + (row % 2))
        tile.neighbors.bottom_left  = Coord(row + 1, col - (row % 2))
        tile.neighbors.left         = Coord(row    , col - 1)

        if tile.coord in inGroupStartCoords.values():
            for team, teamCoords in inGroupStartCoords.items():
                if(teamCoords == tile.coord and inGroupStartWeights[team] > 0):
                    tile.control = team
        else:
            tile.control = SVGTile.attrib.get('control')

        lGroupTiles[tile.coord] = tile

    return lGroupTiles

def UpdateTeamNeighborSet(inControlDict, inTeam):

    startingSet = set(x for x in inControlDict.values() if x.control == inTeam)

    neighborSet = set()

    for tile in startingSet:
        neighborSet.add(tile.coord)

    expansionSet = set()
    unsetNeighbors = set()

    while(len(unsetNeighbors) <= 0):
        neighborSet = neighborSet.union(expansionSet)

        for coord in neighborSet:
            expansionSet.add(Coord(coord.row - 1, coord.col - (coord.row % 2)))
            expansionSet.add(Coord(coord.row - 1, coord.col + (coord.row % 2)))
            expansionSet.add(Coord(coord.row    , coord.col + 1))
            expansionSet.add(Coord(coord.row + 1, coord.col + (coord.row % 2)))
            expansionSet.add(Coord(coord.row + 1, coord.col - (coord.row % 2)))
            expansionSet.add(Coord(coord.row    , coord.col - 1))
    
        newNeighborSet = expansionSet.difference(neighborSet)

        unsetNeighbors = set(x for x in inControlDict.values() if ((x.coord in newNeighborSet) and (x.control == base_control)))

    return unsetNeighbors


def SelectTilesFromSet(inTeamNeighborSet, inRemainingTiles):
    selectedTiles = set(random.sample(inTeamNeighborSet, min(len(inTeamNeighborSet), inRemainingTiles)))
    inTeamNeighborSet.clear()
    return selectedTiles

def BuildMapForGroup(inTileGroupDict, inTeamWeights):
    lUnallocatedTilesSet = set(x for x in inTileGroupDict.values() if x.control == base_control)

    lTotalUnallocatedTiles = len(lUnallocatedTilesSet)

    lRemainingTeamTiles = {}
    lTeamNeighborSets = {}

    for team, weight in inTeamWeights.items():
        lRemainingTeamTiles[team] = int(lTotalUnallocatedTiles * weight)
        lTeamNeighborSets[team] = UpdateTeamNeighborSet(inTileGroupDict, team)

    lUnallocatedTeamTiles = sum(lRemainingTeamTiles.values())

    if(lUnallocatedTeamTiles < lTotalUnallocatedTiles):
        for team in lRemainingTeamTiles:
            if(lUnallocatedTeamTiles < lTotalUnallocatedTiles):
                lRemainingTeamTiles[team] += 1
                lUnallocatedTeamTiles += 1
            else:
                break

    lastNumberOfTilesSet = 0

    while(lTotalUnallocatedTiles > 0):
        for team, remainingTiles in lRemainingTeamTiles.items():
            if((remainingTiles <= 0) or (lTotalUnallocatedTiles <= 0)):
                continue
            currentNeighborSet = None
            if(sum(lRemainingTeamTiles.values()) == remainingTiles):
                currentNeighborSet = set(x for x in inTileGroupDict.values() if x.control == base_control)
            else:
                currentNeighborSet = lTeamNeighborSets[team]
            while True:
                if(len(currentNeighborSet) <= 0):
                    currentNeighborSet = UpdateTeamNeighborSet(inTileGroupDict, team)
                tilesToSet = SelectTilesFromSet(currentNeighborSet, remainingTiles)

                for tile in tilesToSet:
                    inTileGroupDict[tile.coord].control = team
                lastNumberOfTilesSet = len(tilesToSet)
                break

            lRemainingTeamTiles[team] -= lastNumberOfTilesSet
            lTotalUnallocatedTiles -= lastNumberOfTilesSet
            
    return

if __name__ == "__main__":
    
    inStartTilesFile = open('starttiles.json', 'r')
    inStartCoordsJson = inStartTilesFile.read()
    lTeamsInfoDict = json.loads(inStartCoordsJson)

    ET.register_namespace('', "http://www.w3.org/2000/svg")
    ET.register_namespace('xmls:xlink', "http://www.w3.org/1999/xlink")
    tree = ET.parse('Basemap.svg')

    lNorthTeamsInfoDict = lTeamsInfoDict['North'].items()
    lNorthTeamsStartCoords = dict()
    lNorthTeamWeights = dict()
    for key, value in lNorthTeamsInfoDict:
        lNorthTeamsStartCoords[key] = Coord(value['row'], value['col'])
        weight = value['weight']
        if isinstance(weight, str) and '/' in weight:
            fraction = Fraction(weight)
            lNorthTeamWeights[key] = float(fraction)
        else:
            lNorthTeamWeights[key] = float(weight)

    lSouthTeamsInfoDict = lTeamsInfoDict['South'].items()
    lSouthTeamsStartCoords = dict()
    lSouthTeamWeights = dict()
    for key, value in lSouthTeamsInfoDict:
        lSouthTeamsStartCoords[key] = Coord(value['row'], value['col'])
        weight = value['weight']
        if isinstance(weight, str) and '/' in weight:
            fraction = Fraction(weight)
            lSouthTeamWeights[key] = float(fraction)
        else:
            lSouthTeamWeights[key] = weight

    lNorthGroup = tree.findall(".//{http://www.w3.org/2000/svg}g[@id='North']//")
    lSouthGroup = tree.findall(".//{http://www.w3.org/2000/svg}g[@id='South']//")

    lNorthTiles = BuildTilesFromGroup(lNorthGroup, lNorthTeamsStartCoords, lNorthTeamWeights)
    lSouthTiles = BuildTilesFromGroup(lSouthGroup, lSouthTeamsStartCoords, lSouthTeamWeights)

    BuildMapForGroup(lNorthTiles, lNorthTeamWeights)
    BuildMapForGroup(lSouthTiles, lSouthTeamWeights)

    for SVGTile in lNorthGroup:
        row = int(SVGTile.attrib.get('row'))
        col = int(SVGTile.attrib.get('col'))

        tile = lNorthTiles[Coord(row, col)]

        SVGTile.set('control', tile.control)
        

    for SVGTile in lSouthGroup:
        row = int(SVGTile.attrib.get('row'))
        col = int(SVGTile.attrib.get('col'))

        tile = lSouthTiles[Coord(row, col)]

        SVGTile.set('control', tile.control)



    # for tile in northTileList:



    #     if   (row == Cal['row']) and (col == Cal['col']) :
    #         tile.set('control', 'Cal')
    #     elif (row == Oregon['row']) and (col == Oregon['col']) :
    #         tile.set('control', 'Oregon')
    #     elif (row == OSU['row']) and (col == OSU['col']) :
    #         tile.set('control', 'OSU')
    #     elif (row == Stanford['row']) and (col == Stanford['col']) :
    #         tile.set('control', 'Stanford')
    #     elif (row == Washington['row']) and (col == Washington['col']) :
    #         tile.set('control', 'Washington')
    #     elif (row == WSU['row']) and (col == WSU['col']) :
    #         tile.set('control', 'WSU')

    # SouthGroupTemp = dict();

    # for tile in SouthGroup:
    #     row = int(tile.attrib.get('row'))
    #     col = int(tile.attrib.get('col'))
    #     XCoord = int(tile.attrib.get('YCoord'))
    #     YCoord = int(tile.attrib.get('XCoord'))
    #     control = int(tile.attrib.get('control'))

    #     if   (row == Arizona['row']) and (col == Arizona['col']) :
    #         tile.set('control', 'Arizona')
    #     elif (row == ASU['row']) and (col == ASU['col']) :
    #         tile.set('control', 'ASU')
    #     elif (row == Colorado['row']) and (col == Colorado['col']) :
    #         tile.set('control', 'Colorado')
    #     elif (row == UCLA['row']) and (col == UCLA['col']) :
    #         tile.set('control', 'UCLA')
    #     elif (row == USC['row']) and (col == USC['col']) :
    #         tile.set('control', 'USC')
    #     elif (row == Utah['row']) and (col == Utah['col']) :
    #         tile.set('control', 'Utah')

    #     SouthGroupTemp[row][col][]

    
    tree.write('output_test.svg')

# cairosvg.svg2png(url="giftest/svg/output_michigan.svg", write_to="giftest/png/output_michigan.png")


# svgoutputpath = "giftest/svg/output_" + team_to_write.lower() + ".svg"
# pngoutputpath = "giftest/png/output_" + team_to_write.lower() + ".png"

# tree.write(svgoutputpath)