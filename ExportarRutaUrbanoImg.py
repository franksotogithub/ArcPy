import arcpy

arcpy.env.overwriteOutput = True  #sirve para sobreescribir los elementos

arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"




arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/zona_aeu", "zona_aeu_x")
arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/ShapesFinal/MZS_AEU.dbf", "aeu_manzana")

where_inicial = " UBIGEO=\'020601\' "


with arcpy.arcpy.da.SearchCursor("zona_aeu_x", ['UBIGEO', 'ZONA','AEU'],where_inicial) as cursor1:
    for row1 in cursor1:
        where_segundo = ' "UBIGEO"=\'' +str(row1[0])+' \' AND "ZONA" =\''+str(row1[1])+'\' AND AEU='+str(row1[2])

        where_rutas =where_segundo
        where_viviendas = where_segundo+ ' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '

        i=0
        with arcpy.arcpy.da.SearchCursor("aeu_manzana", ['UBIGEO', 'ZONA', 'IDMANZANA','AEU'],where_segundo) as cursor3:
            for row3 in cursor3:

                if i==0:
                    where_temporal3 = ' "FIRST_TB_M"=\'' + str(row3[2]) + '\''
                    where_temporal=' "IDMANZANA"=\'' + str(row3[2]) + '\''
                    where_temporal2=' "MANZANA"=\''+str(row3[2][11:])+'\''
                else:
                    where_temporal = where_temporal+' OR "IDMANZANA"=\'' + str(row3[2]) + '\''
                    where_temporal2 = where_temporal2+' OR "MANZANA"=\''+str(row3[2][11:])+'\''

                i=i+1


        where = where_temporal
        print where


        if i==1:
            where_mapa=where_temporal3
        else:
            where_mapa = ' "MZS_AEU_AE"=' + str(row1[2]) + ' AND "TB_MZS_TRA"=\''+str(row1[0])+'\' AND "TB_MZS_T_1"=\''+str(row1[1])+'\''

        print where_mapa


        where_rutas = where_rutas+ ' AND ('+where_temporal2+')'
        where_viviendas = where_viviendas+' AND ('+where_temporal2+')'


        #where_viviendas=' UBIGEO=\'021806\' AND "ZONA" =\'00800\' AND "MANZANA"=\'001O\' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '
        mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbana/mxd/segmentacion5.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

        arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp", "manzanas",where)
        arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Rutas/TB_RUTAS.shp","rutas",where_rutas)
        arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp", "viviendas",where_viviendas)




        #arcpy.SelectLayerByAttribute_management("rutas_temporal", "NEW_SELECTION", where)
        #arcpy.SelectLayerByAttribute_management("viviendas_temporal", "NEW_SELECTION", where_viviendas)

        #arcpy.SelectLayerByAttribute_management("manzanas_temporal", "NEW_SELECTION", where)
        lyrFile1 = arcpy.mapping.Layer("rutas")
        lyrFile2 = arcpy.mapping.Layer("viviendas")
        lyrFile3 = arcpy.mapping.Layer("manzanas")
        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbana/Layers/rutas_final.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile2,
                                                 "D:/ShapesPruebasSegmentacionUrbana/Layers/vivienda_final.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile3,
                                                 "D:/ShapesPruebasSegmentacionUrbana/Layers/manzana_final.lyr")
        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()

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
        arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", where_mapa)
        for indexPage in ddp.selectedPages:
            ddp.currentPageID = indexPage

            ddp.exportToPDF(r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Croquis"+str(row1[0])+str(row1[1])+str(row1[2])+".pdf", "CURRENT")

        #arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
        # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
        arcpy.mapping.RemoveLayer(df, lyrFile1)
        arcpy.mapping.RemoveLayer(df, lyrFile2)
        arcpy.mapping.RemoveLayer(df, lyrFile3)


        # arcpy.mapping.RemoveLayer(df,lyrFile3)

        del mxd
        del df









