import arcpy
import numpy as np



num_max_zonas=4
arcpy.env.workspace="Database Connections"
if arcpy.Exists ("Prueba6.sde")==False:

    arcpy.CreateDatabaseConnection_management("Database Connections",
                                          "Prueba6.sde",
                                          "SQL_SERVER",
                                          "192.168.200.250",
                                          "DATABASE_AUTH",
                                          "sde",
                                          "$deDEs4Rr0lLo",
                                          "#",
                                          "sprueba",
                                          "#",
                                          "#",
                                          "#",
                                          "#")


#arcpy.ListUsers(conection_sde)

#print arcpy.ListFeatureClasses()

prueba = "Prueba6.sde"
desc= arcpy.Describe("Prueba6.sde")
print desc.name




arcpy.env.workspace = r"Database Connections/Prueba6.sde"

desc= arcpy.Describe("sprueba.DBO.base_urbana")

print desc.name

arcpy.env.workspace = r"Database Connections/Prueba6.sde/sprueba.DBO.base_urbana"

desc= arcpy.Describe("sprueba.DBO.zona_censal")

print desc.name



arcpy.FeatureClassToFeatureClass_conversion("sprueba.DBO.zona_censal", "D:/ArcGisShapesPruebas/", 'zona_censal.shp')

#sze crean los shapes para estos efectos se utiliza solo hasta el numer4o 10
i=1
for row  in arcpy.da.SearchCursor("sprueba.DBO.zona_censal", ["IDDIST","CODZONA","SUFZONA"]):
    print row[0] + " " + row[1]+" "+row[2]
    desc="Shape"+str(row[0])+""+str(row[1])+""+str(row[2])
    where_clause= ' "IDDIST"=%s AND "CODZONA"=%s AND "SUFZONA"=%s' % (row[0],row[1],row[2])


    arcpy.FeatureClassToFeatureClass_conversion("sprueba.DBO.manzana_censal", "D:/ArcGisShapesPruebas/Zones/", desc,where_clause)
    print i
    i=i+1
    if i==num_max_zonas:
        break



#Obtenemos los nombres de los shapes que se han creado y le sacamos su centroide
arcpy.env.workspace = r"D:/ArcGisShapesPrueba"

i=1

for row  in arcpy.da.SearchCursor("zona_censal", ["IDDIST","CODZONA","SUFZONA"]):

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"

#convertimos a puntos

    if arcpy.Exists("D:/ArcGisShapesPruebas/Points/"+desc):
        arcpy.Delete_management("D:/ArcGisShapesPruebas/Points/" + desc)
    else:
        arcpy.FeatureToPoint_management("D:/ArcGisShapesPruebas/Zones/"+desc, "D:/ArcGisShapesPruebas/Points/"+desc,
                                    "CENTROID")





#agregamos una fila z

    fc="D:/ArcGisShapesPruebas/Points/" + desc
    arcpy.AddField_management(fc, 'Z', "SHORT")
    arcpy.CalculateField_management(fc, 'Z', 1)


# convertimos a puntos 3d

    if arcpy.Exists("D:/ArcGisShapesPruebas/Points3D/" + desc):
        arcpy.Delete_management("D:/ArcGisShapesPruebas/Points3D/" + desc)
    else:
        arcpy.FeatureTo3DByAttribute_3d(fc, "D:/ArcGisShapesPruebas/Points3D/" + desc, 'Z')

#convertimos lod puntos 3d a Tin

    Tin="D:/ArcGisShapesPruebas/Tin/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])
    Shapefile="D:/ArcGisShapesPruebas/Points3D/" + desc

    if arcpy.Exists(Tin):
        arcpy.Delete_management(Tin)
    else:
        arcpy.CreateTin_3d(Tin, "", Shapefile, "DELAUNAY")

#Convertimos los TIN a EDGE

    Tin = "D:/ArcGisShapesPruebas/Tin/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])
    Shapefile = "D:/ArcGisShapesPruebas/Edge/" + desc

    if arcpy.Exists(Shapefile):
        arcpy.Delete_management(Shapefile)
    else:
        arcpy.TinEdge_3d(Tin, Shapefile, edge_type='DATA')

#Agremagamos columnas de inicio y fin

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2]) + ".shp"
    inFeatures = "D:/ArcGisShapesPruebas/Edge/" + desc

    fieldName1 = "FirstX_1"
    fieldName2 = "FirstY_1"

    fieldName3 = "LastX_1"
    fieldName4 = "LastY_1"

    fieldPrecision = 20
    fieldScale = 11

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

    # Calculate Points Firts
    arcpy.CalculateField_management(inFeatures, fieldName1,
                                    "!SHAPE.firstPoint.X!",
                                    "PYTHON_9.3")
    arcpy.CalculateField_management(inFeatures, fieldName2,
                                    "!SHAPE.firstPoint.Y!",
                                    "PYTHON_9.3")

    # Calculate Points Last
    arcpy.CalculateField_management(inFeatures, fieldName3,
                                    "!SHAPE.lastPoint.X!",
                                    "PYTHON_9.3")
    arcpy.CalculateField_management(inFeatures, fieldName4,
                                    "!SHAPE.lastPoint.Y!",
                                    "PYTHON_9.3")











#############
    #####################
    #################POLIGONOS DE VORONOI


# Creando poligonos de thiaseen  o voronoi

    arcpy.CreateThiessenPolygons_analysis("D:/ArcGisShapesPruebas/Points/"+desc,
                                          "D:/ArcGisShapesPruebas/VoronoiPolygon/"+desc,
                                          "ALL")
#pologonos de vonoi a polyline ignarando lados vecinos
    arcpy.PolygonToLine_management("D:/ArcGisShapesPruebas/VoronoiPolygon/" + desc,
                                  "D:/ArcGisShapesPruebas/VoronoiLine/" + desc,
                                  "IGNORE_NEIGHBORS")


#polyline  a split lines

    arcpy.SplitLine_management("D:/ArcGisShapesPruebas/VoronoiLine/" + desc,"D:/ArcGisShapesPruebas/VoronoiSplitLine/" + desc)

    fieldName1 = "FirstX_2"
    fieldName2 = "FirstY_2"

    fieldName3 = "LastX_2"
    fieldName4 = "LastY_2"

    fieldPrecision = 20
    fieldScale = 11

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2]) + ".shp"
    inFeatures = "D:/ArcGisShapesPruebas/VoronoiSplitLine/" + desc

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

    # Calculate Points Firts
    arcpy.CalculateField_management(inFeatures, fieldName1,
                                    "!SHAPE.firstPoint.X!",
                                    "PYTHON_9.3")
    arcpy.CalculateField_management(inFeatures, fieldName2,
                                    "!SHAPE.firstPoint.Y!",
                                    "PYTHON_9.3")

    # Calculate Points Last
    arcpy.CalculateField_management(inFeatures, fieldName3,
                                    "!SHAPE.lastPoint.X!",
                                    "PYTHON_9.3")
    arcpy.CalculateField_management(inFeatures, fieldName4,
                                    "!SHAPE.lastPoint.Y!",
                                    "PYTHON_9.3")




#obteniendo los puntos de interseccion
    arcpy.Intersect_analysis(["D:/ArcGisShapesPruebas/VoronoiSplitLine/" + desc, "D:/ArcGisShapesPruebas/Edge/" + desc],
                             "D:/ArcGisShapesPruebas/Intersections/" + desc, "", "", "point")




#calculando la ortagonalidad y depurando los puntos innecesarios


    fc = "D:/ArcGisShapesPruebas/Intersections/" + desc
    fields = ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', 'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2', 'FID']
    # a=np.array([2, 4, 6, 8])
    # b = np.array([2, 4, 6, 8])

    j=0
    with arcpy.arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            a1 = row[0] - row[2]  # ax
            a2 = row[1] - row[3]  # ay  a=(a1,a2)
            b1 = row[4] - row[6]  # bx
            b2 = row[5] - row[7]  # bx b =(b1,b2)

            a = np.array([a1, a2])
            b = np.array([b1, b2])

            producto_escalar = np.dot(a, b)  # a.b=a1*b1 + a2*b2
            coseno = abs(producto_escalar) / (np.linalg.norm(a) * np.linalg.norm(b))

            # print  str(row[8])+":"+str(coseno)



            if coseno >= 0.005:
                cursor.deleteRow()

            j = j + 1

        del cursor





    #Exportar los puntos a lineas de adyacencia



        # Set local variables
        input_table = "D:/ArcGisShapesPruebas/Intersections/" + desc
        out_lines = "D:/ArcGisShapesPruebas/ShapesFinal/" + desc

        # XY To Line
        arcpy.XYToLine_management(input_table, out_lines,'FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', "GEODESIC")




    #arcpy.PolygonToLine_management("D:/ArcGisShapesPruebas/VoronoiPolygon/" + desc,
     #                              "D:/ArcGisShapesPruebas/VoronoiSplitLine/" + desc,
     #                              "IGNORE_NEIGHBORS")






    arcpy.Delete_management("D:/ArcGisShapesPruebas/Points/" + desc)
    arcpy.Delete_management("D:/ArcGisShapesPruebas/Points3D/" + desc)
    arcpy.Delete_management(Tin)
    arcpy.Delete_management(Shapefile)
    arcpy.Delete_management("D:/ArcGisShapesPruebas/VoronoiPolygon/" + desc)
    arcpy.Delete_management("D:/ArcGisShapesPruebas/VoronoiLine/" + desc)
    #arcpy.Delete_management("D:/ArcGisShapesPruebas/VoronoiSplitLine/" + desc)


    i=i+1
    if i==num_max_zonas:
        break





    #arcpy.FeatureClassToFeatureClass_conversion("sprueba.DBO.distritos", "D:/ArcGisShapesZones/", "distritos_prueba2" ,' "IDDIST" = \'150132\' ')






    #if arcpy.Exists ("sprueba.DBO.departamentos_centroide")==False:
    #    arcpy.CreateFeatureclass_management(r"Database Connections/Prueba6.sde/sprueba.DBO.base_limites_nacionales",
     #                               "sprueba.DBO.departamentos_centroide",
     #                               "POINT",
      #                              "",
      #                              "",
      #                              "",
      #                              "")




#cursor= arcpy.da.InsertCursor("sprueba.DBO.departamentos_centroide",["SHAPE@"])

#for row in arcpy.da.SearchCursor("sprueba.DBO.departamentos", ["SHAPE@"]):
 #   rowArray = []
 #   rowArray.append(row[0].centroid)
 #   cursor.insertRow(rowArray)
 #   print row[0].centroid






















#arcpy.AddField_management("sprueba.DBO.departamentos","limites_buffer","TEXT","10")
#arcpy.Buffer_analysis("sprueba.DBO.departamentos","sprueba.DBO.departamentos_buffer",'10 miles')


#if arcpy.Exists ("sprueba.DBO.departamentos_centroide")==False:
#    arcpy.CreateFeatureclass_management(r"Database Connections/Prueba6.sde/sprueba.DBO.base_limites_nacionales",
#                                    "sprueba.DBO.departamentos_centroide",
#                                    "POINT",
#                                    "",
#                                    "",
#                                    "",
#                                    "")
#arcpy.AddField_management(outCentroids, 'ORIG_ID', 'LONG')




#cursor= arcpy.da.InsertCursor("sprueba.DBO.departamentos_centroide",["SHAPE@"])

#for row in arcpy.da.SearchCursor("sprueba.DBO.departamentos", ["SHAPE@"]):
#s    rowArray = []
#    rowArray.append(row[0].centroid)
#    cursor.insertRow(rowArray)
#    print row[0].centroid