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
        return hash((self.row, self.col, self.control))

class Neighbors:
    top_left     = Coord(None, None)
    top_right    = Coord(None, None)
    right        = Coord(None, None)
    bottom_right = Coord(None, None)
    bottom_left  = Coord(None, None)
    left         = Coord(None, None)

    def __init__(self):
        self.top_left     = Coord(None, None)
        self.top_right    = Coord(None, None)
        self.right        = Coord(None, None)
        self.bottom_right = Coord(None, None)
        self.bottom_left  = Coord(None, None)
        self.left         = Coord(None, None)


def SetNeighborTile(inControlDict, inTile, inTeamToSet):
    if (
        ((inTile.neighbors.top_left     in inControlDict.keys()) and (inControlDict[inTile.neighbors.top_left]     != base_control)) or
        ((inTile.neighbors.top_right    in inControlDict.keys()) and (inControlDict[inTile.neighbors.top_right]    != base_control)) or
        ((inTile.neighbors.right        in inControlDict.keys()) and (inControlDict[inTile.neighbors.right]        != base_control)) or
        ((inTile.neighbors.bottom_right in inControlDict.keys()) and (inControlDict[inTile.neighbors.bottom_right] != base_control)) or
        ((inTile.neighbors.bottom_left  in inControlDict.keys()) and (inControlDict[inTile.neighbors.bottom_left]  != base_control)) or
        ((inTile.neighbors.left         in inControlDict.keys()) and (inControlDict[inTile.neighbors.left]         != base_control)) 
    ):
        inTile.control = inTeamToSet
    else:
        inTile.control = (inTeamToSet + 'Border')


def GetAllUnsetNeighbors(inSetToExpand, inControlDict):
    neighborsSet = set();

    for tile in inSetToExpand:
        if ((tile.neighbors.top_left     in inControlDict) and (inControlDict[tile.neighbors.top_left    ] == base_control)): neighborsSet.add(tile.neighbors.top_left    )
        if ((tile.neighbors.top_right    in inControlDict) and (inControlDict[tile.neighbors.top_right   ] == base_control)): neighborsSet.add(tile.neighbors.top_right   )
        if ((tile.neighbors.right        in inControlDict) and (inControlDict[tile.neighbors.right       ] == base_control)): neighborsSet.add(tile.neighbors.right       )
        if ((tile.neighbors.bottom_right in inControlDict) and (inControlDict[tile.neighbors.bottom_right] == base_control)): neighborsSet.add(tile.neighbors.bottom_right)
        if ((tile.neighbors.bottom_left  in inControlDict) and (inControlDict[tile.neighbors.bottom_left ] == base_control)): neighborsSet.add(tile.neighbors.bottom_left )
        if ((tile.neighbors.left         in inControlDict) and (inControlDict[tile.neighbors.left        ] == base_control)): neighborsSet.add(tile.neighbors.left        )

    return neighborsSet

def UpdateTeamNeighborSet(inControlDict, inTeam):
    startingSet = set(filter(lambda x: x.values() == inTeam, inControlDict))
    neighborsSet = GetAllUnsetNeighbors(startingSet, inControlDict)
    if (len(neighborsSet) == 0):
        return GetAllUnsetNeighbors(neighborsSet, inControlDict)
    else:
        return neighborsSet


def SelectTileFromSet(inTeamNeighborSet):
    while len(inTeamNeighborSet) > 0:
        selectedTile = random.choice(inTeamNeighborSet)
        inTeamNeighborSet.remove(selectedTile)
        if selectedTile.control == base_control:
            return selectedTile
    return None

def BuildMapForGroup(inTileGroupDict, inTeamWeights):
    lTotalUnallocatedTiles = len(inTileGroupDict.values())

    lRemainingTeamTiles = dict()
    for team, weight in inTeamWeights.keys():
        lRemainingTeamTiles[team] = int(lTotalUnallocatedTiles * weight)

    while(lTotalUnallocatedTiles > 0):
        for team, teamTilesToAllocate in lRemainingTeamTiles:
            if((teamTilesToAllocate <= 0) or (lTotalUnallocatedTiles <= 0)):
                continue
            while True:
                if(len(teamNeighborSet) <= 0):
                    teamNeighborSet = UpdateTeamNeighborSet(inTileGroupDict, team)
                tile = SelectTileFromSet(teamNeighborSet)
                if(tile == None):
                    continue
                SetNeighborTile(inTileGroupDict, tile, team)
                break

            teamTilesToAllocate -= 1
            lTotalUnallocatedTiles -= 1
            
    return



if __name__ == "__main__":
    
    inStartTilesFile = open('starttiles.json', 'r')
    inStartCoordsJson = inStartTilesFile.read()
    lTeamsInfoDict = json.loads(inStartCoordsJson)

    ET.register_namespace('', "http://www.w3.org/2000/svg")
    ET.register_namespace('xmls:xlink', "http://www.w3.org/1999/xlink")
    tree = ET.parse('Basemap.svg')
    root = tree.getroot()

    lNorthTeamsInfoDict = lTeamsInfoDict['North'].items()
    lNorthTeamsStartCoords = dict()
    lNorthTeamWeights = dict()
    for key, value in lNorthTeamsInfoDict:
        lNorthTeamsStartCoords[key] = Coord(value['row'], value['col'])
        weight = value['weight']
        if '/' in weight:
            fraction = Fraction(weight)
            lNorthTeamWeights[key] = float(fraction)
        else:
            lNorthTeamWeights[key] = weight

    
    NorthGroup = tree.findall(".//{http://www.w3.org/2000/svg}g[@id='North']//")

    lNorthTiles = {}
    # lNorthTileControlDict = defaultdict(coord)

    for SVGTile in NorthGroup:
        row = int(SVGTile.attrib.get('row'))
        col = int(SVGTile.attrib.get('col'))
        tile = Tile(row, col)
        
        if(row % 2 == 0):
            tile.neighbors.top_left     = Coord(row - 1, col - 1)
            tile.neighbors.top_right    = Coord(row - 1, col    )
            tile.neighbors.right        = Coord(row    , col + 1)
            tile.neighbors.bottom_right = Coord(row + 1, col    )
            tile.neighbors.bottom_left  = Coord(row + 1, col - 1)
            tile.neighbors.left         = Coord(row    , col - 1)
        else:
            tile.neighbors.top_left     = Coord(row - 1, col    )
            tile.neighbors.top_right    = Coord(row - 1, col + 1)
            tile.neighbors.right        = Coord(row    , col + 1)
            tile.neighbors.bottom_right = Coord(row + 1, col + 1)
            tile.neighbors.bottom_left  = Coord(row + 1, col    )
            tile.neighbors.left         = Coord(row    , col - 1)

        if tile.coord in lNorthTeamsStartCoords.values():
            for team, teamCoords in lNorthTeamsStartCoords.items():
                if(teamCoords == tile.coord and lNorthTeamWeights[team] > 0):
                    tile.control = team
        else:
            tile.control = SVGTile.attrib.get('control')

        lNorthTiles[tile.coord] = tile


    BuildMapForGroup(lNorthTiles, lNorthTeamWeights)

        # startTiles = list(filter(lambda x: x.values() != 'base', northTileControlDict))
    # northStartTiles = {key:value for key,value in northTileControlDict.items() if value != 'base'}

    SouthGroup = tree.findall(".//{http://www.w3.org/2000/svg}g[@id='South']//")


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

    
    # tree.write('output_test.svg')

# cairosvg.svg2png(url="giftest/svg/output_michigan.svg", write_to="giftest/png/output_michigan.png")


# svgoutputpath = "giftest/svg/output_" + team_to_write.lower() + ".svg"
# pngoutputpath = "giftest/png/output_" + team_to_write.lower() + ".png"

# tree.write(svgoutputpath)