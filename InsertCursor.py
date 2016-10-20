
import arcpy
import numpy as np

arcpy.env.workspace = r"D:/ArcGisShapesPruebas/ShapesFinal/"


cursor= arcpy.da.InsertCursor("D:/ArcGisShapesPruebas/ShapesFinal/adyancencia.shp")

for row in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/ShapesFinal/Shape07010100100.shp"  , ["SHAPE",'FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1']):
    #rowArray = []
    #rowArray.append(row[0],row[1],row[2],row[4])
    print row
    cursor.insertRow(row)

    #cursor.insertRow(rowArray)
    #print row[0].centroid
