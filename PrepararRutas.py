import arcpy
#arcpy.env.workspace="Database Connections"


def ObtenerPuntosMasNorOeste():
    arcpy.env.workspace = "D:/ShapesPruebasSegmentacionUrbana/"
    fc1=r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES_MZS_SORT.shp"
    fc2=r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"

    with arcpy.arcpy.da.SearchCursor(fc2, ['IDMANZANA']) as cursor2:
        for row2 in cursor2:
            where_expression = " IDMANZANA=\'" + str(row2[0])+"\'"
            contador=0
            with arcpy.arcpy.da.UpdateCursor(fc1, ['FID'],where_expression) as cursor1:
                for row1 in cursor1:
                    if(contador>0):
                        cursor1.deleteRow()
                    contador=contador+1

def ReordenarVerticesManzanasMasNorOeste():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES_MZS_SORT.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES_MZS_SORT.shp")

    fc1=r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES_MZS.shp"
    fc2= r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES_MZS_SORT.shp"

#    arcpy.FeatureVerticesToPoints_management(fc1,r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/Vertices_MZS.shp","ALL")
    sort_fields = [["IDMANZANA", "ASCENDING"],["Shape", "ASCENDING"]]

    arcpy.Sort_management(fc1, fc2, sort_fields)

def ObtenerVerticesManzana():
    #fc1=r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO_VERTICES_SORT.shp"

    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES_MZS.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES_MZS.shp")

    arcpy.env.workspace = "D:/ShapesPruebasSegmentacionUrbana/"
    fc1=r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"
    arcpy.FeatureVerticesToPoints_management(fc1,
                                             r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VERTICES_MZS.shp",
                                             "ALL")



#ObtenerVerticesManzana()
#ReordenarVerticesManzanasMasNorOeste()
#ObtenerPuntosMasNorOeste()

def ReordenarViviendas():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    fc3 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"



    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO_SORT.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO_SORT.shp")


    fc1 = r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VIVIENDAS_U_TRABAJO.shp"
    fc2 = r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_VIVIENDAS_U_TRABAJO_SORT.shp"

    sort_fields = [["UBIGEO","ASCENDING"],["ZONA","ASCENDING"],["MANZANA", "ASCENDING"],["Shape", "ASCENDING"]]
    arcpy.Sort_management(fc1, fc2, sort_fields)

    arcpy.MakeFeatureLayer_management(fc2, "viviendas_temporal")

    with arcpy.arcpy.da.SearchCursor(fc3, ['UBIGEO','ZONA','MANZANA']) as cursor3:
        for row3 in cursor3:

            where_expression = " UBIGEO=\'" + str(row3[0]) + "\'  AND  ZONA=\'" + str(row3[1]) + "\' AND MANZANA=\'"+str(row3[2])
            arcpy.arcpy.SelectLayerByAttribute_management("viviendas_temporal",where_expression)

            #contador = 0
            orden=1
            with arcpy.arcpy.da.UpdateCursor("viviendas_temporal", ['OR_VIV_AEU'], where_expression) as cursor1:
                for row1 in cursor1:
                    row1[0]=orden
                    orden = orden + 1
                    cursor1.updateRow(row1)

def CrearPuntosDeRuta():
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"


    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_RUTA.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_RUTA.shp")

    desc="TB_PUNTOS_RUTA.shp"

    spatial_reference = arcpy.Describe(r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_MZS_INICIO_FIN.shp").spatialReference


    arcpy.CreateFeatureclass_management(r"D:/ShapesPruebasSegmentacionUrbana/PuntosCorte",
                                        desc,
                                        "POINT",
                                        "",
                                        "",
                                        "DISABLED",
                                        spatial_reference)

    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas")
    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp",
                                      "viviendas")
    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_CORTES.shp",
                                      "viviendas_cortes")
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", "aer_manzana")

    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", "zonas")
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_MZS_INICIO_FIN_ORDENADO.shp", "puntos_inicio_fin")

    inFeatures = "D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_RUTA.shp"
    fieldName1 = "IDMANZANA"
    fieldName2 = "AEU"


    # Add fields
    arcpy.AddField_management(inFeatures, fieldName1, "TEXT")
    arcpy.AddField_management(inFeatures, fieldName2, "TEXT")




    cursor_insert = arcpy.da.InsertCursor("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_RUTA.shp", ["SHAPE@"])
    cursor_insert2 = arcpy.da.InsertCursor("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_RUTA.shp",
                                          ["SHAPE@"])
    j = 0
#    for row11 in arcpy.da.SearchCursor("puntos_inicio_fin",
#                                       ["SHAPE@","UBIGEO","ZONA","MANZANA"] ):
#        cursor_insert.insertRow([row11[0]])
#        where_expresion="UBIGEO=\'" + str(row11[1]) + "\' AND ZONA=\'" + str(row11[2]) + "\' AND MANZANA= \'"+str(row11[3])+"\' AND ID_REG_OR=1"
#
#
#        for row22 in arcpy.da.SearchCursor("viviendas",
#                                            ["SHAPE@"],where_expresion):
#             cursor_insert2.insertRow([row22[0]])


    for row3 in arcpy.da.SearchCursor("manzanas",["UBIGEO", "ZONA","IDMANZANA"]):
        where_expression1= "UBIGEO=\'" + str(row3[0]) + "\' AND ZONA=\'" + str(row3[1]) + "\' AND IDMANZANA= \'"+str(row3[2])+"\'"

        cant_aeus=0

        for row1 in arcpy.da.SearchCursor("aer_manzana",["UBIGEO"],where_expression1):
            cant_aeus=cant_aeus+1

        if cant_aeus==1:
           where_expression = "UBIGEO=\'" + str(row3[0]) + "\' AND ZONA=\'" + str(row3[1]) + "\' AND MANZANA= \'"+str(row3[2])[11:]+"\'"


           j=0
           for row11 in arcpy.da.SearchCursor("puntos_inicio_fin",
                                                      ["SHAPE@"],where_expression):

               cursor_insert.insertRow([row11[0],row11])
               where_expresion3 = "UBIGEO=\'" + str(row11[1]) + "\' AND ZONA=\'" + str(
                   row11[2]) + "\' AND MANZANA= \'" + str(row11[3]) + "\' AND ID_REG_OR=1"
               for row22 in arcpy.da.SearchCursor(
                                     "viviendas",
                                     ["SHAPE@"],where_expresion3):
                   row22


 #      #where_expression
 #          aeu=0
 #          for rowx in arcpy.da.SearchCursor("aer_manzana", ["UBIGEO","AEU"], where_expression1):
 #              aeu=int(rowx[0])

 #          puntos_inicio_fin=[]

 #          puntos_medios=[]

 #          puntos_ruta=[]




 #          where_expression2="UBIGEO=\'" + str(row3[0]) + "\' AND ZONA=\'" + str(row3[1]) + "\' AND MANZANA= \'"+str(row3[2])[11:]+"\'"
 #          for row11 in arcpy.da.SearchCursor("puntos_inicio_fin",
 #                                           ["SHAPE@"],where_expression2):
 #              puntos_inicio_fin.append(row11)
 #              cursor_insert.insertRow(row11)
 #          where_expression3=where_expression2+ "  AND ID_REG_OR=1"
 #          for row22 in arcpy.da.SearchCursor(
 #                      "viviendas",
 #                      ["SHAPE@"],where_expression3):
 #              puntos_medios.append(row22)
 #              cursor_insert.insertRow(row11)
 #          puntos_ruta=[puntos_inicio_fin[0],puntos_medios[0],puntos_inicio_fin[1]]


 #          print puntos_ruta

            #fila=[]

 # #          for el in puntos_ruta:
  #              cursor_insert.insertRow(el)

#    cursor = arcpy.da.InsertCursor("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_RUTA.shp",["SHAPE@"])
#
#
#
#
#
#    for row in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/PuntosCorte/TB_PUNTOS_MZS_INICIO_FIN.shp",
#                                     ["SHAPE@"]):
#
#        cursor.insertRow(row)




def CrearRutas():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    #fc1 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"

    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas")
    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Rutas/TB_RUTAS_PREPARACION.shp",
                                      "rutas")
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", "aeu_manzana")





    if arcpy.Exists ("D:/ShapesPruebasSegmentacionUrbana/Rutas/TB_RUTAS.shp"):
        arcpy.Delete_management("D:/ShapesPruebasSegmentacionUrbana/Rutas/TB_RUTAS.shp")


    #fc2=r"D:/ShapesPruebasSegmentacionUrbana/Rutas/TB_RUTAS_PREPARACION.shp"



    lista_rutas=[]
    sort_fields = [["Shape", "ASCENDING"]]

    where_inicial = " UBIGEO=\'020601\' "
    with arcpy.arcpy.da.SearchCursor("manzanas", ['UBIGEO','ZONA','MANZANA'],where_inicial) as cursor3:
        for row3 in cursor3:

            fc2="D:/ShapesPruebasSegmentacionUrbana/Rutas/RutasPreparacion/Ruta"+str(row3[0])+str(row3[1])+str(row3[2])+".shp"
            where_expression = " UBIGEO=\'" + str(row3[0]) + "\'  AND  ZONA=\'" + str(row3[1]) + "\' AND MANZANA=\'"+str(row3[2])+"\' "
            where_expression2 =" IDMANZANA=\'"+str(row3[0])+str(row3[1])+str(row3[2])+"\'"

            print where_expression

            arcpy.arcpy.SelectLayerByAttribute_management("rutas","NEW_SELECTION",where_expression)
            arcpy.Sort_management("rutas", fc2, sort_fields,"PEANO")
            lista_rutas.append(fc2)

            arcpy.arcpy.SelectLayerByAttribute_management("aeu_manzana", "NEW_SELECTION", where_expression2)

            fid=0


            with arcpy.da.SearchCursor("aeu_manzana", ['AEU']) as cursorx:
                for rowx in cursorx:
                    aeu=rowx[0]
                    where_expressionxx="FID="+str(fid)
                    with arcpy.da.UpdateCursor(fc2, ['AEU'],where_expressionxx) as cursorxx:
                        for rowxx in cursorxx:
                            rowxx[0]=aeu
                            #cursor1.updateRow(row1)
                            cursorxx.updateRow(rowxx)

                    fid=fid+1

    #del cursor3

    arcpy.Merge_management(lista_rutas, "D:/ShapesPruebasSegmentacionUrbana/Rutas/TB_RUTAS.shp")


    for el in lista_rutas:
        arcpy.Delete_management(el)




def ActualizarRutasAEUSinViviendas():

    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    #fc1 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"

    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas")

    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Rutas/TB_RUTAS.shp",
                                      "rutas")

    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", "aeu_manzana")

    where_inicial= " VIV_MZ=0 "

    aeu=0
    with arcpy.arcpy.da.SearchCursor("manzanas", ['UBIGEO','ZONA','MANZANA'],where_inicial) as cursor3:
        for row3 in cursor3:

            where_expression = " UBIGEO=\'" + str(row3[0]) + "\'  AND  ZONA=\'" + str(
                row3[1]) + "\' AND MANZANA=\'" + str(row3[2]) + "\' "


            where_expression2 = " IDMANZANA=\'" + str(row3[0])+(row3[1]) + str(row3[2]) + "\' "

            arcpy.SelectLayerByAttribute_management("rutas", "NEW_SELECTION", where_expression)
            arcpy.SelectLayerByAttribute_management("aeu_manzana", "NEW_SELECTION", where_expression2)

            #print where_expression

            with arcpy.arcpy.da.SearchCursor("aeu_manzana", ['AEU']) as cursor4:
                for row4 in cursor4:
                    aeu=int(row4[0])
                    #print aeu
            del cursor4

            with arcpy.arcpy.da.UpdateCursor("rutas", ['AEU']) as cursor5:
                for row5 in cursor5:
                    row5[0]=aeu
                    cursor5.updateRow(row5)

            del cursor5
        del cursor3
            #arcpy.SelectLayerByAttribute_management("rutas", "NEW_SELECTION", where_expression)


#CrearRutas()
##SE ACTUALIZA DESPUES DE QUE?

####SE ACTUALIZA DESPUES

######porque se debe actualizar debido al punto adyacente



def ActualizarRutasCantidadViviendas():
    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    #fc1 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"

    #arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas")
    TB_RUTAS="D:/ShapesPruebasSegmentacionUrbana/Mapas/TB_RUTAS.shp"

    if arcpy.Exists (TB_RUTAS):
        arcpy.Delete_management(TB_RUTAS)

    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp",
                                  TB_RUTAS)


    arcpy.MakeFeatureLayer_management(TB_RUTAS,
                                      "rutas2")

    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", "aeu_manzana2")

    with arcpy.da.UpdateCursor("rutas2", ['UBIGEO','ZONA','AEU_FINAL','VIV_AEU']) as cursor3:
        for row3 in cursor3:

            where_expression = " UBIGEO=\'" + str(row3[0]) + "\'  AND  ZONA=\'" + str(
                row3[1]) + "\' AND AEU_FINAL=" + str(row3[2])

            cant_viv_aeu=0

            arcpy.SelectLayerByAttribute_management("aeu_manzana2", "NEW_SELECTION", where_expression)

            with arcpy.arcpy.da.SearchCursor("aeu_manzana2", ['AEU_FINAL','VIV_AEU']) as cursor4:
                for row4 in cursor4:
                    cant_viv_aeu =cant_viv_aeu+int(row4[1])
                    #print cant_viv_aeu

            row3[3]=cant_viv_aeu
            cursor3.updateRow(row3)

#ActualizarRutasCantidadViviendas()
#def ActualizarRutasSegundaPasada():



def CrearCapaMapas():

    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    #fc1 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"

    #arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas")


    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp",
                                      "tb_mzs")

    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", "mzs_aeu")

    lista=[]
    #print where_x
    with arcpy.da.SearchCursor("mzs_aeu",['IDMANZANA','AEU']) as cursor5:
        for row5 in cursor5:
            where_x = ' "IDMANZANA"=\'' + str(row5[0]) + '\' '
            arcpy.SelectLayerByAttribute_management("tb_mzs", "NEW_SELECTION", where_x)

            with arcpy.da.UpdateCursor("tb_mzs", ['AEU']) as cursor6:
                for row6 in cursor6:
                    row6[0]=int(row5[1])
                    f="D:/ShapesPruebasSegmentacionUrbana/Manzanas/ManzanasMapas/Shape"+str(row5[0])+str(row5[1])+".shp"
                    #arcpy.management.CopyFeatures("tb_mzs", f)
                    lista.append(f)



    arcpy.Merge_management (lista,"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_AEU.shp" )

    for el in lista:
        arcpy.Delete_management(el)


def ActualizarRutasViviendasMenoresIguales16():

    arcpy.env.workspace="D:/ShapesPruebasSegmentacionUrbana/"
    #fc1 = r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"
    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas")
    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/RutasTratamiento2/TB_RUTAS.shp",
                                      "rutas")
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", "aeu_manzana")
    where_inicial= " VIV_MZ<16 "
    aeu=0
    viv_aeu=0
    with arcpy.arcpy.da.SearchCursor("manzanas", ['UBIGEO','ZONA','MANZANA'],where_inicial) as cursor3:
        for row3 in cursor3:

            where_expression = " UBIGEO=\'" + str(row3[0]) + "\'  AND  ZONA=\'" + str(
                row3[1]) + "\' AND MANZANA=\'" + str(row3[2]) + "\' "


            where_expression2 = " IDMANZANA=\'" + str(row3[0])+(row3[1]) + str(row3[2]) + "\' "

            arcpy.SelectLayerByAttribute_management("rutas", "NEW_SELECTION", where_expression)
            arcpy.SelectLayerByAttribute_management("aeu_manzana", "NEW_SELECTION", where_expression2)

            #print where_expression

            with arcpy.arcpy.da.SearchCursor("aeu_manzana", ['AEU','VIV_AEU']) as cursor4:
                for row4 in cursor4:
                    aeu=int(row4[0])
                    viv_aeu=int(row4[1])
                    #print aeu
            del cursor4

            with arcpy.arcpy.da.UpdateCursor("rutas", ['AEU','VIV_AEU','flg','ID_RUTA','UBIGEO','ZONA','MANZANA']) as cursor5:
                for row5 in cursor5:
                    row5[0]=aeu
                    row5[1] = viv_aeu
                    row5[2]=1
                    row5[3]=str(row5[4])+str(row5[5])+str(row5[6])+str(aeu)
                    cursor5.updateRow(row5)

            del cursor5
        del cursor3
#ActualizarRutasViviendasMenoresIguales16()



def ActualizarRutasAEUSegundaPasada():
    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
    MZS_AEU= "D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/MZS_AEU.dbf"
    MZS_TRABAJO="D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_MZS_TRABAJO.shp"
    VIVIENDAS="D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_VIVIENDAS_U_TRABAJO.shp"
    RUTAS="D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_RUTAS.shp"
    SEGUNDA_PASADA = "D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_SEGUNDA_PASADA.shp"
    #arcpy.MakeTableView_management(MZS_AEU, "mzs_aeu")
    #arcpy.MakeFeatureLayer_management(MZS_TRABAJO,"mzs_trabajo")
    #arcpy.MakeFeatureLayer_management(VIVIENDAS,"viviendas")
    #arcpy.MakeFeatureLayer_management(RUTAS, "rutas")
    #arcpy.MakeFeatureLayer_management(SEGUNDA_PASADA, "rutas")
    #where_list = ["020601","021806","110204"]
  ## arcpy.AddField_management(MZS_AEU, "AEU_SP", "SHORT")
  # arcpy.AddField_management(MZS_TRABAJO, "AEU_SP", "SHORT")
  # arcpy.AddField_management(VIVIENDAS, "AEU_SP", "SHORT")
  # arcpy.AddField_management(RUTAS, "AEU_SP", "SHORT")


    with arcpy.da.SearchCursor(SEGUNDA_PASADA, ['UBIGEO', 'ZONA','AEU','AEU_1']) as cursor:
        for row in cursor:
            where=' UBIGEO=\''+str(row[0])+'\' AND ZONA=\''+str(row[1])+'\' AND AEU='+str(row[2])  # SE UBICA EL AEU DE LA MANZANA ESCOGIDA
            where_2=' UBIGEO=\''+str(row[0])+'\' AND ZONA=\''+str(row[1])+'\' AND AEU='+str(row[3])  ##SE UBICA EL AEU DEL SEGMENTO ESCOGIDO
            numero_aeu=int(row[3])
            where_viviendas = ' UBIGEO=\'' + str(row[0]) + '\' AND ZONA=\'' + str(row[1]) + '\' AND AEU=' + str(row[2]) +' AND (USOLOCAl=1 OR USOLOCAl=3) ' # SE UBICA EL AEU DE LA MANZANA ESCOGIDA

            with arcpy.da.UpdateCursor(MZS_AEU,['AEU'], where) as cursor8:
                for row8 in cursor8:
                    row8[0] = int(numero_aeu)
                    cursor8.updateRow(row8)

            del cursor8

            with arcpy.da.UpdateCursor(MZS_TRABAJO,['AEU'], where) as cursor9:
                for row9 in cursor9:
                    row9[0] = int(numero_aeu)
                    cursor9.updateRow(row9)
            del cursor9

            or_max=0

            with arcpy.da.SearchCursor(VIVIENDAS, ['AEU', 'OR_VIV_AEU'], where_2) as cursor7:
                for row7 in cursor7:
                    if or_max<int(row7[1]):
                        or_max=int(row7[1])

            del cursor7

            or_max=or_max+1

            with arcpy.da.UpdateCursor(VIVIENDAS,['AEU','OR_VIV_AEU'],where_viviendas ) as cursor10:
                for row10 in cursor10:
                    row10[0] = int(numero_aeu)
                    row10[1]=or_max
                    or_max=or_max+1
                    cursor10.updateRow(row10)
            del cursor10


            with arcpy.da.UpdateCursor(RUTAS,['AEU'], where) as cursor11:
                for row11 in cursor11:
                    row11[0] = int(numero_aeu)
                    cursor11.updateRow(row11)


            del cursor11

            with arcpy.da.UpdateCursor(RUTAS, ['flg'], where_2) as cursor12:
                for row12 in cursor12:
                    row12[0] = 1
                    cursor12.updateRow(row12)
            del cursor12

ActualizarRutasAEUSegundaPasada()














#ActualizarRutasCantidadViviendas()

#
#def ActualizarRutasAEUColas():
#
#    arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
#
#    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbana\\ShapesFinal\\MZS_AEU.dbf"
#    AEU_CANT_VIV = "D:\\ShapesPruebasSegmentacionUrbana\\SegundaPasada\\AEU_CANT_VIV"
#    LISTA_ADYACENCIA="D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/LISTA_ADYACENCIA_MANZANA.dbf"
#    RUTAS = "D:/ShapesPruebasSegmentacionUrbana/SegundaPasada/TB_RUTAS.shp"
#    if arcpy.Exists (AEU_CANT_VIV):
#        arcpy.Delete_management(AEU_CANT_VIV)
#
#    if arcpy.Exists (AEU_CANT_VIV):
#        arcpy.Delete_management(AEU_CANT_VIV)
#
#    arcpy.management.CopyFeatures("D:/ShapesPruebasSegmentacionUrbana/Rutas/TB_RUTAS.shp",
#                                  RUTAS)
#    arcpy.Statistics_analysis(MZS_AEU_dbf, AEU_CANT_VIV, [["VIV_AEU", "SUM"]], ["UBIGEO","ZONA","AEU"])
#
#    where=' "SUM_VIV_AEU"<=8'
#
#    arcpy.MakeTableView_management(MZS_AEU_dbf, 'mzs_aeu')
#    arcpy.MakeTableView_management(AEU_CANT_VIV, 'aeu_cant_viv',where)
#    arcpy.MakeTableView_management(LISTA_ADYACENCIA, 'lista_adyacencia')
#    arcpy.MakeFeatureLayer_management(RUTAS,"rutas")
#
#    with arcpy.da.SearchCursor("aeu_cant_viv",['UBIGEO','ZONA','AEU']) as cursor1:
#        for row1 in cursor1:
#            where1 = ' "UBIGEO"=\''+str(row1[0])+'\' AND "ZONA"=\''+str(row1[1])+'\' AND AEU=' +str(row1[2])
#            arcpy.SelectLayerByAttribute_management("mzs_aeu", "NEW_SELECTION", where1)
#
#
#            with arcpy.da.SearchCursor("mzs_aeu", ['IDMANZANA']) as cursor2:
#                for row2 in cursor2:
#                    idmanzana=row2[0]
#
#
#            BuscarManzanasAdyacentesMayores16V(idmanzana)
#
#
#
#def BuscarManzanasAdyacentesMayores16V(idmanzana):
#    list_ady=[]
#    where_expression=' "IDMANZANA"=\''+str(idmanzana)+'\' AND "TOT_VIV_AD">16'
#
#    for rowx in arcpy.da.SearchCursor('lista_adyacencia',["IDMANZ_ADY", "TOT_VIV_AD"], where_expression):
#        fila = [rowx[0],rowx[1]]
#        list_ady.append(list_ady)
#
#    return list_ady




    #Actualizando los AEU 'colas' que tengan menos de 8 viviendas








    





            #cursor4.updateRow(row4)

#            cursor_insercion.insertRow()
#
#
#
#
#
#
#
#
#            where_expression = " UBIGEO=\'" + str(row3[0]) + "\'  AND  ZONA=\'" + str(
#                row3[1]) + "\' AND AEU=" + str(row3[2])
#
#            cant_viv_aeu=0
#
#            arcpy.SelectLayerByAttribute_management("aeu_manzana2", "NEW_SELECTION", where_expression)
#
#            with arcpy.arcpy.da.SearchCursor("aeu_manzana2", ['AEU','VIV_AEU']) as cursor4:
#                for row4 in cursor4:
#                    cant_viv_aeu =cant_viv_aeu+int(row4[1])
#                    #print cant_viv_aeu
#
#            row3[3]=cant_viv_aeu
#            cursor3.updateRow(row3)
#
#
#ActualizarRutasAEUSinViviendas()
#ActualizarRutasCantidadViviendas().

#CrearCapaMapas()



