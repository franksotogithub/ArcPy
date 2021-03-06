
import os
import shutil
import arcpy

import  UBIGEO

from time import time
from datetime import *


def CrearCarpetasCroquisSegmEsp(ubigeos):
    arcpy.env.workspace = "D:/ShapesPruebasSegmentacionUrbanaCondominios"
    ZONAS=r"D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    Path_inicial = "\\\srv-fileserver\\CPV2017"
    if os.path.exists(Path_inicial+"\\croquis_segm_esp")==False:
        os.mkdir(Path_inicial+"\\croquis_segm_esp")

    Path_urbano = Path_inicial + "\\croquis_segm_esp\\urbano"

    if os.path.exists(Path_urbano) == False:
        os.mkdir(Path_urbano)

    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)

    for row in ubigeos:
        print row
        if os.path.exists(Path_urbano+"\\"+ str(row)) == False:
            os.mkdir(Path_urbano+"\\"+ str(row))

    with arcpy.da.SearchCursor(ZONAS, ['UBIGEO', 'ZONA'],where_expression) as cursor:
        for row in cursor:
            #print Path_urbano+"\\"+ str(row[0])+"\\"+str(row[1])
            if os.path.exists(Path_urbano+"\\"+ str(row[0])+"\\"+str(row[1])) == False:
                os.mkdir(Path_urbano+"\\"+ str(row[0])+"\\"+str(row[1]))
    del cursor


#def Crear_Carpetas_Croquis_AEU(ubigeos):
#    arcpy.MakeFeatureLayer_management(r"D:\ShapesPruebasSegmentacionUrbanaCondominios\AEU\EnumerarAEUViviendas\TB_ZONA_CENSAL.shp",
#                                      "zonas")
#
#    where_list=ubigeos
#
#
#
#    if os.path.exists("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CroquisUrbanoAEU")==False:
#        os.mkdir("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CroquisUrbanoAEU")
#
#
#    lista_directorios=os.listdir("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CroquisUrbanoAEU/")
#
#
#
#    if len(lista_directorios)>0:
#        for el in lista_directorios:
#
#            shutil.rmtree("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CroquisUrbanoAEU/"+str(el))
#
#
#
#
#
#    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)
#
#    with arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'],where_expression) as cursor:
#        for row in cursor:
#            os.mkdir("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CroquisUrbanoAEU/"+str(row[0])+str(row[1]))

#def EliminarCroquisAEU():
#    lista_directorios=os.listdir("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CroquisUrbanoAEU/")
#    if len(lista_directorios)>0:
#        for el in lista_directorios:
#            os.remove("D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CroquisUrbanoAEU/" + str(el))
#

def ExportarCroquisUrbanoAEU(where_expression):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbanaCondominios"
    MZS_AEU_dbf = "D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"
    RUTAS_LINEAS_MULTIPART = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS_MULTIPART.shp"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    AEUS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS.dbf"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    VIVIENDAS_ORDENADAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_VIVIENDAS_ORDENADAS.shp"
    ZONA_CENSAL  = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"

    Path_inicial = "\\\srv-fileserver\\CPV2017"
    Path_urbano = Path_inicial + "\\croquis_segm_esp\\urbano"

    #where_expression=UBIGEO.ExpresionUbigeos(ubigeos)


    #where_expression=' "UBIGEO"=\'150116\' AND "ZONA"=\'00500\' '

    print where_expression
    for row in arcpy.da.SearchCursor(AEUS, ["UBIGEO", "ZONA",  "AEU_FINAL","CANT_VIV","CODCCPP","SECCION"],where_expression):
        where_segundo = ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA" =\'' + str(row[1]) + '\' AND AEU_FINAL=' + str(row[2])
        print where_segundo
        #print ' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA" =\'' + str(row[1]) + '\' AND AEU_FINAL=' + str(row[2]) + ' AND SECCION=' + str(row[5])


        where_zona =' "UBIGEO"=\'' + str(row[0]) + '\' AND "ZONA" =\'' + str(row[1]) + '\' '

        i=0
        where_temporal=""



        for row1 in arcpy.da.SearchCursor(MZS_AEU_dbf, ["UBIGEO","ZONA","MANZANA"],where_segundo):
            if (i == 0):

                where_temporal = ' "IDMANZANA"=\'' + str(row1[0]) +str(row1[1]) +str(row1[2])+'\''

            else:
                where_temporal = where_temporal + ' OR "IDMANZANA"=\'' + str(row1[0]) +str(row1[1]) +str(row1[2]) + '\''

            i = i + 1

        where_rutas = where_segundo
        #where_mapa = ' "UBIGEO"=\'' + str(int(row[0])) + '\' AND "ZONA" =\'' + str(int(row[1])) + '\' AND AEU_FINAL=' + str(int(row[2]))
        where_mapa = where_segundo

        where_viviendas = where_segundo + ' AND ( P29=1 OR P29=3 ) '
        where_manzanas=where_temporal



        mxd = arcpy.mapping.MapDocument(
            r"D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Mxd/CroquisSegmentacionUrbanoFinal2.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]


        arcpy.MakeFeatureLayer_management(TB_MZS_shp, "manzanas", where_manzanas)
        arcpy.MakeFeatureLayer_management(RUTAS_LINEAS_MULTIPART, "rutas_lineas", where_rutas)
        arcpy.MakeFeatureLayer_management(RUTAS_PUNTOS, "rutas_puntos", where_rutas)
        arcpy.MakeFeatureLayer_management(VIVIENDAS_ORDENADAS,"viviendas",where_viviendas)


        lyrFile1 = arcpy.mapping.Layer("rutas_lineas")
        #lyrFile2 = arcpy.mapping.Layer("viviendas")
        lyrFile3 = arcpy.mapping.Layer("manzanas")
        lyrFile4 = arcpy.mapping.Layer("rutas_puntos")

        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/rutas_lineas.lyr")
        #arcpy.ApplySymbologyFromLayer_management(lyrFile2,
        #                                         "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/vivienda_final.lyr")
        arcpy.ApplySymbologyFromLayer_management(lyrFile3,
                                                 "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/manzana_final.lyr")

        arcpy.ApplySymbologyFromLayer_management(lyrFile4,
                                                 "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/rutas_puntos.lyr")

        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()

        #arcpy.mapping.AddLayer(df, lyrFile2)
        #arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile3)
        arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile4)
        arcpy.RefreshActiveView()

        viv_aeu = int(row[3])
        seccion = "0" * (3 - len(str(row[5]))) + str(row[5])
        aeu = "0" * (3 - len(str(row[2]))) + str(row[2])
        ubigeo = str(row[0])
        zona = UBIGEO.EtiquetaZona(str(row[1]))
        codigo = str(row[0]) + str(row[1]) + seccion + aeu
        TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
        TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
        TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
        TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
        TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
        TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
        TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
        TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
        TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU")[0]
        TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION")[0]
        TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VIV_AEU")[0]
        TextElement12 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "COD_BARRA")[0]
        TextElement13 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TEXT_COD_BARRA")[0]

        TextElement1.text = ubigeo[0:2]
        TextElement2.text = ubigeo[2:4]
        TextElement3.text = ubigeo[4:6]
        TextElement8.text = zona
        TextElement9.text = str(aeu)
        TextElement10.text = seccion
        TextElement11.text = str(viv_aeu)
        TextElement12.text = str(codigo)
        TextElement13.text=str(codigo)



        for row4 in arcpy.da.SearchCursor(ZONA_CENSAL, ['DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP'],where_zona):
            TextElement4.text = str(row4[0])
            TextElement5.text = row4[1]
            TextElement6.text = row4[2]
            TextElement7.text = row4[3]


        df.extent = lyrFile3.getSelectedExtent()
        df.scale = df.scale

        dflinea=arcpy.Polyline(arcpy.Array([ arcpy.Point (df.extent.XMin,df.extent.YMin) ,arcpy.Point(  df.extent.XMax,df.extent.YMax)]),df.spatialReference)
        distancia=dflinea.getLength("GEODESIC","METERS")

        if (float(distancia)<=50):
            df.scale = df.scale*4

        if (float(distancia)>50 and float(distancia)<=100):
            df.scale = df.scale*3

        if (float(distancia)>100 and float(distancia)<=490):
            df.scale = df.scale*2

        if (float(distancia)>490 and float(distancia)<=900):
            df.scale = df.scale*1.5

        if (float(distancia)>900 and float(distancia)<=1200):
            df.scale = df.scale*1.25

        if (float(distancia)>1200 and float(distancia)<=1800):
            df.scale = df.scale*1.10

        if (float(distancia)>1800):
            df.scale = df.scale*1.05
        #ddp = mxd.dataDrivenPages
        #indexLayer = ddp.indexLayer

        #arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", where_mapa)
        #print where_mapa

        out = Path_urbano + "\\" + str(row[0]) + "\\" + str(row[1]) + "\\" + codigo + ".pdf"

        #print out
        arcpy.mapping.ExportToPDF(mxd,out , "PAGE_LAYOUT")
        #for indexPage in ddp.selectedPages:
        #    ddp.currentPageID = indexPage
        #    #print indexPage
#
#
        #    out=Path_urbano+"\\" + str(row[0]) + "\\" + str(row[1]) + "\\" + codigo + ".pdf"
        #    #print out
        #    ddp.exportToPDF(out, "CURRENT")


        arcpy.mapping.RemoveLayer(df, lyrFile1)
        #arcpy.mapping.RemoveLayer(df, lyrFile2)
        arcpy.mapping.RemoveLayer(df, lyrFile3)
        arcpy.mapping.RemoveLayer(df, lyrFile4)


        del mxd
        del df

#def Crear_Carpetas_Croquis_Seccion(ubigeos):
#
#
#    arcpy.MakeFeatureLayer_management(r"D:\ShapesPruebasSegmentacionUrbanaCondominios\AEU\EnumerarAEUViviendas\TB_ZONA_CENSAL.shp",
#                                      "zonas")
#
#    where_expression = UBIGEO.ExpresionUbigeos(ubigeos)
#
#    if os.path.exists("D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/CroquisUrbanoSeccion") == False:
#        os.mkdir("D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/CroquisUrbanoSeccion")
#
#    lista_directorios = os.listdir("D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/CroquisUrbanoSeccion")
#
#    if len(lista_directorios) > 0:
#        for el in lista_directorios:
#            shutil.rmtree("D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/CroquisUrbanoSeccion/" + str(el))
#
#
#
#    with arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'], where_expression) as cursor:
#        for row in cursor:
#            os.mkdir("D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/CroquisUrbanoSeccion/" + str(row[0]) + str(row[1]))
#
#def EliminarCroquisSeccion():
#    lista_directorios=os.listdir("D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/CroquisUrbanoSeccion/")
#    if len(lista_directorios)>0:
#        for el in lista_directorios:
#            os.remove("D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/CroquisUrbanoSeccion/" + str(el))
#

def ExportarCroquisUrbanoSeccion(where_expression):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbanaCondominios"
    ZONA_SECCION = r"D:/ShapesPruebasSegmentacionUrbanaCondominios/EnumerarSecciones/zona_seccion"
    ZONA_CENSAL = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    ZONA_AEU="D:/ShapesPruebasSegmentacionUrbanaCondominios/EnumerarSecciones/zona_aeu"

    AEUS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS.dbf"
    MZS_AEU="D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

    SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"

    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"
    AEUS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS_PUNTOS.shp"


    #where_expression=UBIGEO.ExpresionUbigeos(ubigeos)
    Path_inicial = "\\\srv-fileserver\\CPV2017"
    Path_urbano = Path_inicial + "\\croquis_segm_esp\\urbano"

    for row1 in arcpy.da.SearchCursor(SECCIONES, ['UBIGEO', 'ZONA', 'SECCION','CANT_VIV'],where_expression):
        where_expression1= ' "UBIGEO"=\''+str(row1[0])+'\' AND "ZONA"=\''+str(row1[1])+'\' AND SECCION=' +str(row1[2])
        where_expression_zona = ' "UBIGEO"=\'' + str(row1[0]) + '\' AND "ZONA"=\'' + str(row1[1]) + '\''

        mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/Mxd/CroquisSegmentacionUrbanoSecciones.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

        where_expression3=''

        where_expression2 = ''

        i = 0

        aeu_inicial_temp=0
        aeu_final_temp=0



        for row2 in arcpy.da.SearchCursor(AEUS, ['AEU_FINAL'], where_expression1):
            where_expression2 = ' "UBIGEO"=\'' + str(row1[0]) + '\' AND "ZONA"=\'' + str(row1[1]) + '\' AND AEU_FINAL='+str(row2[0])

            if (i==0):
                aeu_inicial_temp=int(row2[0])
            else:
                aeu_final_temp=int(row2[0])

            for row3 in arcpy.da.SearchCursor(MZS_AEU, ["UBIGEO","ZONA","MANZANA"],where_expression2):
                if (i==0):

                    where_expression3=' "IDMANZANA"=\'' + str(row3[0])+str(row3[1])+str(row3[2]) + '\''
                else:

                    where_expression3 = where_expression3+' OR "IDMANZANA"=\''+str(row3[0])+str(row3[1])+str(row3[2])+'\''

                i=i+1

       #where_mapa = ' "UBIGEO"=\'' + str(int(row1[0])) + '\' AND "ZONA" =\'' + str(int(row1[1])) + '\' AND SECCION='+ str(int(row1[2]))

        where_mapa = where_expression1
        ubigeo = str(row1[0])
        zona = UBIGEO.EtiquetaZona(str(row1[1]))
        seccion = "0"*(3-len(str(row1[2])))+str(row1[2])
        aeu_inicial="0"*(3-len(str(aeu_inicial_temp)))+str(aeu_inicial_temp)
        aeu_final = "0" * (3 - len(str(aeu_final_temp))) + str(aeu_final_temp)
        cant_viv=str(int(row1[3]))
        arcpy.MakeFeatureLayer_management(SECCIONES,"secciones_1", where_expression1)
        arcpy.MakeFeatureLayer_management(TB_MZS_shp, "manzanas", where_expression3)
        #arcpy.MakeFeatureLayer_management(AEUS_LINEAS, "aeus_lineas", where_expression1)
        #arcpy.MakeFeatureLayer_management(AEUS_PUNTOS, "aeus_puntos", where_expression1)
        #arcpy.MakeFeatureLayer_management(RUTAS_LINEAS, "rutas_lineas", where_expression1)


        #arcpy.MakeFeatureLayer_management(TB_MZS_shp, "manzanas", where_expression3)

        lyrFile1 = arcpy.mapping.Layer("secciones_1")
        lyrFile2 = arcpy.mapping.Layer("manzanas")
        #lyrFile3 = arcpy.mapping.Layer("aeus_lineas")
        #lyrFile4 = arcpy.mapping.Layer("aeus_puntos")

        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/seccion.lyr")

        arcpy.ApplySymbologyFromLayer_management(lyrFile2,
                                             "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/manzana_final.lyr")


        #arcpy.ApplySymbologyFromLayer_management(lyrFile3,
        #                                         "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/mapa_secciones_aeus_lineas.lyr")
#
#
        #arcpy.ApplySymbologyFromLayer_management(lyrFile4,
        #                                         "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/mapa_secciones_aeus_puntos.lyr")

        arcpy.RefreshActiveView()
        arcpy.mapping.AddLayer(df, lyrFile2)
        arcpy.RefreshActiveView()
        #arcpy.mapping.AddLayer(df, lyrFile3)
        #arcpy.RefreshActiveView()
        #arcpy.mapping.AddLayer(df, lyrFile4)
        #arcpy.RefreshActiveView()


        #if lyrFile1.supports("LABELCLASSES"):
        #    for lblclass in lyrFile1.labelClasses:
        #        lblclass.expression = '"%s" &"AEU "& [AEU_FINAL]  & "%s"' % (
        #        "<FNT size='5' >", "</FNT>")
        #        lblclass.showClassLabels = True
        #lyrFile1.showLabels = True

        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()

        codigo=str(row1[0]) + str(row1[1]) + seccion
        #ddp = mxd.dataDrivenPages
        #indexLayer = ddp.indexLayer



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
        TextElement13 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "COD_BARRA")[0]
        TextElement14 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TEXT_COD_BARRA")[0]

        TextElement13.text = str(codigo)
        TextElement14.text = str(codigo)

        TextElement1.text = ubigeo[0:2]
        TextElement2.text = ubigeo[2:4]
        TextElement3.text = ubigeo[4:6]

        TextElement8.text = zona
        TextElement9.text = seccion
        TextElement10.text = aeu_inicial
        TextElement11.text = aeu_final
        TextElement12.text = cant_viv


        df.extent = lyrFile2.getSelectedExtent()
        df.scale = df.scale *2



        for row4 in arcpy.da.SearchCursor(ZONA_CENSAL, ['DEPARTAMEN','PROVINCIA','DISTRITO','NOMCCPP'],where_expression_zona):
            TextElement4.text=str(row4[0])
            TextElement5.text = row4[1]
            TextElement6.text = row4[2]
            TextElement7.text = row4[3]

        out = Path_urbano + "\\" + str(row1[0]) + "\\" + str(row1[1]) + "\\" + codigo + ".pdf"
        arcpy.mapping.ExportToPDF(mxd,out , "PAGE_LAYOUT")


        arcpy.mapping.RemoveLayer(df, lyrFile1)
        arcpy.mapping.RemoveLayer(df, lyrFile2)
        #arcpy.mapping.RemoveLayer(df, lyrFile3)
        #arcpy.mapping.RemoveLayer(df, lyrFile4)



def ExportarCroquisUrbanoZona(where_expression):
    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbanaCondominios"

    ZONA_CENSAL = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_ZONA_CENSAL.shp"
    ZONA_AEU="D:/ShapesPruebasSegmentacionUrbanaCondominios/EnumerarSecciones/zona_aeu"


    AEUS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS.dbf"
    MZS_AEU="D:\\ShapesPruebasSegmentacionUrbanaCondominios\\AEU\\EnumerarAEUViviendas\\MZS_AEU.dbf"

    SECCIONES = "D:/ShapesPruebasSegmentacionUrbanaCondominios/SECCIONES/EnumerarSecciones/TB_SECCIONES.shp"
    AEUS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Renumerar/TB_AEUS_LINEAS.shp"
    TB_MZS_shp = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/EnumerarAEUViviendas/TB_MZS.shp"
    RUTAS_LINEAS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_LINEAS.shp"
    RUTAS_PUNTOS = "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/CrearRepresentacionAEU/TB_RUTAS_PUNTOS.shp"

    Path_inicial = "\\\srv-fileserver\\CPV2017"
    Path_urbano = Path_inicial + "\\croquis_segm_esp\\urbano"


    #where_expression = UBIGEO.ExpresionUbigeos(ubigeos)

    for row_seccion in arcpy.da.SearchCursor(ZONA_CENSAL, ['UBIGEO', 'ZONA'], where_expression):
        ubigeo=row_seccion[0]
        zona=row_seccion[1]

        where_inicial = ' "UBIGEO"=\'' + str(ubigeo) + '\' AND "ZONA"=\'' + str(zona) + '\''
        print where_inicial
        mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbanaCondominios/ZONAS/Mxd/CroquisSegmentacionUrbanoZonas.mxd")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]



        #arcpy.MakeFeatureLayer_management(RUTAS_LINEAS, "rutas_lineas",
        #                                  where_inicial)


        #arcpy.MakeFeatureLayer_management(RUTAS_PUNTOS, "rutas_puntos",where_inicial)

        #arcpy.MakeFeatureLayer_management(TB_MZS_shp, "manzanas",
        #                                  where_inicial)

        arcpy.MakeFeatureLayer_management(ZONA_CENSAL, "zona_censal",where_inicial)

        lyrFile1 = arcpy.mapping.Layer("zona_censal")
        #lyrFile2 = arcpy.mapping.Layer("manzanas")
        #lyrFile3 = arcpy.mapping.Layer("zona_censal_layer")
        #lyrFile4 = arcpy.mapping.Layer("rutas_puntos")


        #arcpy.MakeFeatureLayer_management(SECCIONES,
        #                                  "secciones", where_inicial)

        # lyrFile3 = arcpy.mapping.Layer("manzanas")
        #arcpy.ApplySymbologyFromLayer_management(lyrFile1,
        #                                         "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/rutas_colores.lyr")
        #arcpy.ApplySymbologyFromLayer_management(lyrFile2,
        #                                         "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/manzana_final2.lyr")

        arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                 "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/zonas.lyr")


        #arcpy.ApplySymbologyFromLayer_management(lyrFile4,
        #                                         "D:/ShapesPruebasSegmentacionUrbanaCondominios/AEU/Layers/aeus_puntos.lyr")

        #lyr = arcpy.mapping.ListLayers(mxd, "TB_ZONA_CENSAL", df)[0]

        i = 0
        aeu_inicial_temp = 0
        aeu_final_temp = 0

        seccion_inicial_temp = 0
        seccion_final_temp = 0

        for rowx in arcpy.da.SearchCursor(RUTAS_LINEAS,
                                          ['AEU_FINAL'], where_inicial):
            aeu_temp = int(rowx[0])
            if (i == 0):
                aeu_inicial_temp = aeu_temp
                aeu_final_temp = aeu_temp
            else:
                if aeu_inicial_temp > aeu_temp:
                    aeu_inicial_temp = aeu_temp

                if aeu_final_temp < aeu_temp:
                    aeu_final_temp = aeu_temp

            i = i + 1
        del rowx

        i = 0

        cant_viv = 0

        for rowxx in arcpy.da.SearchCursor(SECCIONES,
                                           ['SECCION', 'CANT_VIV'], where_inicial):
            seccion_temp = int(rowxx[0])

            if (i == 0):
                seccion_inicial_temp = seccion_temp
                seccion_final_temp = seccion_temp
            else:
                if seccion_inicial_temp > seccion_temp:
                    seccion_inicial_temp = seccion_temp

                if seccion_final_temp < seccion_temp:
                    seccion_final_temp = seccion_temp

            cant_viv = cant_viv + int(rowxx[1])
            i = i + 1
        del rowxx


        aeu_inicial = "0" * (3 - len(str(aeu_inicial_temp))) + str(aeu_inicial_temp)
        aeu_final = "0" * (3 - len(str(aeu_final_temp))) + str(aeu_final_temp)

        seccion_inicial = "0" * (3 - len(str(seccion_inicial_temp))) + str(seccion_inicial_temp)
        seccion_final = "0" * (3 - len(str(seccion_final_temp))) + str(seccion_final_temp)

        codigo = str(ubigeo) + str(zona)
        zona_etiqueta = UBIGEO.EtiquetaZona(zona)

        TextElement1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDD")[0]
        TextElement2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCPP")[0]
        TextElement3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCDI")[0]
        TextElement4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DEPARTAMENTO")[0]
        TextElement5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "PROVINCIA")[0]
        TextElement6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DISTRITO")[0]
        TextElement7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "NOMCCPP")[0]
        TextElement8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZONA")[0]
        TextElement9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION_INICIAL")[0]
        TextElement13 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SECCION_FINAL")[0]
        TextElement10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU_INICIAL")[0]
        TextElement11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "AEU_FINAL")[0]
        TextElement12 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CANT_VIV")[0]

        TextElement14 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "COD_BARRA")[0]
        TextElement15 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TEXT_COD_BARRA")[0]

        TextElement14.text = str(codigo)
        TextElement15.text = str(codigo)
        TextElement1.text = ubigeo[0:2]
        TextElement2.text = ubigeo[2:4]
        TextElement3.text = ubigeo[4:6]



        TextElement8.text = zona_etiqueta
        TextElement9.text = seccion_inicial
        TextElement13.text = seccion_final
        TextElement10.text = aeu_inicial
        TextElement11.text = aeu_final
        TextElement12.text = cant_viv

        for row4 in arcpy.da.SearchCursor(ZONA_CENSAL, ['DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP'], where_inicial):
            TextElement4.text = str(row4[0])
            TextElement5.text = row4[1]
            TextElement6.text = row4[2]
            TextElement7.text = row4[3]


        arcpy.mapping.AddLayer(df, lyrFile1)
        arcpy.RefreshActiveView()

        df.extent = lyrFile1.getSelectedExtent()
        df.scale = df.scale *1.2

        out = Path_urbano + "\\" + str(row_seccion[0]) + "\\" + str(row_seccion[1]) + "\\" + codigo + ".pdf"

        arcpy.mapping.ExportToPDF(mxd,out , "PAGE_LAYOUT")

        arcpy.mapping.RemoveLayer(df, lyrFile1)


        del mxd
        del df


    del row_seccion








#ubigeos=['021509']
#CrearCarpetasCroquisSegmEsp(ubigeos)
#Exportar_Croquis_Urbano_AEU(ubigeos)



#Crear_Carpetas_Croquis_AEU(ubigeos)
#print "Crear_Carpetas_Croquis_AEU"
#print datetime.today()
#Exportar_Croquis_Urbano_AEU(ubigeos)
#print "Exportar_Croquis_Urbano_AEU"
#print datetime.today()

#
#Crear_Carpetas_Croquis_Seccion(ubigeos)
#print "Crear_Carpetas_Croquis_Seccion"
#Exportar_Croquis_Urbano_Seccion(ubigeos)
#print "Exportar_Croquis_Urbano_Seccion"


#ubigeos=["020601","021806"]
#EliminarCroquisAEU()
#Exportar_Croquis_Urbano_AEU(ubigeos)
#print "Exportar_Croquis_Urbano_AEU"
#EliminarCroquisSeccion()
#Exportar_Croquis_Urbano_Seccion(ubigeos)
#EliminarCroquisZona()
#Exportar_Croquis_Urbano_Zona(ubigeos)
#print "Exportar_Croquis_Urbano_Zona"




