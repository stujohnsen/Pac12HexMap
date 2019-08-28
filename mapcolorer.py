import time, json
# import cairosvg
import xml.etree.ElementTree as ET

if __name__ == "__main__":

    inStartTilesFile = open('starttiles.json', 'r')
    inStartCoordsJson = inStartTilesFile.read()
    lStartCoordsDict = json.loads(inStartCoordsJson)
    Cal        = lStartCoordsDict['North']['Cal']
    Oregon     = lStartCoordsDict['North']['Oregon']
    OSU        = lStartCoordsDict['North']['OSU']
    Stanford   = lStartCoordsDict['North']['Stanford']
    Washington = lStartCoordsDict['North']['Washington']
    WSU        = lStartCoordsDict['North']['WSU']
    Arizona    = lStartCoordsDict['South']['Arizona']
    ASU        = lStartCoordsDict['South']['ASU']
    Colorado   = lStartCoordsDict['South']['Colorado']
    UCLA       = lStartCoordsDict['South']['UCLA']
    USC        = lStartCoordsDict['South']['USC']
    Utah       = lStartCoordsDict['South']['Utah']
    
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    ET.register_namespace('xmls:xlink', "http://www.w3.org/1999/xlink")


    tree = ET.parse('JS Basemap.svg')
    root = tree.getroot()

    NorthGroup = tree.findall(".//{http://www.w3.org/2000/svg}g[@id='North']//")
    SouthGroup = tree.findall(".//{http://www.w3.org/2000/svg}g[@id='South']//")

    for tile in NorthGroup:
        row = int(tile.attrib.get('row'))
        col = int(tile.attrib.get('col'))

        if   (row == Cal['row']) and (col == Cal['col']) :
            tile.set('control', 'Cal')
        elif (row == Oregon['row']) and (col == Oregon['col']) :
            tile.set('control', 'Oregon')
        elif (row == OSU['row']) and (col == OSU['col']) :
            tile.set('control', 'OSU')
        elif (row == Stanford['row']) and (col == Stanford['col']) :
            tile.set('control', 'Stanford')
        elif (row == Washington['row']) and (col == Washington['col']) :
            tile.set('control', 'Washington')
        elif (row == WSU['row']) and (col == WSU['col']) :
            tile.set('control', 'WSU')

    SouthGroupTemp = dict();

    for tile in SouthGroup:
        row = int(tile.attrib.get('row'))
        col = int(tile.attrib.get('col'))
        XCoord = int(tile.attrib.get('YCoord'))
        YCoord = int(tile.attrib.get('XCoord'))
        control = int(tile.attrib.get('control'))

        if   (row == Arizona['row']) and (col == Arizona['col']) :
            tile.set('control', 'Arizona')
        elif (row == ASU['row']) and (col == ASU['col']) :
            tile.set('control', 'ASU')
        elif (row == Colorado['row']) and (col == Colorado['col']) :
            tile.set('control', 'Colorado')
        elif (row == UCLA['row']) and (col == UCLA['col']) :
            tile.set('control', 'UCLA')
        elif (row == USC['row']) and (col == USC['col']) :
            tile.set('control', 'USC')
        elif (row == Utah['row']) and (col == Utah['col']) :
            tile.set('control', 'Utah')

        SouthGroupTemp[row][col][]

    
tree.write('output_test.svg')

# cairosvg.svg2png(url="giftest/svg/output_michigan.svg", write_to="giftest/png/output_michigan.png")


# svgoutputpath = "giftest/svg/output_" + team_to_write.lower() + ".svg"
# pngoutputpath = "giftest/png/output_" + team_to_write.lower() + ".png"

# tree.write(svgoutputpath)