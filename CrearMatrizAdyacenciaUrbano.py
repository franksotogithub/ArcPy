import arcpy
import numpy as np
import CreateLineGeometry as c
#import ImportarExportarSQL as sql
import EliminarAdyacencias
import SolucionInicial as s
import ConectionSQL as conx
import ImportarExportarSQL as ie



#conx.ActualizarCantViviendasMzs()
#conx.ActualizarTipoVivienda()

def CrearMatrizAdyacencia():
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"


    #num_max_zonas=5
    arcpy.env.workspace="Database Connections"
    if arcpy.Exists ("PruebaSegmentacion.sde")==False:

        arcpy.CreateDatabaseConnection_management("Database Connections",
                                              "PruebaSegmentacion.sde",
                                              "SQL_SERVER",
                                              "192.168.200.250",
                                              "DATABASE_AUTH",
                                              "sde",
                                              "$deDEs4Rr0lLo",
                                              "#",
                                              "CPV_SEGMENTACION",
                                              "#",
                                              "#",
                                              "#",
                                              "#")


    #arcpy.ListUsers(conection_sde)

    #print arcpy.ListFeatureClasses()

    prueba = "PruebaSegmentacion.sde"
    #desc= arcpy.Describe("PruebaSegmentacion.sde")
    #print desc.name


    arcpy.env.workspace = r"Database Connections/PruebaSegmentacion.sde"

    #desc= arcpy.Describe("CPV_SEGMENTACION.dbo.base_urbana")

    #print desc.name


    #arcpy.env.workspace = r"Database Connections/PruebaSegmentacion.sde/"

    #arcpy.Exists ("PruebaSegmentacion.sde")==False:
    if arcpy.Exists (r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.ADYACENCIA"):
        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.adyacencia")

    if arcpy.Exists (r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO"):
        arcpy.Delete_management("Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.sde.TB_MZS_TRABAJO")



    #arcpy.env.workspace = r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.dbo.base_urbana"

    #desc= arcpy.Describe("CPV_SEGMENTACION.dbo.zona_censal")

    #print desc.name

    where_list=["020601",
    "021806",
    "110204"]
    #where_expression=' "IDDIST"=%s AND "CODZONA"=%s ' % (where_list[0],where_list[1])
    m=0

    where_expression=""
    for x in where_list:
        if (m+1)==len(where_list):
            where_expression =where_expression+' "UBIGEO"=%s'%where_list[m]
        else:
            where_expression=where_expression+' "UBIGEO"=%s OR'%(where_list[m])
        #where_expression=' "UBIGEO"=%s OR "UBIGEO"=%s "UBIGEO"=%s or "UBIGEO"=%s or "UBIGEO"=%s or "UBIGEO"=%s or "UBIGEO"=%s or "UBIGEO"=%s or "UBIGEO"=%s' % (where_list[0],where_list[1],where_list[1])

        m=m+1
    #IDIST='150133'
    #CODZONA='002'



    print where_expression
    #arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.zona_censal", "D:/ShapesPruebasSegmentacionUrbana/", 'zona_censal.shp' ,' "IDDIST" = \'150133\' ')
    arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_ZONA_CENSAL", "D:/ShapesPruebasSegmentacionUrbana/Zones/", 'zona_censal.shp' ,where_expression)
    arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.TB_MZS", r"D:/ShapesPruebasSegmentacionUrbana/Manzanas", 'TB_MZS_TRABAJO.shp',where_expression )




    #crear el shape que  va a contener toda lainformacion


    #se crean los shapes para estos efectos se utiliza solo hasta el numer4o 10





    #Obtenemos los nombres de los shapes que se han creado y le sacamos su centroide
    #arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
    #arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"



    ############################AGREGAMOS EL CENTROIDE Y EL AREA DE CADA MANZANA##################
    inFeatures = "D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"
    fieldName1 = "xCentroid"
    fieldName2 = "yCentroid"
    fieldPrecision = 18
    fieldScale = 11
    fieldScale2 = 2
    #### Add fields

    arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                              fieldPrecision, fieldScale)
    arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                              fieldPrecision, fieldScale)

    # Calculate centroid

    fields=["SHAPE@X","SHAPE@Y","xCentroid","yCentroid"]

    with arcpy.da.UpdateCursor(inFeatures, fields) as cursorx:
        for row0 in cursorx:
            row0[2]=row0[0]
            row0[3] = row0[1]
            cursorx.updateRow(row0)


    arcpy.AddField_management(inFeatures, "AREA", "DOUBLE",fieldPrecision,fieldScale2)
    exp = "!SHAPE.AREA@METERS!"
    arcpy.CalculateField_management(inFeatures, "AREA", exp, "PYTHON_9.3")




    arcpy.AddField_management(inFeatures, "IDMANZANA", "TEXT")
    exp = "!UBIGEO!+!ZONA!+!MANZANA!"
    arcpy.CalculateField_management(inFeatures, "IDMANZANA", exp, "PYTHON_9.3")

    #arcpy.AddField_management(inFeatures, "AEU", "SHORT")

    #############CREAMOS LA MATRIZ DE ADYACENCIA

    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf")==False:
        arcpy.CreateTable_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/",
                                        "adyacencia.dbf")


      # arcpy.CreateFeatureclass_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/",
      #                                     "adyacencia.dbf",
      #                                     "POLYLINE",
      #                                     "",
      #                                     "",
      #                                     "ENABLED",
      #                                     "")
        #arcpy.CreateTable_management("C:/output", "habitatTemperatures.dbf", "vegtable.dbf")

        fieldName1 = "FirstX"
        fieldName2 = "FirstY"

        fieldName3 = "LastX"
        fieldName4 = "LastY"

        fieldPrecision = 18
        fieldScale = 11


        inFeatures = "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf"

        # Add fields inicio
        arcpy.AddField_management(inFeatures, fieldName1, "DOUBLE",
                                  fieldPrecision, fieldScale)
        arcpy.AddField_management(inFeatures, fieldName2, "DOUBLE",
                                  fieldPrecision, fieldScale)
        # Add fields inicio
        arcpy.AddField_management(inFeatures, fieldName3, "DOUBLE",
                                  fieldPrecision, fieldScale)
        arcpy.AddField_management(inFeatures, fieldName4, "DOUBLE",
                                  fieldPrecision, fieldScale)
    #
    #else:
    #    with arcpy.arcpy.da.UpdateCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf" ) as cursor:
    #          cursor.deleteRow()
    #
    #    del cursor


    num_max_zonas=5

    i=1
    for row in arcpy.da.SearchCursor(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", ["UBIGEO","ZONA","CODCCPP"]):
        print row[0] + " " + row[1]+" "+row[2]
        desc="Shape"+str(row[0])+""+str(row[1])+""+str(row[2])
        where_clause= ' "UBIGEO"=\'%s\' AND "ZONA"=\'%s\' AND "CODCCPP"=\'%s\' ' % (row[0],row[1],row[2])
        print where_clause


        arcpy.FeatureClassToFeatureClass_conversion("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "D:/ShapesPruebasSegmentacionUrbana/Zones/", desc,where_clause)

        #Feature="D:/ShapesPruebasSegmentacionUrbana/Zones/"+desc+".shp"
        #fieldName1 = "xCentroid"
        #fieldName2 = "yCentroid"
        #fieldName3 = "AREA"
        #fieldPrecision = 18
        #fieldScale = 11

        # Add fields

    #    arcpy.AddField_management(Feature, fieldName1, "DOUBLE",
    #                              fieldPrecision, fieldScale)
    #    arcpy.AddField_management(Feature, fieldName2, "DOUBLE",
    #                              fieldPrecision, fieldScale)
    #
    #    arcpy.AddField_management(Feature, fieldName3, "DOUBLE",
    #                              fieldPrecision, fieldScale)
    #    # Calculate centroid
    #
    #
    #    arcpy.CalculateField_management(Feature, fieldName1,
    #                                    "!SHAPE.CENTROID.X!",
    #                                    "PYTHON_9.3")
    #    arcpy.CalculateField_management(Feature, fieldName2,
    #                                "!SHAPE.CENTROID.Y!",
    #                                "PYTHON_9.3")
    #
    #
    #    arcpy.CalculateField_management(Feature, "AREA", "!SHAPE.AREA@METERS!", "PYTHON_9.3")


    # arcpy.AddField_management(inFeatures, "AREA", "DOUBLE")
    # exp = "!SHAPE.AREA@METERS!"
    # arcpy.CalculateField_management(inFeatures, "AREA", exp, "PYTHON_9.3")

        print i
        i=i+1

       # if i==num_max_zonas:
       #     break




    i=1

    for row  in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", ["UBIGEO","ZONA","CODCCPP"]):

        desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"

    #convertimos a puntos

        if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbana/Points/"+desc):
            arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Points/" + desc)
        else:
            arcpy.FeatureToPoint_management("D:/ShapesPruebasSegmentacionUrbana/Zones/"+desc, "D:/ShapesPruebasSegmentacionUrbana/Points/"+desc,
                                        "CENTROID")





    #agregamos una fila z

        fc="D:/ShapesPruebasSegmentacionUrbana/Points/" + desc
        arcpy.AddField_management(fc, 'Z', "SHORT")
        arcpy.CalculateField_management(fc, 'Z', 1)


    # convertimos a puntos 3d

        if arcpy.Exists("D:/ShapesPruebasSegmentacionUrbana/Points3D/" + desc):
            arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Points3D/" + desc)
        else:
            arcpy.FeatureTo3DByAttribute_3d(fc, "D:/ShapesPruebasSegmentacionUrbana/Points3D/" + desc, 'Z')

    #convertimos lod puntos 3d a Tin

        Tin="D:/ShapesPruebasSegmentacionUrbana/Tin/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])
        Shapefile="D:/ShapesPruebasSegmentacionUrbana/Points3D/" + desc


        arcpy.CreateTin_3d(Tin, "", Shapefile, "DELAUNAY")

    #Convertimos los TIN a EDGE

        Tin = "D:/ShapesPruebasSegmentacionUrbana/Tin/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])
        Shapefile = "D:/ShapesPruebasSegmentacionUrbana/Edge/" + desc


        arcpy.TinEdge_3d(Tin, Shapefile, edge_type='DATA')

    #Agremagamos columnas de inicio y fin

        desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2]) + ".shp"
        inFeatures = "D:/ShapesPruebasSegmentacionUrbana/Edge/" + desc

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

        arcpy.CreateThiessenPolygons_analysis("D:/ShapesPruebasSegmentacionUrbana/Points/"+desc,
                                              "D:/ShapesPruebasSegmentacionUrbana/VoronoiPolygon/"+desc,
                                              "ALL")
    #pologonos de vonoi a polyline ignorando lados vecinos
        arcpy.PolygonToLine_management("D:/ShapesPruebasSegmentacionUrbana/VoronoiPolygon/" + desc,
                                      "D:/ShapesPruebasSegmentacionUrbana/VoronoiLine/" + desc,
                                      "IGNORE_NEIGHBORS")




    #polyline  a split lines

        arcpy.SplitLine_management("D:/ShapesPruebasSegmentacionUrbana/VoronoiLine/" + desc,"D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc)



        fieldName1 = "FirstX_2"
        fieldName2 = "FirstY_2"

        fieldName3 = "LastX_2"
        fieldName4 = "LastY_2"

        fieldPrecision = 20
        fieldScale = 11

        desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2]) + ".shp"
        inFeatures = "D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc

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


    #Eliminando los registros identicos
        arcpy.DeleteIdentical_management(r"D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc, ["Shape"])

    #creando las lineas

        c.CreateLineGeometry(desc)

    #obteniendo los puntos de interseccion
        arcpy.Intersect_analysis(["D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc, "D:/ShapesPruebasSegmentacionUrbana/Edge/" + desc],
                                 "D:/ShapesPruebasSegmentacionUrbana/IntersectionsInitial/" + desc, "ALL", "", "point")

        arcpy.Intersect_analysis(["D:/ShapesPruebasSegmentacionUrbana/WriteGeometry/" + desc, "D:/ShapesPruebasSegmentacionUrbana/Edge/" + desc],
                                 "D:/ShapesPruebasSegmentacionUrbana/Intersections/" + desc, "ALL", "", "point")


    #depurando los puntos duplicados
        fc1 = "D:/ShapesPruebasSegmentacionUrbana/Edge/" + desc
        fields1 = ['FID']
        fc2 = "D:/ShapesPruebasSegmentacionUrbana/Intersections/" + desc
        fields2 = ['FID_Shap_1']

        fc3="D:/ShapesPruebasSegmentacionUrbana/IntersectionsInitial/" + desc
        fields3 = ['FID_Shap_1']


        with arcpy.arcpy.da.SearchCursor(fc1, fields1) as cursor1:

            # contador=0
            for row1 in cursor1:
                # print "ID:" + str(row1[0])
                contador = 0
                with arcpy.arcpy.da.UpdateCursor(fc3, fields3) as cursor2:

                    for row2 in cursor2:
                        if row1[0] == row2[0]:
                            contador = contador + 1
                            # print "contador:" + str(contador)
                        if contador>2:
                            cursor2.deleteRow()
                            contador =  contador - 1
                del cursor2

            #    if contador>2:

            #        with arcpy.arcpy.da.UpdateCursor(fc3, fields3) as cursor2:
            #            for row2 in cursor2:
            #                if row1[0] == row2[0]:
            #                    cursor2.deleteRow()

            #        del cursor2
                            #contador = 1

        del cursor1

        with arcpy.arcpy.da.SearchCursor(fc1, fields1) as cursor1:

            # contador=0
            for row1 in cursor1:
                #print "ID:" + str(row1[0])
                with arcpy.arcpy.da.UpdateCursor(fc2, fields2) as cursor2:
                    contador = 0
                    for row2 in cursor2:
                        if row1[0] == row2[0]:
                            contador = contador + 1
                            #print "contador:" + str(contador)
                        if contador>3:
                            cursor2.deleteRow()
                            contador = contador - 1
            #        if contador > 3:
                 #       with arcpy.arcpy.da.UpdateCursor(fc2, fields2) as cursor2:
                 #           for row2 in cursor2:
                 #               if row1[0] == row2[0]:
                 #                   cursor2.deleteRow()

           # #            del cursor2
        del cursor1

    #calculando la ortagonalidad y depurando los puntos innecesarios


        fc = "D:/ShapesPruebasSegmentacionUrbana/Intersections/" + desc
        fields = ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', 'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2']
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


    #    fc = "D:/ShapesPruebasSegmentacionUrbana/IntersectionsInitial/" + desc
    #    fields = ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', 'FirstX_2', 'FirstY_2', 'LastX_2', 'LastY_2']
    #    j=0
    #
    #    with arcpy.arcpy.da.UpdateCursor(fc, fields) as cursor:
    #        for row in cursor:
    #            a1 = row[0] - row[2]  # ax
    #            a2 = row[1] - row[3]  # ay  a=(a1,a2)
    #            b1 = row[4] - row[6]  # bx
    #            b2 = row[5] - row[7]  # bx b =(b1,b2)
    #
    #            a = np.array([a1, a2])
    #            b = np.array([b1, b2])
    #
    #            producto_escalar = np.dot(a, b)  # a.b=a1*b1 + a2*b2
    #            coseno = abs(producto_escalar) / (np.linalg.norm(a) * np.linalg.norm(b))
    #
    #            # print  str(row[8])+":"+str(coseno)
    #
    #
    #
    #            if coseno >= 0.005:
    #                cursor.deleteRow()
    #
    #            j = j + 1
    #
    #        del cursor

        #Exportar los puntos a lineas de adyacencia



            # Set local variables
        input_table = "D:/ShapesPruebasSegmentacionUrbana/Intersections/" + desc
        out_lines = "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/" + desc


            # XY To Line
        arcpy.XYToLine_management(input_table, out_lines,'FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', "GEODESIC")

        arcpy.DeleteIdentical_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/" + desc, ["Shape"])


        #input_table = "D:/ShapesPruebasSegmentacionUrbana/IntersectionsInitial/" + desc
        #out_lines = "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal2/" + desc

            # XY To Line
        #arcpy.XYToLine_management(input_table, out_lines,'FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1', "GEODESIC")
        #arcpy.DeleteIdentical_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal2/" + desc, ["Shape"])

        #arcpy.PolygonToLine_management("D:/ShapesPruebasSegmentacionUrbana/VoronoiPolygon/" + desc,
         #                              "D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc,
         #                              "IGNORE_NEIGHBORS")

        # exportando datos a la base de datos

        #out_lines = "D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/" + desc


        #insertamos las filas en el shape adyacencia
        adyacencias_x="D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/"+desc
        manzanas="D:/ShapesPruebasSegmentacionUrbana/Zones/" + desc

        EliminarAdyacencias.PorCantidadManzanasCruza(manzanas,adyacencias_x)

        cursor = arcpy.da.InsertCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf", ['FirstX', 'FirstY', 'LastX', 'LastY'])
        for row in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/" + desc, ['FirstX_1', 'FirstY_1', 'LastX_1', 'LastY_1']):
            #print row
            cursor.insertRow(row)
        del cursor






        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Points/" + desc)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Points3D/" + desc)
        arcpy.Delete_management(Tin)
        #arcpy.Delete_management(Shapefile)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/VoronoiPolygon/" + desc)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/VoronoiLine/" + desc)

        #arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/" + desc)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal2/" + desc)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/VoronoiSplitLine/" + desc)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Intersections/" + desc)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/IntersectionsInitial/" + desc)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Edge/" + desc)
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/WriteGeometry/" + desc)
        i=i+1
       # if i==num_max_zonas:
        #    break


    #arcpy.FeatureClassToGeodatabase_conversion(['D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf'],
    #                                                   'Database Connections/PruebaSegmentacion.sde/')
    arcpy.TableToTable_conversion('D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf', 'Database Connections/PruebaSegmentacion.sde/','adyacencia' )
    arcpy.FeatureClassToGeodatabase_conversion(['D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp'],
                                               'Database Connections/PruebaSegmentacion.sde/')


    arcpy.Delete_management('D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp')
    arcpy.Delete_management('D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf')

#sql.Exportar_TB_MZS_TRABAJO()
conx.InsertarAdyacencia()



#arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/adyacencia.dbf")
#arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp")


    #arcpy.FeatureClassToFeatureClass_conversion("CPV_SEGMENTACION.dbo.distritos", "D:/ArcGisShapesZones/", "distritos_prueba2" ,' "IDDIST" = \'150132\' ')






    #if arcpy.Exists ("CPV_SEGMENTACION.dbo.departamentos_centroide")==False:
    #    arcpy.CreateFeatureclass_management(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.dbo.base_limites_nacionales",
     #                               "CPV_SEGMENTACION.dbo.departamentos_centroide",
     #                               "POINT",
      #                              "",
      #                              "",
      #                              "",
      #                              "")




#cursor= arcpy.da.InsertCursor("CPV_SEGMENTACION.dbo.departamentos_centroide",["SHAPE@"])

#for row in arcpy.da.SearchCursor("CPV_SEGMENTACION.dbo.departamentos", ["SHAPE@"]):
 #   rowArray = []
 #   rowArray.append(row[0].centroid)
 #   cursor.insertRow(rowArray)
 #   print row[0].centroid






















#arcpy.AddField_management("CPV_SEGMENTACION.dbo.departamentos","limites_buffer","TEXT","10")
#arcpy.Buffer_analysis("CPV_SEGMENTACION.dbo.departamentos","CPV_SEGMENTACION.dbo.departamentos_buffer",'10 miles')


#if arcpy.Exists ("CPV_SEGMENTACION.dbo.departamentos_centroide")==False:
#    arcpy.CreateFeatureclass_management(r"Database Connections/PruebaSegmentacion.sde/CPV_SEGMENTACION.dbo.base_limites_nacionales",
#                                    "CPV_SEGMENTACION.dbo.departamentos_centroide",
#                                    "POINT",
#                                    "",
#                                    "",
#                                    "",
#                                    "")
#arcpy.AddField_management(outCentroids, 'ORIG_ID', 'LONG')




#cursor= arcpy.da.InsertCursor("CPV_SEGMENTACION.dbo.departamentos_centroide",["SHAPE@"])

#for row in arcpy.da.SearchCursor("CPV_SEGMENTACION.dbo.departamentos", ["SHAPE@"]):
#s    rowArray = []
#    rowArray.append(row[0].centroid)
#    cursor.insertRow(rowArray)
#    print row[0].centroid