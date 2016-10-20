import arcpy
from arcpy import env
from math import hypot

env.overwriteOutput = True

#arcpy.DeleteIdentical_management("C:/data/fireincidents.shp", ["ZONE", "INTENSITY"])


env.workspace = r"D:/ArcGisShapesPruebas/WriteGeometry"

#desc="Shape07010100100.shp"
desc="Shape15013300200.shp"
spatial_reference =arcpy.Describe(r"D:/ArcGisShapesPruebas/WriteGeometry/"+desc).spatialReference

#pnt = arcpy.Point(-88.236, 40.096)
#pnt_geometry = arcpy.PointGeometry(pnt, spatial_reference)





arcpy.CreateFeatureclass_management(r"D:/ArcGisShapesPruebas/WriteGeometry",
                                    "puntos2.shp",
                                    "POINT",
                                    "",
                                    "",
                                    "DISABLED",
                                    spatial_reference)






cursor= arcpy.da.InsertCursor(r"D:/ArcGisShapesPruebas/WriteGeometry/puntos2.shp",["SHAPE@XY"])

r=0.0005
for row in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/WriteGeometry/Shape15013300200.shp"  , ["SHAPE",'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2']):
    #rowArray = []
    #rowArray.append(row[0],row[1],row[2],row[4])


    #array = arcpy.Array()

    x1=row[1]
    y1=row[2]
    x2=row[3]
    y2=row[4]
    dx=x1-x2
    dy=y1-y2
    linelen= hypot(dx,dy)
    x3=x2-r*dx/linelen
    y3 = y2 - r*dy/linelen
    pnt = arcpy.Point(x3,y3)
    xy=(x3,y3)



    #pnt_geometry=arcpy.PointGeometry(pnt, spatial_reference)
    #array.add(arcpy.Point(pnt_geometry))
    #pnt = arcpy.Point(x2, y2)
    #pnt_geometry = arcpy.PointGeometry(pnt, spatial_reference)
    #array.add(arcpy.Point(pnt_geometry))
    #row3[0]=arcpy.Polyline(array,spatial_reference)
    #x4=x1-dx/linelen*3
    #y4 = y1 - dy / linelen * 3
    #print "nuevo x: " +str(x3)
    #print "nuevo y: " + str(y3)
    cursor.insertRow([xy])
    x4 = x1 + r * dx / linelen
    y4 = y1 + r * dy / linelen

    xy = (x4, y4)
    cursor.insertRow([xy])

    print x2
    print y2
