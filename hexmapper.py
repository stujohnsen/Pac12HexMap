import time

if __name__ == "__main__":
    inCoordFile = open("coordmap", "r")
    coordList = list()
    index = 0
    y = 0
    maxX = 0
    for line in inCoordFile:
        x=0
        for loc in line:
            if(loc == 'x' or loc == 'X'):
                coordList.append((x,y,index))
                x += 1
                index += 1
            elif (loc != ' '):
                x += 1
            elif (loc == ' '):
                continue
            
        if x > maxX: maxX = x
        y += 1

    hexGrid = list()

    minX = 0
    minY = 0
    maxY = y

    for coord in coordList:
        coordX = coord[0] * 43.3
        coordY = coord[1] * 37.5
        index  = coord[2]

        if((coord[1] % 2) == 1):
            coordX += 21.65

        if minX > (coordX - 21.65):
            minX = (coordX - 21.65)
            round(minX, 3)
        if maxX < (coordX + 21.65):
            maxX = (coordX + 21.65)
            round(maxX, 3)
        if minY > (coordY - 25):
            minY = (coordY - 25)
            round(minY, 3)
        if maxY < (coordY + 25):
            maxY = (coordY + 25)
            round(maxY, 3)  

        pointA = (round(coordX       , 3), round(coordY - 25, 3))
        pointB = (round(coordX + 21.65, 3), round(coordY - 12.5, 3))
        pointC = (round(coordX + 21.65, 3), round(coordY + 12.5, 3))
        pointD = (round(coordX       , 3), round(coordY + 25, 3))
        pointE = (round(coordX - 21.65, 3), round(coordY + 12.5, 3))
        pointF = (round(coordX - 21.65, 3), round(coordY - 12.5, 3))

        hexString = \
            '<polygon control="base" ' + \
            'row="' + repr(coord[1]) +'" col="' + repr(coord[0]) + '" ' +\
            'XCoord="' + repr(round(coordX, 3)) + '" YCoord="' + repr(round(coordY, 3)) + '" index="' + repr(index) + '" ' +\
            'points="' + \
            repr(pointA[0]) + ',' + repr(pointA[1]) + ' ' + \
            repr(pointB[0]) + ',' + repr(pointB[1]) + ' ' + \
            repr(pointC[0]) + ',' + repr(pointC[1]) + ' ' + \
            repr(pointD[0]) + ',' + repr(pointD[1]) + ' ' + \
            repr(pointE[0]) + ',' + repr(pointE[1]) + ' ' + \
            repr(pointF[0]) + ',' + repr(pointF[1]) + ' ' + \
            '"></polygon>'

        hexGrid.append(hexString)

    strokeWidth = 5

    width = repr(round(abs(minX)+abs(maxX) + (3 * strokeWidth),3))
    height = repr(round(abs(minY)+abs(maxY) + (3 * strokeWidth),3))

    viewBox = '"' + repr(minX - (strokeWidth)) + ' ' + repr(minY - (strokeWidth)) + ' ' + width + ' ' + height +'"'

    svgFileContents = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" ' +\
        'width="' + width + '" height="' + height + '" viewBox=' + viewBox + '>\n'

    svgFileContents += \
        '\t<defs> \n' + \
            '\t\t<style>\n' + \
            '\t\t\tpolygon {stroke: #000; stroke-width: ' + repr(strokeWidth) + 'px;}\n' + \
            '\t\t\tpolygon[control="base"]             {fill:grey}\n' + \
            '\t\t\tpolygon[control="baseborder"]       {fill:black}\n' + \
            '\t\t\tpolygon[control="Arizona"]          {fill:#CC0033}\n' + \
            '\t\t\tpolygon[control="ArizonaBorder"]    {fill:#003366}\n' + \
            '\t\t\tpolygon[control="ASU"]              {fill:#FFC425}\n' + \
            '\t\t\tpolygon[control="ASUBorder"]        {fill:#A40046}\n' + \
            '\t\t\tpolygon[control="Cal"]              {fill:#041E42}\n' + \
            '\t\t\tpolygon[control="CalBorder"]        {fill:#FFC72C}\n' + \
            '\t\t\tpolygon[control="Colorado"]         {fill:#CFB87C}\n' + \
            '\t\t\tpolygon[control="ColoradoBorder"]   {fill:#565A5C}\n' + \
            '\t\t\tpolygon[control="Oregon"]           {fill:#124734}\n' + \
            '\t\t\tpolygon[control="OregonBorder"]     {fill:#FEE123}\n' + \
            '\t\t\tpolygon[control="OSU"]              {fill:#D85A1A}\n' + \
            '\t\t\tpolygon[control="OSUBorder"]        {fill:#685040}\n' + \
            '\t\t\tpolygon[control="Stanford"]         {fill:#990000}\n' + \
            '\t\t\tpolygon[control="StanfordBorder"]   {fill:#175E54}\n' + \
            '\t\t\tpolygon[control="UCLA"]             {fill:#3284BF}\n' + \
            '\t\t\tpolygon[control="UCLABorder"]       {fill:#FFE800}\n' + \
            '\t\t\tpolygon[control="USC"]              {fill:#991B1E}\n' + \
            '\t\t\tpolygon[control="USCBorder"]        {fill:#FFCC00}\n' + \
            '\t\t\tpolygon[control="Utah"]             {fill:#CC0000}\n' + \
            '\t\t\tpolygon[control="UtahBorder"]       {fill:#808080}\n' + \
            '\t\t\tpolygon[control="Washington"]       {fill:#33006F}\n' + \
            '\t\t\tpolygon[control="WashingtonBorder"] {fill:#E8D3A2}\n' + \
            '\t\t\tpolygon[control="WSU"]              {fill:#981E32}\n' + \
            '\t\t\tpolygon[control="WSUBorder"]        {fill:#53565A}\n' + \
            '\t</style>\n' + \
        '\t</defs>\n'

    for hex in hexGrid:
        svgFileContents += '\t' + hex + '\n'

    svgFileContents += "</svg>\n"
    svgFileName = 'hexMap' + time.strftime("%Y%m%d-%H%M%S") + '.svg'
    outSVGFile = open(svgFileName, "w")
    outSVGFile.write(svgFileContents)

