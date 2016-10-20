# Name: CreateDatabase.py
# Description: Connects to a point in time in the geodatabase in
#              PostgreSQL using database authentication.

# Import system modules
import arcpy
import os




#datasets=arcpy.ListDatasets()


arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana/Zones/"


#arcpy.AddField_management(outCentroids, 'ORIG_ID', 'LONG')






for row in arcpy.da.SearchCursor("Shape020601001000001.shp", ["FID","SHAPE@X"]):

    print  "FID: " +str(row[0]) + "X:" +str(row[1])

    #print row[0].centroid







