#! -*- coding: utf-8 -*-
import arcpy
import os
import shutil
import sys
from arcpy import env
#sys.getdefaultencoding()
import  Zonas



arcpy.env.overwriteOutput = True  #sirve para sobreescribir los elementos

#arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"

#arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/zona_aeu", "zona_aeu_x")
#arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", "aeu_manzana")

#def Exportar_Croquis_Urbano():

def Crear_Carpetas_Croquis_AEU(ubigeos):

    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                      "zonas")

    where_list=ubigeos
    #where_list = ["020601", "021806", "110204"]


    if os.path.exists("D:/ShapesPruebasSegmentacionUrbana/Croquis")==False:
        os.mkdir("D:/ShapesPruebasSegmentacionUrbana/Croquis")

    #shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/Croquis/")
    lista_directorios=os.listdir("D:/ShapesPruebasSegmentacionUrbana/Croquis/")

    if len(lista_directorios)>0:
        for el in lista_directorios:
            shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/Croquis/"+str(el))

    m = 0
    where_expression = ""
    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1

    with arcpy.arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'],where_expression) as cursor:
        for row in cursor:
            os.mkdir("D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona"+str(row[0])+str(row[1]))





def Exportar_Croquis_Urbano_AEU(ubigeos):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"
    ZONA_AEU = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/zona_aeu"
    #ZONA_AEU="D:/ShapesPruebasSegmentacionUrbana/Renumerar/zona_aeu"
    ZONA_CENSAL=r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp"
    MZS_AEU="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/MZS_AEU.dbf"
    MZS_FINAL="D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_FINAL.shp"
    MZS_TRABAJO = "D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp"
    RUTAS = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_RUTAS.shp"

    AEUS = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_AEUS.shp"

#    if arcpy.Exists (ZONA_AEU):
#        arcpy.Delete_management(ZONA_AEU)
#
#    if arcpy.Exists(MZS_FINAL):
#        arcpy.Delete_management(MZS_FINAL)

    #arcpy.Statistics_analysis(MZS_AEU_dbf, MIN_AEU, [["IDMANZANA", "MIN"]], ["UBIGEO", "ZONA", "AEU"])
    #arcpy.Sort_management(MIN_AEU, MIN_AEU_SORT, ["MIN_IDMANZANA","AEU"])
    #arcpy.MakeTableView_management(MIN_AEU_SORT,"min_aeu_sort")

    arcpy.Dissolve_management(MZS_TRABAJO,MZS_FINAL,["UBIGEO","ZONA","AEU_FINAL"],[["IDMANZANA","FIRST"]])
    #arcpy.Statistics_analysis(MZS_AEU, ZONA_AEU, [["IDMANZANA", "COUNT"]], ["UBIGEO", "ZONA", "AEU_FINAL"])
    arcpy.MakeTableView_management(ZONA_AEU, "zona_aeu_x")
    arcpy.MakeTableView_management(MZS_AEU, "mzs_aeu")
    arcpy.MakeFeatureLayer_management(ZONA_CENSAL,"zonas")
    arcpy.MakeFeatureLayer_management(RUTAS, "rutas")
    arcpy.MakeFeatureLayer_management(AEUS, "aeus")


    where_list=ubigeos
    m = 0
    where_expression = ""
    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1

    with arcpy.arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'],where_expression) as cursor:
        for fila in cursor:
            Exportar_Croquis_Urbano_Zona_AEU(str(fila[0]),str(fila[1]))




def Exportar_Croquis_Urbano_Zona_AEU(ubigeo,zona):
    ZONAS = r"D:/ShapesPruebasSegmentacionUrbana/Zones/TB_ZONAS.shp"
    MZS = "D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"
    where_inicial = ' "UBIGEO"=\''+str(ubigeo)+'\' AND "ZONA"=\''+str(zona)+'\''


    with arcpy.arcpy.da.SearchCursor("aeus", ['UBIGEO', 'ZONA','AEU_FINAL','SECCION','SUM_VIV_AE'],where_inicial) as cursor1:
        for row1 in cursor1:
            where_segundo = ' "UBIGEO"=\'' +str(row1[0])+'\' AND "ZONA" =\''+str(row1[1])+'\' AND AEU_FINAL='+str(row1[2])
            where_expression_zona = ' "UBIGEO"=\'' + str(row1[0]) + '\' AND "ZONA"=\'' + str(row1[1]) + '\''
            print  where_segundo
            where_rutas =where_segundo
            where_viviendas = where_segundo+ ' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '

            i=0
            viv_aeu=int(row1[4])
            seccion="0"*(3-len(str(row1[3])))+str(row1[3])
            aeu="0"*(3-len(str(row1[2])))+str(row1[2])
            ubigeo=str(row1[0])
            zona= EtiquetaZona(str(row1[1]))

            with arcpy.arcpy.da.SearchCursor("mzs_aeu", ['UBIGEO', 'ZONA', 'IDMANZANA','AEU_FINAL','VIV_AEU'],where_segundo) as cursor3:
                for row3 in cursor3:

                    if i==0:

                        where_temporal=' "IDMANZANA"=\'' + str(row3[2]) + '\''
                        where_temporal2=' "MANZANA"=\''+str(row3[2][11:])+'\''
                    else:
                        where_temporal = where_temporal+' OR "IDMANZANA"=\'' + str(row3[2]) + '\''
                        where_temporal2 = where_temporal2+' OR "MANZANA"=\''+str(row3[2][11:])+'\''

                    i=i+1

                    #viv_aeu=int(row3[4])+viv_aeu

            where = where_temporal
            where_rutas = where_rutas
            where_viviendas = where_viviendas


            where_mapa=' "UBIGEO"=\'' +str(int(row1[0]))+'\' AND "ZONA" =\''+str(int(row1[1]))+'\' AND AEU_FINAL='+str(int(row1[2]))
            print where_mapa
            #where_viviendas=' UBIGEO=\'021806\' AND "ZONA" =\'00800\' AND "MANZANA"=\'001O\' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '
            mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbana/mxd/CroquisSegmentacionUrbano.mxd")
            df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

            arcpy.MakeFeatureLayer_management(MZS, "manzanas", where)
            #arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp", "manzanas",where)
            arcpy.MakeFeatureLayer_management("rutas","rutas2",where_rutas)
            arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp", "viviendas",where_viviendas)
            arcpy.MakeFeatureLayer_management(ZONAS, "zonas", where_expression_zona)
            TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
            TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
            TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
            TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
            TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
            TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
            TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
            TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
            #TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CATEGORIACCPP")[0]
            TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU")[0]
            TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION")[0]
            TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VIV_AEU")[0]
            #TextElement.text =str(row1[0])[0:2]
            # -*- coding: 850 -*-

            TextElement1.text = ubigeo[0:2]
            TextElement2.text = ubigeo[2:4]
            TextElement3.text = ubigeo[4:6]
            TextElement8.text = zona
            TextElement9.text = str(aeu)
            TextElement10.text = seccion
            TextElement11.text = str(viv_aeu)

            for row4 in arcpy.da.SearchCursor("zonas", ['DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP']):
                TextElement4.text = str(row4[0])
                TextElement5.text = row4[1]
                TextElement6.text = row4[2]
                TextElement7.text = row4[3]


            lyrFile1 = arcpy.mapping.Layer("rutas2")
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
                    lblclass.showClassLabels = False

            lyrFile2.showLabels = False
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
            #mxd = arcpy.mapping.MapDocument(r"C:\Project\Project.mxd")



            #df_mapa = arcpy.mapping.ListDataFrames(mxd, "Mapa")[0]
            for indexPage in ddp.selectedPages:
                ddp.currentPageID = indexPage
                #arcpy.mapping.ExportToJPEG(mxd, r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona" + str(row1[0]) + str(
                #    row1[1]) + "/Imagen" + str(row1[0]) + str(row1[1]) + str(row1[2]) + ".jpeg", df,
                #                           df_export_width=1024,
                #                           df_export_height=1024,
                #                           resolution=1600, world_file=True)

               # arcpy.mapping.ExportToPNG(mxd, r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona"+ str(row1[0]) + str(
               #     row1[1]) + "/ImagenPNG" + str(row1[0]) + str(row1[1]) + str(row1[2]) + ".png", df,
               #                           df_export_width=1600,
               #                           df_export_height=1600,
               #                           world_file=True)
#
             #   arcpy.mapping.ExportToEPS(mxd, r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona" + str(row1[0]) + str(
             #       row1[1]) + "/ImagenEPS" + str(row1[0]) + str(row1[1]) + str(row1[2]) + ".png", df,
             #                             df_export_width=640,
             #                             df_export_height=640)

                #arcpy.mapping.ExportToSVG(mxd, r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona" + str(row1[0]) + str(
                #    row1[1]) + "/PDF"+ str(row1[0]) + str(row1[1]) + str(row1[2]) + ".pdf", df,
                #                          df_export_width=2400,
                #                          df_export_height=2400)
                ddp.exportToPDF(r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona"+str(row1[0])+str(row1[1])+"/Croquis"+str(row1[0])+str(row1[1])+str(row1[2])+".pdf", "CURRENT")

            #arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
            # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
            arcpy.mapping.RemoveLayer(df, lyrFile1)
            arcpy.mapping.RemoveLayer(df, lyrFile2)
            arcpy.mapping.RemoveLayer(df, lyrFile3)


            # arcpy.mapping.RemoveLayer(df,lyrFile3)

            del mxd
            del df



def Exportar_Croquis_Urbano_Zona2(ubigeo, zona):

    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/zona_aeu", "zona_aeu_x")
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", "aeu_manzana")
    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                      "zonas")

    where_inicial = ' "UBIGEO"=\'' + str(ubigeo) + '\' AND "ZONA"=\'' + str(zona) + '\''
    with arcpy.arcpy.da.SearchCursor("zona_aeu_x", ['UBIGEO', 'ZONA', 'AEU'], where_inicial) as cursor1:
        for row1 in cursor1:
            where_segundo = ' "UBIGEO"=\'' + str(row1[0]) + ' \' AND "ZONA" =\'' + str(
                row1[1]) + '\' AND AEU_FINAL=' + str(row1[2])

            where_rutas = where_segundo
            where_viviendas = where_segundo + ' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '

            i = 0
            viv_aeu = 0
            aeu = "00" + str(row1[2])
            with arcpy.arcpy.da.SearchCursor("aeu_manzana", ['UBIGEO', 'ZONA', 'IDMANZANA', 'AEU_FINAL', 'VIV_AEU'],
                                             where_segundo) as cursor3:
                for row3 in cursor3:

                    if i == 0:
                        where_temporal3 = ' "FIRST_TB_M"=\'' + str(row3[2]) + '\''
                        where_temporal = ' "IDMANZANA"=\'' + str(row3[2]) + '\''
                        where_temporal2 = ' "MANZANA"=\'' + str(row3[2][11:]) + '\''
                    else:
                        where_temporal = where_temporal + ' OR "IDMANZANA"=\'' + str(row3[2]) + '\''
                        where_temporal2 = where_temporal2 + ' OR "MANZANA"=\'' + str(row3[2][11:]) + '\''

                    i = i + 1

                    viv_aeu = int(row3[4]) + viv_aeu

            where = where_temporal
            # print where


            if i == 1:
                where_mapa = where_temporal3
            else:
                where_mapa = ' "MZS_AEU_AE"=' + str(row1[2]) + ' AND "TB_MZS_TRA"=\'' + str(
                    row1[0]) + '\' AND "TB_MZS_T_1"=\'' + str(row1[1]) + '\''

            # print where_mapa


            where_rutas = where_rutas + ' AND (' + where_temporal2 + ')'


            #where_rutas_2=

            where_viviendas = where_viviendas + ' AND (' + where_temporal2 + ')'

            # where_viviendas=' UBIGEO=\'021806\' AND "ZONA" =\'00800\' AND "MANZANA"=\'001O\' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '
            mxd = arcpy.mapping.MapDocument(
                r"D:/ShapesPruebasSegmentacionUrbana/mxd/CroquisSegmentacionUrbano.mxd")
            df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

            arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp",
                                              "manzanas", where)
            arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_RUTAS_DISSOLVE.shp",
                                              "rutas", where_rutas)
            arcpy.MakeFeatureLayer_management(
                r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp", "viviendas",
                where_viviendas)

            TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
            TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
            TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
            TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
            TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
            TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
            TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
            TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
            # TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CATEGORIACCPP")[0]
            TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU")[0]
            TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VIV_AEU")[0]
            # TextElement.text =str(row1[0])[0:2]
            # -*- coding: 850 -*-
            with arcpy.arcpy.da.SearchCursor("manzanas",
                                             ['UBIGEO', 'DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP',
                                              'ZONA', 'AEU']) as cursorxx:
                for rowxx in cursorxx:
                    TextElement1.text = str(rowxx[0])[0:2]
                    TextElement2.text = str(rowxx[0])[2:4]
                    TextElement3.text = str(rowxx[0])[4:6]
                 #   print  rowxx[1]
                 #   print  rowxx[2]
                 #   print  rowxx[3]
                 #   print  u'Cerón'.encode('utf-8')
                 #   cadena= rowxx[4]
                 #   cadena.replace(u"Ã?","n")
                 #   print cadena

                    TextElement4.text =  rowxx[1]
                    TextElement5.text =  rowxx[2]
                    TextElement6.text = rowxx[3]
                    TextElement7.text =rowxx[4]

                    TextElement8.text = str(rowxx[5])[0:3]

            TextElement9.text = str(aeu)
            TextElement11.text = str(viv_aeu)

            # arcpy.SelectLayerByAttribute_management("rutas_temporal", "NEW_SELECTION", where)
            # arcpy.SelectLayerByAttribute_management("viviendas_temporal", "NEW_SELECTION", where_viviendas)

            # arcpy.SelectLayerByAttribute_management("manzanas_temporal", "NEW_SELECTION", where)
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
                    lblclass.showClassLabels = False

            lyrFile2.showLabels = False
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

                ddp.exportToPDF(r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona" + str(row1[0]) + str(
                    row1[1]) + "/Croquis" + str(row1[0]) + str(row1[1]) + str(row1[2]) + ".pdf", "CURRENT")

            # arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
            # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
            arcpy.mapping.RemoveLayer(df, lyrFile1)
            arcpy.mapping.RemoveLayer(df, lyrFile2)
            arcpy.mapping.RemoveLayer(df, lyrFile3)

            # arcpy.mapping.RemoveLayer(df,lyrFile3)

            del mxd
            del df



def CrearMarcosCroquis(ubigeos):
    env.overwriteOutput = True
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"

    ZONA_AEU="D:/ShapesPruebasSegmentacionUrbana/Renumerar/zona_aeu"
    ZONA_CENSAL=r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp"
    MZS_AEU="D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf"
    MZS_TRABAJO = "D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp"
    BUFFER_DISSOLVE = "D:/ShapesPruebasSegmentacionUrbana/Mapas/BufferDissolve"
    MARCOS = "D:/ShapesPruebasSegmentacionUrbana/Mapas/Marcos"
    MARCOS_FINAL = "D:/ShapesPruebasSegmentacionUrbana/Mapas/TB_MARCOS_AEUS.shp"

    if arcpy.Exists (MARCOS_FINAL):
        arcpy.Delete_management(MARCOS_FINAL)

    if arcpy.Exists (ZONA_AEU):
        arcpy.Delete_management(ZONA_AEU)
    #Creando Shape final




    #Eliminado Carpetas de los marcos
    if os.path.exists(BUFFER_DISSOLVE):
        shutil.rmtree(BUFFER_DISSOLVE)
    if os.path.exists(MARCOS):
        shutil.rmtree(MARCOS)
    ####creando las carpetas de los marcos

    os.mkdir(BUFFER_DISSOLVE)
    os.mkdir(MARCOS)

    spatial_reference = arcpy.Describe(MZS_TRABAJO).spatialReference
#    arcpy.CreateFeatureclass_management("D:/ShapesPruebasSegmentacionUrbana/Mapas", "Marcos_final.shp", "POLYGON","",
#                                        "",
#                                        "",
#                                        spatial_reference)
#    arcpy.AddField_management(MARCOS_FINAL, "UBIGEO", "TEXT")
#    arcpy.AddField_management(MARCOS_FINAL, "ZONA", "TEXT")
#    arcpy.AddField_management(MARCOS_FINAL, "AEU_FINAL", "SHORT")
#    arcpy.AddField_management(MARCOS_FINAL, "ID_MAPA", "TEXT")

    arcpy.Statistics_analysis(MZS_AEU, ZONA_AEU, [["IDMANZANA", "COUNT"]], ["UBIGEO", "ZONA", "AEU_FINAL"])

    arcpy.MakeTableView_management(ZONA_AEU, "zona_aeu")
    arcpy.MakeTableView_management(MZS_AEU, "mzs_aeu")
    arcpy.MakeFeatureLayer_management(MZS_TRABAJO,"mzs_trabajo")


    where_list=ubigeos
    m = 0
    where_expression_xx = ""
    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression_xx = where_expression_xx + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression_xx = where_expression_xx + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1


    #cursorXX = arcpy.da.InsertCursor("D:/ShapesPruebasSegmentacionUrbana/Mapas/Marcos_final.shp" ,["SHAPE@"])
    #xy=arcpy.Point(-77.6490655715,-9.27512333229)
    #xy=arcpy.PointGeometry(arcpy.Point(-77.6490655715,-9.27512333229))
    #cursor_insert.insertRow([xy])

 #   with arcpy.da.InsertCursor("D:/ShapesPruebasSegmentacionUrbana/Mapas/Marcos_final.shp" , ["SHAPE@"]) as cursorXX:
 #       #arrayll = arcpy.Array()
 #       xy = arcpy.Point(-77.6490655715, -9.27512333229)
 #       xy2 = arcpy.Point(-77.6490655717, -9.27512333229)
 #       #arrayll.add(xy)
 #       #arrayll.add(xy2)
 #       #cursorXX.insertRow([arcpy.Polyline(arrayll)])
 #   del cursorXX



    arrayll = arcpy.Array()

    j=0
    for row1 in arcpy.da.SearchCursor("zona_aeu", ["UBIGEO", "ZONA", "AEU_FINAL"],where_expression_xx):
        arrayll=arcpy.Array()
        where1=' UBIGEO=\''+str(row1[0])+'\' AND ZONA=\''+str(row1[1])+'\' AND AEU_FINAL='+str(row1[2])

        #lista_manzanas=[]

        i=0
        where_mzs=""
        for row2 in arcpy.da.SearchCursor("mzs_aeu", ["IDMANZANA"],where1):
            if i==0:
                where_mzs=where_mzs+' "IDMANZANA"=\''+str(row2[0])+'\''
            else:
                where_mzs = where_mzs + ' OR "IDMANZANA"=\'' + str(row2[0])+'\''
            i=i+1
        del row2


        in_features=arcpy.SelectLayerByAttribute_management("mzs_trabajo","NEW_SELECTION",where_mzs)
        #arcpy.SelectLayerByAttribute_management("mzs_trabajo", "NEW_SELECTION", )

        out_feature = "D:/ShapesPruebasSegmentacionUrbana/Mapas/Marcos/Marco"+str(row1[0])+str(row1[1])+str(row1[2])+".shp"
        out_feature_2="D:/ShapesPruebasSegmentacionUrbana/Mapas/BufferDissolve/BufferDissolve"+str(row1[0])+str(row1[1])+str(row1[2])+".shp"
        arcpy.FeatureEnvelopeToPolygon_management(in_features, out_feature)
        arcpy.Buffer_analysis(in_features, out_feature_2, "20 METERS", "", "","ALL")
        arcpy.FeatureEnvelopeToPolygon_management(out_feature_2, out_feature)

        arcpy.AddField_management(out_feature, "UBIGEO", "TEXT")
        arcpy.AddField_management(out_feature, "ZONA", "TEXT")
        arcpy.AddField_management(out_feature, "AEU_FINAL", "SHORT")
        arcpy.AddField_management(out_feature, "ID_MAPA", "TEXT")

     #   calculate_expression1="\'"+str(row1[0])+"\'"
     #   calculate_expression2 = "\'" + str(row1[1])+"\'"
     #   calculate_expression3 = str(row1[2])
     #   calculate_expression4 =   str(row1[3])

        arcpy.CalculateField_management(out_feature,"UBIGEO",str(row1[0]))
        arcpy.CalculateField_management(out_feature, "ZONA", str(row1[1]))
        arcpy.CalculateField_management(out_feature, "AEU_FINAL", str(row1[2]))
        arcpy.CalculateField_management(out_feature, "ID_MAPA", str(row1[0])+str(row1[1]) +str(row1[2]))



        #for row3 in arcpy.da.UpdateCursor(out_feature, [""]):
        if (j==0):
            arcpy.CopyFeatures_management(out_feature, MARCOS_FINAL)
        else:
            arcpy.Append_management(out_feature, MARCOS_FINAL)
        j=j+1


      ##for row3 in arcpy.da.SearchCursor(out_feature, ["OID@", "SHAPE@"]):

      #    for part in row3[1]:
      #        for pnt in part:
      #            if pnt:

      #                # Print x,y coordinates of current point
      #                #
      #                print("{}, {}".format(pnt.X, pnt.Y))
      #                arrayll.add(arcpy.Point(pnt.X,pnt.Y))

      #del row3

        #print arrayll



        #with arcpy.da.InsertCursor("D:/ShapesPruebasSegmentacionUrbana/Mapas/Marcos_final.shp" , ["SHAPE@","UBIGEO","ZONA","AEU_FINAL","ID_MAPA"]) as cursorXX:
        #    cursorXX.insertRow([arcpy.Polygon(arrayll),str(row1[0]),str(row1[1]),str(row1[2]),str(row1[0])+str(row1[1])+str(row1[2])])
        #del cursorXX
        #cursorXX.insertRow([arcpy.Polyline(arrayll)])



        #expression="!UBIGEO! + !ZONA! + str(!AEU_FINAL!)"
        #arcpy.CalculateField_management(MARCOS_FINAL, "ID_MAPA", expression)

        #arcpy.Append_management(out_feature,MARCOS_FINAL)
        #manzana = [str(row1[0]), float(row1[1]), float(row1[2])]
        #manzanas_adyacentes.append(manzana)

        #FeatureEnvelopeToPolygon_management(in_features, out_feature_class, {single_envelope})








def Crear_Carpetas_Croquis_Seccion(ubigeos):

    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                      "zonas")

    where_list=ubigeos
    #where_list = ["020601", "021806", "110204"]


    if os.path.exists("D:/ShapesPruebasSegmentacionUrbana/CroquisSeccion")==False:
        os.mkdir("D:/ShapesPruebasSegmentacionUrbana/CroquisSeccion")

    #shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/Croquis/")
    lista_directorios=os.listdir("D:/ShapesPruebasSegmentacionUrbana/CroquisSeccion/")

    if len(lista_directorios)>0:
        for el in lista_directorios:
            shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/CroquisSeccion/"+str(el))

    m = 0
    where_expression = ""
    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1

    with arcpy.arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'],where_expression) as cursor:
        for row in cursor:
            os.mkdir("D:/ShapesPruebasSegmentacionUrbana/CroquisSeccion/Zona"+str(row[0])+str(row[1]))



def Exportar_Croquis_Urbano_Seccion(ubigeos):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"
    ZONA_SECCION = r"D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/zona_seccion"
    ZONA_AEU="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/zona_aeu"
    ZONAS=r"D:/ShapesPruebasSegmentacionUrbana/Zones/TB_ZONAS.shp"
    MZS_AEU="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/MZS_AEU.dbf"
    MZS="D:/ShapesPruebasSegmentacionUrbana/Manzanas/TB_MZS_TRABAJO.shp"
    SECCIONES = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_SECCIONES.shp"
    AEUS = "D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_AEUS.shp"
    RUTAS="D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_RUTAS.shp"

    where_list=ubigeos
    m = 0
    where_expression = ""
    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1


    for row1 in arcpy.da.SearchCursor(ZONA_SECCION, ['UBIGEO', 'ZONA', 'SECCION','SUM_SUM_VIV_AEU'],where_expression):
        where_expression1= ' "UBIGEO"=\''+str(row1[0])+'\' AND "ZONA"=\''+str(row1[1])+'\' AND SECCION=' +str(row1[2])
        where_expression_zona = ' "UBIGEO"=\'' + str(row1[0]) + '\' AND "ZONA"=\'' + str(row1[1]) + '\''

        mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbana/mxd/CroquisSegmentacionUrbanoSecciones.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

        where_expression3=''
        where_expression2 = ''

        i = 0



        aeu_inicial_temp=0
        aeu_final_temp=0

        for row2 in arcpy.da.SearchCursor(ZONA_AEU, ['AEU_FINAL'], where_expression1):
            where_expression2 = ' "UBIGEO"=\'' + str(row1[0]) + '\' AND "ZONA"=\'' + str(row1[1]) + '\' AND AEU_FINAL='+str(row2[0])

            if (i==0):
                aeu_inicial_temp=int(row2[0])
            else:
                aeu_final_temp=int(row2[0])

            for row3 in arcpy.da.SearchCursor(MZS_AEU, ['IDMANZANA'],where_expression2):
                if (i==0):

                    where_expression3=' "IDMANZANA"=\'' + str(row3[0]) + '\''
                else:

                    where_expression3 = where_expression3+' OR "IDMANZANA"=\''+str(row3[0])+'\''

                i=i+1


        print where_expression2
        print  where_expression3


        where_mapa = ' "UBIGEO"=\'' + str(int(row1[0])) + '\' AND "ZONA" =\'' + str(int(row1[1])) + '\' AND SECCION='+ str(int(row1[2]))

        ubigeo = str(row1[0])
        zona = EtiquetaZona(str(row1[1]))
        seccion = "0"*(3-len(str(row1[2])))+str(row1[2])
        aeu_inicial="0"*(3-len(str(aeu_inicial_temp)))+str(aeu_inicial_temp)
        aeu_final = "0" * (3 - len(str(aeu_final_temp))) + str(aeu_final_temp)
        cant_viv=str(int(row1[3]))


        arcpy.MakeFeatureLayer_management(SECCIONES,"secciones", where_expression1)
        #arcpy.MakeFeatureLayer_management(AEUS, "aeus", where_expression1)
        arcpy.MakeFeatureLayer_management(RUTAS, "rutas", where_expression1)
        arcpy.MakeFeatureLayer_management(MZS,"manzanas", where_expression3)
        arcpy.MakeFeatureLayer_management(ZONAS, "zonas", where_expression_zona)

        lyrFile1 = arcpy.mapping.Layer("rutas")
        lyrFile2 = arcpy.mapping.Layer("secciones")
        lyrFile3 = arcpy.mapping.Layer("manzanas")

        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbana/Layers/aeus.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile2,
                                                 "D:/ShapesPruebasSegmentacionUrbana/Layers/seccion.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile3,"D:/ShapesPruebasSegmentacionUrbana/Layers/manzana_final.lyr")

        #arcpy.mapping.AddLayer(df, lyrFile1)

        arcpy.RefreshActiveView()



     #   if lyrFile1.supports("SHOWLABELS"):
     #       for lblclass2 in lyrFile1.labelClasses:
     #           lblclass2.SQLQuery = where_expression1
     #           lblclass2.visible = True

        arcpy.mapping.AddLayer(df, lyrFile3)
        arcpy.RefreshActiveView()

        arcpy.mapping.AddLayer(df, lyrFile2)
        arcpy.RefreshActiveView()

        if lyrFile1.supports("LABELCLASSES"):
            for lblclass in lyrFile1.labelClasses:
                # lblclass.className = "[ORDEN]"

                lblclass.expression = '"%s" &"AEU "& [AEU_FINAL]  & "%s"' % (
                "<FNT size='5' >", "</FNT>")
                #lblclass.expression = ' \'<FNT size=\'6\'>\'& "AE "& [AEU_FINAL]'
                lblclass.showClassLabels = True
        lyrFile1.showLabels = True

        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()



        # for el in arcpy.mapping.ListDataFrames(mxd):
        #    print el.name
        # for el2 in arcpy.mapping.ListLayers(mxd):
        #    print el2.name
        ddp = mxd.dataDrivenPages
        indexLayer = ddp.indexLayer

        TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
        TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
        TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
        TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
        TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
        TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
        TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
        TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
        TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION")[0]
        TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU_INICIAL")[0]
        TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU_FINAL")[0]
        TextElement12 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CANT_VIV")[0]

        TextElement1.text = ubigeo[0:2]
        TextElement2.text = ubigeo[2:4]
        TextElement3.text = ubigeo[4:6]
        #TextElement4.text = rowxx[1]
        #TextElement5.text = rowxx[2]
        #TextElement6.text = rowxx[3]
        #TextElement7.text = rowxx[4]
        TextElement8.text = zona
        TextElement9.text = seccion
        TextElement10.text = aeu_inicial
        TextElement11.text = aeu_final
        TextElement12.text = cant_viv


        for row4 in arcpy.da.SearchCursor("zonas", ['DEPARTAMEN','PROVINCIA','DISTRITO','NOMCCPP']):
            TextElement4.text=str(row4[0])
            TextElement5.text = row4[1]
            TextElement6.text = row4[2]
            TextElement7.text = row4[3]



        arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", where_mapa)
        for indexPage in ddp.selectedPages:
            ddp.currentPageID = indexPage

            ddp.exportToPDF(
                r"D:/ShapesPruebasSegmentacionUrbana/CroquisSeccion/Zona" + str(row1[0]) + str(row1[1]) + "/CroquisSeccion" + str(
                    row1[0]) + str(row1[1]) + str(row1[2]) + ".pdf", df_export_width=1600,
                          df_export_height=1600)

        # arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
        # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)


        arcpy.mapping.RemoveLayer(df, lyrFile1)
        arcpy.mapping.RemoveLayer(df, lyrFile2)
        arcpy.mapping.RemoveLayer(df, lyrFile3)







    #with arcpy.arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'],where_expression) as cursor:
    #    for fila in cursor:
    #        Exportar_Croquis_Urbano_Zona_Seccion(str(fila[0]),str(fila[1]))


def EtiquetaZona(zona):
    rango_equivalencia=[[1,'A'],[2,'B'],[3,'C'],[4,'D'],[5,'E'],[6,'F'],[7,'G'],[8,'H'],[9,'I'],[10,'J'],[11,'K'],[12,'L'],[13,'M'],[14,'N'],[15,'O'],[16,'P'],[17,'Q']]

    #zona='001001'

    zona_temp=zona[0:3]
    zona_int=int(zona[3:])
    zona_int_eq=""
    # busacar equivalencia
    for el in rango_equivalencia:
        if (el[0]==zona_int):
            zona_int_eq=el[1]

    zona_temp=zona_temp+str(zona_int_eq)

    return zona_temp


def Exportar_Croquis_Urbano_Zona_Seccion(ubigeo,zona):
    where_inicial = ' "UBIGEO"=\''+str(ubigeo)+'\' AND "ZONA"=\''+str(zona)+'\''

    with arcpy.arcpy.da.SearchCursor("zona_aeu_x", ['UBIGEO', 'ZONA','AEU_FINAL'],where_inicial) as cursor1:
        for row1 in cursor1:
            where_segundo = ' "UBIGEO"=\'' +str(row1[0])+'\' AND "ZONA" =\''+str(row1[1])+'\' AND AEU_FINAL='+str(row1[2])
            print  where_segundo
            where_rutas =where_segundo
            where_viviendas = where_segundo+ ' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '

            i=0
            viv_aeu=0
            aeu="0"*(3-len(str(row1[2])))+str(row1[2])


            with arcpy.arcpy.da.SearchCursor("mzs_aeu", ['UBIGEO', 'ZONA', 'IDMANZANA','AEU_FINAL','VIV_AEU'],where_segundo) as cursor3:
                for row3 in cursor3:

                    if i==0:
                        where_temporal3 = ' "FIRST_TB_M"=\'' + str(row3[2]) + '\''
                        where_temporal=' "IDMANZANA"=\'' + str(row3[2]) + '\''
                        where_temporal2=' "MANZANA"=\''+str(row3[2][11:])+'\''
                    else:
                        where_temporal = where_temporal+' OR "IDMANZANA"=\'' + str(row3[2]) + '\''
                        where_temporal2 = where_temporal2+' OR "MANZANA"=\''+str(row3[2][11:])+'\''

                    i=i+1

                    viv_aeu=int(row3[4])+viv_aeu

            where = where_temporal
            #print where


            #if i==1:
            #    where_mapa=where_temporal3
            #else:
            #    where_mapa = ' "MZS_AEU_AE"=' + str(row1[2]) + ' AND "TB_MZS_TRA"=\''+str(row1[0])+'\' AND "TB_MZS_T_1"=\''+str(row1[1])+'\''

            #print where_mapa



            #where_rutas = where_rutas
                          #+ ' AND ('+where_temporal2+')'
            #where_viviendas = where_viviendas

                              #+' AND ('+where_temporal2+')'

            where_mapa=' "UBIGEO"=\'' +str(int(row1[0]))+'\' AND "ZONA" =\''+str(int(row1[1]))+'\' AND AEU_FINAL='+str(int(row1[2]))

            print where_mapa
            #where_viviendas=' UBIGEO=\'021806\' AND "ZONA" =\'00800\' AND "MANZANA"=\'001O\' AND ( USOLOCAL=1 OR USOLOCAL=3 ) '
            mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbana/mxd/CroquisSegmentacionUrbano.mxd")
            df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

            arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp", "manzanas",where)
            arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_RUTAS.shp","rutas",where_rutas)
            arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_VIVIENDAS_U_TRABAJO.shp", "viviendas",where_viviendas)

            TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
            TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
            TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
            TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
            TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
            TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
            TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
            TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
            #TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CATEGORIACCPP")[0]
            TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU")[0]
            TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VIV_AEU")[0]
            #TextElement.text =str(row1[0])[0:2]
            # -*- coding: 850 -*-
            with arcpy.arcpy.da.SearchCursor("manzanas", ['UBIGEO','DEPARTAMEN','PROVINCIA','DISTRITO','NOMCCPP','ZONA', 'AEU']) as cursorxx:
                for rowxx in cursorxx:
                    TextElement1.text=str(rowxx[0])[0:2]
                    TextElement2.text = str(rowxx[0])[2:4]
                    TextElement3.text = str(rowxx[0])[4:6]
                    TextElement4.text =  rowxx[1]
                    TextElement5.text =  rowxx[2]
                    TextElement6.text = rowxx[3]
                    TextElement7.text =rowxx[4]
                    TextElement8.text = str(rowxx[5])[0:3]

            TextElement9.text = str(aeu)
            TextElement11.text = str(viv_aeu)





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
                    lblclass.showClassLabels = False

            lyrFile2.showLabels = False
            arcpy.RefreshActiveView()
            #arcpy.mapping.AddLayer(df, lyrFile2)
            #arcpy.RefreshActiveView()
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

                ddp.exportToPDF(r"D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona"+str(row1[0])+str(row1[1])+"/Croquis"+str(row1[0])+str(row1[1])+str(row1[2])+".pdf", "CURRENT")

            #arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
            # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
            arcpy.mapping.RemoveLayer(df, lyrFile1)
            arcpy.mapping.RemoveLayer(df, lyrFile2)
            arcpy.mapping.RemoveLayer(df, lyrFile3)


            # arcpy.mapping.RemoveLayer(df,lyrFile3)

            del mxd
            del df




#CrearMarcosCroquis()
#ubigeos = ["110204"]
#CrearMarcosCroquis(ubigeos)
#Crear_Carpetas_Croquis_AEU(ubigeos)
#Exportar_Croquis_Urbano_AEU(ubigeos)

ubigeos = ["020601"]
#Crear_Carpetas_Croquis_Seccion(ubigeos)
#Exportar_Croquis_Urbano_Seccion(ubigeos)

#ubigeos = ["110204"]
Crear_Carpetas_Croquis_AEU(ubigeos)
Exportar_Croquis_Urbano_AEU(ubigeos)

#ubigeo="110204"
#zona="00400"
#Exportar_Croquis_Urbano_Zona2(ubigeo,zona)

