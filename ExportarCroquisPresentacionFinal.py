#! -*- coding: utf-8 -*-
import arcpy
import os
import shutil
import sys
#sys.getdefaultencoding()

arcpy.env.overwriteOutput = True  #sirve para sobreescribir los elementos

#
#
#def Crear_Carpetas_Croquis_Zona(ubigeos):
#
#    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
#                                      "zonas")
#
#    where_list=ubigeos
#    #where_list = ["020601", "021806", "110204"]
#
#
#    if os.path.exists("D:/ShapesPruebasSegmentacionUrbana/Croquis")==False:
#        os.mkdir("D:/ShapesPruebasSegmentacionUrbana/Croquis")
#    #shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/Croquis/")
#    lista_directorios=os.listdir("D:/ShapesPruebasSegmentacionUrbana/Croquis/")
#
#    if len(lista_directorios)>0:
#        for el in lista_directorios:
#            shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/Croquis/"+str(el))
#
#    m = 0
#    where_expression = ""
#    for x in where_list:
#        if (m + 1) == len(where_list):
#            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
#        else:
#            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])
#
#        m = m + 1
#
#    with arcpy.arcpy.da.SearchCursor("zonas", ['UBIGEO', 'ZONA'],where_expression) as cursor:
#        for row in cursor:
#            os.mkdir("D:/ShapesPruebasSegmentacionUrbana/Croquis/Zona"+str(row[0])+str(row[1]))
#


def Crear_Carpetas_Croquis_Jefe_Zona(ubigeos):

    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                      "zonas")

    where_list=ubigeos
    #where_list = ["020601", "021806", "110204"]


    if os.path.exists("D:/ShapesPruebasSegmentacionUrbana/CroquisJefeZona")==False:
        os.mkdir("D:/ShapesPruebasSegmentacionUrbana/CroquisJefeZona")

    #shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/Croquis/")
    lista_directorios=os.listdir("D:/ShapesPruebasSegmentacionUrbana/CroquisJefeZona/")

    if len(lista_directorios)>0:
        for el in lista_directorios:
            shutil.rmtree("D:/ShapesPruebasSegmentacionUrbana/CroquisJefeZona/"+str(el))


    for row in ubigeos:
        os.mkdir("D:/ShapesPruebasSegmentacionUrbana/CroquisJefeZona/"+str(row))





def Exportar_Croquis_Urbano_JefeZona(ubigeos):
    ZONA_AEU = "D:/ShapesPruebasSegmentacionUrbana/Renumerar/zona_aeu"

    MZS_AEU = "D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf"

    arcpy.env.workspace ="D:/ShapesPruebasSegmentacionUrbana"
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/zona_aeu", "zona_aeu_x")
    arcpy.MakeTableView_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/MZS_AEU.dbf", "aeu_manzana")
    arcpy.MakeFeatureLayer_management(r"D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp",
                                      "zonas")

    if arcpy.Exists (ZONA_AEU):
        arcpy.Delete_management(ZONA_AEU)


    arcpy.Statistics_analysis(MZS_AEU, ZONA_AEU, [["IDMANZANA", "COUNT"]], ["UBIGEO", "ZONA", "AEU_FINAL"])


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
            Exportar_Croquis_Urbano_Resumen_AEU(str(fila[0]),str(fila[1]))
            #Exportar_Croquis_Urbano_Resumen_Seccion(str(fila[0]), str(fila[1]))



def Exportar_Croquis_Urbano_Resumen_AEU(ubigeo,zona):
    where_inicial = ' "UBIGEO"=\''+str(ubigeo)+'\' AND "ZONA"=\''+str(zona)+'\''
    mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbana/mxd/PresentacionFinal2.mxd")
    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp", "manzanas",
                                      where_inicial)


    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_RUTAS.shp","rutas",where_inicial)
  #  arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", "rutas",
  #                                    where_inicial)


    lyrFile1 = arcpy.mapping.Layer("rutas")
    lyrFile2 = arcpy.mapping.Layer("manzanas")
    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_SECCIONES.shp",
                                      "secciones", where_inicial)

    #lyrFile3 = arcpy.mapping.Layer("manzanas")
    arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                     "D:/ShapesPruebasSegmentacionUrbana/Layers/rutas_colores.lyr")
    arcpy.ApplySymbologyFromLayer_management(lyrFile2,
                                                     "D:/ShapesPruebasSegmentacionUrbana/Layers/manzana_final2.lyr")

    #arcpy.mapping.AddLayer(df, lyrFile1)
    #arcpy.RefreshActiveView()
    lyr = arcpy.mapping.ListLayers(mxd,"zona_censal",df)[0]

    i=0
    aeu_inicial_temp=0
    aeu_final_temp=0

    seccion_inicial_temp = 0
    seccion_final_temp = 0

    for rowx in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_RUTAS.shp", ['AEU_FINAL'], where_inicial):
        aeu_temp=int(rowx[0])
        if (i == 0):
            aeu_inicial_temp = aeu_temp
            aeu_final_temp = aeu_temp
        else:
            if aeu_inicial_temp>aeu_temp:
                aeu_inicial_temp = aeu_temp

            if aeu_final_temp < aeu_temp:
                aeu_final_temp= aeu_temp

        i=i+1
    del rowx

    i=0

    cant_viv=0



    for rowxx in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_SECCIONES.shp", ['SECCION','CANT_VIV'], where_inicial):
        seccion_temp=int(rowxx[0])


        if (i == 0):
            seccion_inicial_temp = seccion_temp
            seccion_final_temp = seccion_temp
        else:
            if seccion_inicial_temp>seccion_temp:
                seccion_inicial_temp = seccion_temp

            if seccion_final_temp < seccion_temp:
                seccion_final_temp= seccion_temp

        cant_viv=cant_viv+int(rowxx[1])
        i = i + 1
    del rowxx


    aeu_inicial = "0" * (3 - len(str(aeu_inicial_temp))) + str(aeu_inicial_temp)
    aeu_final = "0" * (3 - len(str(aeu_final_temp))) + str(aeu_final_temp)

    seccion_inicial = "0" * (3 - len(str(seccion_inicial_temp))) + str(seccion_inicial_temp)
    seccion_final = "0" * (3 - len(str(seccion_final_temp))) + str(seccion_final_temp)

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

    TextElement1.text = ubigeo[0:2]
    TextElement2.text = ubigeo[2:4]
    TextElement3.text = ubigeo[4:6]
    # TextElement4.text = rowxx[1]
    # TextElement5.text = rowxx[2]
    # TextElement6.text = rowxx[3]
    # TextElement7.text = rowxx[4]

    zona=EtiquetaZona(zona)

    TextElement8.text = zona
    TextElement9.text = seccion_inicial
    TextElement13.text = seccion_final
    TextElement10.text = aeu_inicial
    TextElement11.text = aeu_final
    TextElement12.text = cant_viv

    for row4 in arcpy.da.SearchCursor("zonas", ['DEPARTAMEN', 'PROVINCIA', 'DISTRITO', 'NOMCCPP'],where_inicial):
        TextElement4.text = str(row4[0])
        TextElement5.text = row4[1]
        TextElement6.text = row4[2]
        TextElement7.text = row4[3]








    if lyrFile1.supports("LABELCLASSES"):
        for lblclass in lyrFile1.labelClasses:
            lblclass.expression = '"%s" &"AEU "& [AEU_FINAL] &"/"&[VIV_AEU] & "%s"' % (
                "<FNT size='5' >", "</FNT>")
            #lblclass.expression = '[AEU_FINAL]'
            lblclass.showClassLabels = True

    if lyr.supports("SHOWLABELS"):
        for lblclass2 in lyr.labelClasses:
            lblclass2.SQLQuery = where_inicial
            lblclass2.visible = True

    if lyrFile2.supports("LABELCLASSES"):
        for lblclass3 in lyrFile2.labelClasses:
            lblclass3.expression = '[MANZANA]&"/"&[VIV_MZ]'
            lblclass3.showClassLabels = True

    lyrFile1.showLabels = True
    arcpy.mapping.AddLayer(df, lyrFile1)
    arcpy.RefreshActiveView()

    lyr.showLabels=True

    lyrFile2.showLabels = True
    arcpy.mapping.AddLayer(df, lyrFile2)
    arcpy.RefreshActiveView()



    ddp = mxd.dataDrivenPages
    indexLayer = ddp.indexLayer
    arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", where_inicial)
    for indexPage in ddp.selectedPages:
        ddp.currentPageID = indexPage
        ddp.exportToPDF(r"D:/ShapesPruebasSegmentacionUrbana/CroquisJefeZona/"+str(ubigeo)+"/ResumenAEUS"+str(ubigeo)+str(zona)+".pdf", "CURRENT")

    #arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
    # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
    arcpy.mapping.RemoveLayer(df, lyrFile1)
    arcpy.mapping.RemoveLayer(df, lyrFile2)
    # arcpy.mapping.RemoveLayer(df,lyrFile3)

    del mxd
    del df


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

def Exportar_Croquis_Urbano_Resumen_Seccion(ubigeo,zona):

    where_inicial = ' "UBIGEO"=\''+str(ubigeo)+'\' AND "ZONA"=\''+str(zona)+'\''
    mxd = arcpy.mapping.MapDocument(r"D:/ShapesPruebasSegmentacionUrbana/mxd/PresentacionFinal2.mxd")
    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Renumerar/TB_MZS_TRABAJO.shp", "manzanas",
                                      where_inicial)

    arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/EnumerarSecciones/TB_SECCIONES.shp","secciones",where_inicial)
  #  arcpy.MakeFeatureLayer_management("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", "rutas",
  #                                    where_inicial)

    lyrFile1 = arcpy.mapping.Layer("secciones")
    lyrFile2 = arcpy.mapping.Layer("manzanas")
    #lyrFile3 = arcpy.mapping.Layer("manzanas")
    arcpy.ApplySymbologyFromLayer_management(lyrFile1,
                                                     "D:/ShapesPruebasSegmentacionUrbana/Layers/secciones.lyr")
    arcpy.ApplySymbologyFromLayer_management(lyrFile2,
                                                     "D:/ShapesPruebasSegmentacionUrbana/Layers/manzana_final.lyr")

    #arcpy.mapping.AddLayer(df, lyrFile1)
    #arcpy.RefreshActiveView()
    lyr = arcpy.mapping.ListLayers(mxd,"zona_censal",df)[0]


#    if lyrFile1.supports("LABELCLASSES"):
#        for lblclass in lyrFile1.labelClasses:
#            lblclass.expression = '"%s" &"AEU "& [AEU_FINAL] &"/"&[VIV_AEU] & "%s"' % (
#                "<FNT size='5' >", "</FNT>")

















    if lyrFile1.supports("LABELCLASSES"):
        for lblclass in lyrFile1.labelClasses:
            lblclass.expression =' "%s" & "%s" & "SECCION "&[SECCION] & "%s" & "%s"'% (
                "<CLR red='139' green='137' blue='137'>","<FNT size='14' >", "</FNT>","</CLR>")
            #lblclass.expression = ' "%s" "%s" &"SECCION "& [SECCION] &"/"&[VIV_AEU] & "%s" "%s" ' % (
            #    "<CLR red='205' green='201' blue='201'>","<FNT size='12' >", "</FNT>","</CLR>")


            lblclass.showClassLabels = True

    if lyr.supports("SHOWLABELS"):
        for lblclass2 in lyr.labelClasses:
            lblclass2.SQLQuery = where_inicial
            lblclass2.visible = True

    if lyrFile2.supports("LABELCLASSES"):
        for lblclass3 in lyrFile2.labelClasses:
            lblclass3.expression = '[MANZANA]&"/"&[VIV_MZ]'
            lblclass3.showClassLabels = True


    lyr.showLabels=True



    lyrFile2.showLabels = True
    arcpy.mapping.AddLayer(df, lyrFile2)
    arcpy.RefreshActiveView()

    lyrFile1.showLabels = True
    arcpy.mapping.AddLayer(df, lyrFile1)
    arcpy.RefreshActiveView()



    ddp = mxd.dataDrivenPages
    indexLayer = ddp.indexLayer
    arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", where_inicial)
    for indexPage in ddp.selectedPages:
        ddp.currentPageID = indexPage
        ddp.exportToPDF(r"D:/ShapesPruebasSegmentacionUrbana/CroquisJefeZona/"+str(ubigeo)+"/ResumenSecciones"+str(ubigeo)+str(zona)+".pdf", "CURRENT")

    #arcpy.mapping.ExportToPNG(mxd,"D:/ShapesPruebasSegmentacionUrbana/Croquis/CroquiseEJEMPLO.png")
    # arcpy.mapping.PrintMap(mxd, r"\\pincullo\CANONiR4051-OEDS", df)
    arcpy.mapping.RemoveLayer(df, lyrFile1)
    arcpy.mapping.RemoveLayer(df, lyrFile2)
    # arcpy.mapping.RemoveLayer(df,lyrFile3)

    del mxd
    del df


ubigeos=["020601","021806","110204"]
Crear_Carpetas_Croquis_Jefe_Zona(ubigeos)
Exportar_Croquis_Urbano_JefeZona(ubigeos)


#ubigeo="110204"
#zona="00400"
#Exportar_Croquis_Urbano_Zona2(ubigeo,zona)

