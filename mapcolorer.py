import time, json
from fractions import Fraction
from collections import defaultdict
# import cairosvg
import xml.etree.ElementTree as ET

class coord:
    row = int()
    col = int()

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

class neighbors:
    top_left     = coord(None, None)
    top_right    = coord(None, None)
    right        = coord(None, None)
    bottom_right = coord(None, None)
    bottom_left  = coord(None, None)
    left         = coord(None, None)

def SetNeighborTile(controlDict, tile, teamToSet):
    if tile.

    if any neighbor to input tile belongs to other team or any neighbor to input file not in controlDict
        set tile control color to team border
    else
        set tile control color to team
    
def UpdateTeamNeighborSet(inControlDict, team):
    startingSet = filter inControlDict by team as set
    neighborsSet = GetAllUnsetNeighbors(startingSet)
    if neighborsSet is empty:
        return GetAllUnsetNeighbors(neighborsSet)
    else:
        return neighborsSet

def GetAllUnsetNeighbors(inSetToExpand):
    return unset neighbors of inSetToExpand as set

def SelectTileFromSet(teamNeighborSet):
    while len(teamNeighborSet) > 0:
        selectedTile = select random tile from teamNeighborSet
        remove selectedTile from teamNeighborSet
        if selectedTile is unset
            return selected tile
    return None

def BuildMapForGroup(inTileGroupControlDict, inTileGroupNeighborsDict, inTeamWeights):
    lTotalUnallocatedTiles = len(inTileGroupControlDict)

    lRemainingTeamTiles = dict()
    for team, weight in inTeamWeights.keys():
        lRemainingTeamTiles[team] = int(lTotalTiles * weight)

    while(lTotalUnallocatedTiles > 0):
        for team, teamTilesToAllocate in lRemainingTeamTiles:
            if(teamTilesToAllocate <= 0 or lTotalUnallocatedTiles <= 0)
                continue
            while True:
                if len(teamNeighborSet) <= 0
                    teamNeighborSet = UpdateTeamNeighborSet(inTileGroupControlDict, team)
                lTile = SelectTileFromSet(teamNeighborSet)
                if lTile = None
                    continue
                SetNeighborTile(controlDict, tile, teamToSet)
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
        lNorthTeamsStartCoords[key] = coord(value['row'], value['col'])
        weight = value['weight']
        if '/' in weight:
            fraction = Fraction(weight)
            lNorthTeamWeights[key] = float(fraction)
        else:
            lNorthTeamWeights[key] = weight

    
    NorthGroup = tree.findall(".//{http://www.w3.org/2000/svg}g[@id='North']//")

    # northTileList = list()
    lNorthTileNeighborsDict = defaultdict(coord)
    lNorthTileControlDict = defaultdict(coord)

    for tile in NorthGroup:
        row = int(tile.attrib.get('row'))
        col = int(tile.attrib.get('col'))
        tileCoord = coord(row, col)
        tileNeighbors = neighbors()
        
        if(row % 2 == 0):
            tileNeighbors.top_left     = coord(row - 1, col - 1)
            tileNeighbors.top_right    = coord(row - 1, col    )
            tileNeighbors.right        = coord(row    , col + 1)
            tileNeighbors.bottom_right = coord(row + 1, col    )
            tileNeighbors.bottom_left  = coord(row + 1, col - 1)
            tileNeighbors.left         = coord(row    , col - 1)
        else:
            tileNeighbors.top_left     = coord(row - 1, col    )
            tileNeighbors.top_right    = coord(row - 1, col + 1)
            tileNeighbors.right        = coord(row    , col + 1)
            tileNeighbors.bottom_right = coord(row + 1, col + 1)
            tileNeighbors.bottom_left  = coord(row + 1, col    )
            tileNeighbors.left         = coord(row    , col - 1)

        lNorthTileNeighborsDict[tileCoord] = tileNeighbors

        if tileCoord in lNorthTeamsStartCoords.values():
            for key, value in lNorthTeamsStartCoords.items():
                if(value == tileCoord and lNorthTeamWeights[key] > 0):
                    control = key
        else:
            control = tile.attrib.get('control')

        lNorthTileControlDict[tileCoord] = control


    BuildMapForGroup(lNorthTileControlDict, lNorthTileNeighborsDict, lNorthTeamWeights)

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