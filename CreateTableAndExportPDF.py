import arcpy
mxd = arcpy.mapping.MapDocument(r"D:/ArcGisProgramas/prueba.mxd")

#Reference items in the map document
lyr = arcpy.mapping.ListLayers(mxd, "sprueba.DBO.departamentos")[0]
horzLine = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "horzLine")[0]
vertLine = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "vertLine")[0]
tableText = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TableText")[0]
#Get/set information about the table
numRows = int(arcpy.GetCount_management(lyr).getOutput(0))
rowHeight = 0.4
fieldNames = ["NOM_DPTO", "xCentroid", "yCentroid"]
numColumns = len(fieldNames)
colWidth = 3.0

#Build graphic table lines based on upper left coordinate
#  set the proper size of the original, parent line, then clone it and position appropriately
upperX = 1.0
upperY = 5.0

#Vertical lines
vertLine.elementPositionX = upperX
vertLine.elementPositionY = upperY
#vertLine.elementHeight =  (rowHeight * numRows) + rowHeight #extra line for column names
x = upperX


#for vert in range(1, numColumns+1):
#  x = x + colWidth
#  vert_clone = vertLine.clone("_clone")
#  vert_clone.elementPositionX = x

#Horizontal lines
horzLine.elementPositionX = upperX
horzLine.elementPositionY = upperY
horzLine.elementWidth = numColumns * colWidth

y = upperY - rowHeight
for horz in range(1, numRows +2 ):  #need to accommodate the extra line for field names
  temp_horz = horzLine.clone("_clone")
  temp_horz.elementPositionY = y
  y = y - rowHeight

#Place text column names
tableText.elementPositionX = upperX + 0.05 #slight offset
tableText.elementPositionY = upperY
tableText.text = fieldNames[0]
accumWidth = colWidth
for field in range(1, numColumns):
  newFieldTxt = tableText.clone("_clone")
  newFieldTxt.text = fieldNames[field]
  newFieldTxt.elementPositionX = newFieldTxt.elementPositionX + accumWidth
  accumWidth = accumWidth + colWidth

#Create text elements based on values from the table
table = arcpy.SearchCursor(lyr.dataSource)
y = upperY - rowHeight
for row in table:
  x = upperX + 0.05 #slight offset
  try:
    for field in fieldNames:
      newCellTxt = tableText.clone("_clone")
      newCellTxt.text = row.getValue(field)
      newCellTxt.elementPositionX = x
      newCellTxt.elementPositionY = y
      accumWidth = accumWidth + colWidth
      x = x + colWidth
    y = y - rowHeight
  except:
    print"Invalid value assignment"

#Export to PDF and delete cloned elements
arcpy.mapping.ExportToPDF(mxd, r"D:/ArcGISPDF/test.pdf")

for elm in arcpy.mapping.ListLayoutElements(mxd, wildcard="_clone"):
  elm.delete()
del mxd