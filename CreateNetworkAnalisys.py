import arcpy
from arcpy import env
import os


arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"
i=0
max_zonas=5


for row  in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", ["UBIGEO","ZONA","CODCCPP"]):

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"
    arcpy.Buffer_analysis("D:/ShapesPruebasSegmentacionUrbana/Zones/"+desc, "D:/ShapesPruebasSegmentacionUrbana/BufferZonas/"+desc, '0.5 METERS')


    arcpy.PolygonToLine_management("D:/ShapesPruebasSegmentacionUrbana/BufferZonas/" + desc,
                                   "D:/ShapesPruebasSegmentacionUrbana/BufferZonasLine/" + desc,
                                   "IGNORE_NEIGHBORS")





    i=i+1
    if i>max_zonas:
        break