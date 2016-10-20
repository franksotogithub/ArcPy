import arcpy
from arcpy import env
from math import hypot




def CreateLineGeometry(desc):
    r = 0.00005
    env.overwriteOutput = True

    #arcpy.DeleteIdentical_management("C:/data/fireincidents.shp", ["ZONE", "INTENSITY"])

    #pnt = arcpy.Point(-88.236, 40.096)
    #pnt_geometry = arcpy.PointGeometry(pnt, spatial_reference)
    #spatial_reference = arcpy.Describe(r"D:/ArcGisShapesPruebas/VoronoiSplitLine/" + desc).spatialReference
    spatial_reference = arcpy.Describe(r"D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc).spatialReference
#    arcpy.CreateFeatureclass_management(r"D:/ArcGisShapesPruebas/WriteGeometry",
#                                        desc,
#                                        "POLYLINE",
#                                        "",
#                                        "",
#                                        "DISABLED",
#                                        spatial_reference)

    arcpy.CreateFeatureclass_management(r"D:/ShapesPruebasSegmentacionUrbana/WriteGeometry",
                                        desc,
                                        "POLYLINE",
                                        "",
                                        "",
                                        "DISABLED",
                                        spatial_reference)


    fieldName1 = "FirstX_2"
    fieldName2 = "FirstY_2"

    fieldName3 = "LastX_2"
    fieldName4 = "LastY_2"

    fieldPrecision = 20
    fieldScale = 11

    #desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2]) + ".shp"
    #inFeatures = "D:/ArcGisShapesPruebas/WriteGeometry/" + desc
    inFeatures = "D:/ShapesPruebasSegmentacionUrbana/WriteGeometry/" + desc

    # Add fields inicio
    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                              fieldPrecision, fieldScale)
    arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                              fieldPrecision, fieldScale)

    # Add fields fin
    arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
                              fieldPrecision, fieldScale)
    arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
                              fieldPrecision, fieldScale)



    #cursor= arcpy.da.InsertCursor(r"D:/ArcGisShapesPruebas/WriteGeometry/"+desc,["SHAPE@",'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2'])
    cursor = arcpy.da.InsertCursor(r"D:/ShapesPruebasSegmentacionUrbana/WriteGeometry/" + desc,
                                   ["SHAPE@", 'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2'])



    #for row in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/VoronoiSplitLine/"+desc  , ["SHAPE",'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2']):
    for row in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc,
                                         ["SHAPE", 'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2']):
        #rowArray = []
        #rowArray.append(row[0],row[1],row[2],row[4])

        array = arcpy.Array()


        x1=row[1]
        y1=row[2]
        x2=row[3]
        y2=row[4]
        dx=x1-x2
        dy=y1-y2
        linelen= hypot(dx,dy)
        x3=x2-r*dx/linelen
        y3 = y2 - r*dy/linelen

        #x3 = x2 - 0.1 * dx
        #y3 = y2 - 0.1 * dy

        pnt = arcpy.Point(x3,y3)

        xy=(x3,y3)

        array.add(arcpy.Point(x3,y3)) # agregamos el primer punto

        # cursor.insertRow([xy])

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


        #cursor.insertRow([arcpy.Polyline(array)])
        x4 = x1 + r * dx / linelen
        y4 = y1 + r * dy / linelen

        #x4 = x1 + 0.1 * dx
        #y4 = y1 + 0.1 * dy

        xy = (x4, y4)

        array.add(arcpy.Point(x4, y4)) #agregamos el segundo punto

        cursor.insertRow([arcpy.Polyline(array),x1,y1,x2,y2])# construimos la linea y lo insertamos
        #cursor.insertRow([xy])

        #print x2
        #print y2
        del array

    del cursor




#env.workspace = r"D:/ArcGisShapesPruebas"
# desc="Shape15013300200.shp"
#voronoi="Shape15013300200.shp"


#CreateLineGeometry(voronoi)