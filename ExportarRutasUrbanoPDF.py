import arcpy

arcpy.env.overwriteOutput = True  #sirve para sobreescribir los elementos

arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"


i = 0
max_zonas = 2

for row in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                     ["UBIGEO", "ZONA"]):
    where_expression = "UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" +str(row[1])+ "\'"
    #"  AND CODCCPP=\'"+str(row[2])+"\'"
    #where_expression = "AER=\'" + str(i)+"\'"
#where_expression = " AER= '1' "
#arcpy.SelectLayerByAttribute_management("viviendas", "NEW_SELECTION")
#arcpy.SelectLayerByAttribute_management("aer_manzana", "NEW_SELECTION",where_expression)

    aeumax = 0

    for row11 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf",
                                     ["AEU","IDMANZANA"],where_expression):
        if row11[0]>aeumax:
            aeumax=row11[0]


    #print aeumax
    j=0

    while aeumax>=j:
        j=j+1
        #print j

        where_expression_3="UBIGEO=\'" + str(row[0]) + "\' AND ZONA=\'" +str(row[1])+ "\' AND AEU="+str(j)

        print where_expression_3

        where_expression_4=""
        manzanas=[]


        for row22 in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf",
                                           ["IDMANZANA"], where_expression_3):
            manzanas.append(str(row22[0]))

        tamanio_manzanas=len(manzanas)

        k=1
        where_manzanas =""

        for el in manzanas:
            if (k==tamanio_manzanas):
                where_manzanas = where_manzanas+"IDMANZANA=\'" + str(el)+"\'"
            else:
                where_manzanas="IDMANZANA=\'"+str(el)+"\' OR "+where_manzanas
            k=k+1
        print where_manzanas

        #where_expression_4=where_expression_3 + " AND (" +where_manzanas+")"

        mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbana/Xml/segmentacion.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
        arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Rutas/rutas_final.shp",
                                          "rutas_temporal", where_expression_3)
        arcpy.MakeFeatureLayer_management(
            r"D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO_FINAL.shp", "viviendas_temporal",
            where_expression_3)

        arcpy.MakeFeatureLayer_management(
            r"D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas_temporal",
            where_manzanas)

        arcpy.SelectLayerByAttribute_management("rutas_temporal", "NEW_SELECTION", where_expression_3)

        arcpy.SelectLayerByAttribute_management("viviendas_temporal", "NEW_SELECTION", where_expression_3)
        arcpy.SelectLayerByAttribute_management("manzanas_temporal", "NEW_SELECTION", where_manzanas)


        lyrFile1 = arcpy.mapping.Layer("rutas_temporal")
        lyrFile2 = arcpy.mapping.Layer("viviendas_temporal")
        lyrFile3 = arcpy.mapping.Layer("manzanas_temporal")

        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbana/Layers/rutas_final.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile2,
                                                 "D:/ShapesPruebasSegmentacionUrbana/Layers/vivienda_final.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile3,
                                                 "D:/ShapesPruebasSegmentacionUrbana/Layers/manzana_final.lyr")
        arcpy.mapping.AddLayer(df, lyrFile1)

        if lyrFile2.supports("LABELCLASSES"):
            for lblclass in lyrFile2.labelClasses:
                # lblclass.className = "[ORDEN]"
                lblclass.expression = "[OR_VIV_AEU]"
                lblclass.showClassLabels = True

        lyrFile2.showLabels = True



        arcpy.RefreshActiveView()

        arcpy.mapping.AddLayer(df, lyrFile2)
        arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile3)
        arcpy.RefreshActiveView()

        # for el in arcpy.mapping.ListDataFrames(mxd):
        #    print el.name

        # for el2 in arcpy.mapping.ListLayers(mxd):
        #    print el2.name

        ddp = mxd.dataDrivenPages
        indexLayer = ddp.indexLayer

        arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", where_expression_3)

        for indexPage in ddp.selectedPages:
            ddp.currentPageID = indexPage
            ddp.exportToPNG(r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Croquis"+str(row[0])+str(row[1])+str(j)+ ".pdf", "CURRENT")
            # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
        arcpy.mapping.RemoveLayer(df, lyrFile1)
        arcpy.mapping.RemoveLayer(df, lyrFile2)
        # arcpy.mapping.RemoveLayer(df,lyrFile3)

        del mxd
        del df


    i = i+1

    if i>max_zonas:
        break



    #arcpy.mapping.ExportToPDF(mxd,r"D:/ArcGisPDFSegmentacion/pruebaPDF.pdf")

    #print df
    #print df[0]
    #arcpy.SelectLayerByAttribute_management("rutas_temporal")


    #arcpy.mapping.ExportToPDF(mxd,r"D:/ArcGisPDFSegmentacion/pruebaPDF.pdf", "CURRENT")







