

import arcpy
import  SolucionInicialUrbano as s
import SolucionVecinaUrbano as v
import  CalculoFuncionObjetivo2 as funcionObjetivo
import ActualizarAEU as actualizar


i=0
max_zonas=0
arcpy.env.workspace = r"D:/ShapesPruebasSegmentacionUrbana"
ruta_carpeta=r"D:/ShapesPruebasSegmentacionUrbana"

for row  in arcpy.da.SearchCursor(ruta_carpeta+"/Zones/zona_censal.shp", ["UBIGEO","ZONA","CODCCPP"]):

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"

    resultado=[]
    solucion_inicial_zona=[]
    manzanas=[]
    solucion_vecina = []

    fc=ruta_carpeta+"/Zones/"+desc
    #fc_circles = "D:/ArcGisShapesPruebas/EnvolvesCircles/" + desc
    #fc_circles2 = "D:/ArcGisShapesPruebas/EnvolvesCirclesBuffers/" + desc

    resultado=s.SolucionInicial(fc)  ## se obtiene una solucion inicial




    solucion_inicial=resultado[0]
    manzanas=resultado[1]
#    fc = "D:/ArcGisShapesPruebas/Zones/" + desc
#    file_sol = "D:/ArcGisShapesPruebas/Soluciones/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(
#        row[2]) + "SolucionInicial.shp"
#
#    arcpy.CopyFeatures_management(fc, file_sol)

#    actualizar.ActualizarAER(file_sol,solucion_inicial)
#    #print "\n \n Zona:"  + str(row[0]) + "" + str(row[1]) + "" + str(row[2])
#
    print "Manzanas: " +str(manzanas)
    print "Solucion inicial: "+str(solucion_inicial)

    actualizar.ActualizarAEU(fc,solucion_inicial,manzanas)


#
#    print "zona:" + desc
#    print "Calculo Funcion Objertivo:" + str(funcionObjetivo.Calculo(solucion_inicial,manzanas))
#

    #file_sol = "D:/ArcGisShapesPruebas/Soluciones/ShapeInicial.shp"

    #arcpy.CopyFeatures_management(fc, file_sol)
    #actualizar.ActualizarAER(file_sol, solucion_inicial)




    resultado_vecina=[]
    resultado_vecina=v.SolucionVecina(manzanas,solucion_inicial)[:]
    print "Solucion Vecina: " + str(resultado_vecina)





#
#    solucion_vecina=resultado_vecina[0]
#    indice_grupo_escogido=resultado_vecina[1]
#    indice_grupo_adyacente=resultado_vecina[2]
#
#
#   # print "Funcion Objetivo del vecino 1 :"+ str(funcionObjetivo.Calculo(solucion_vecina, manzanas))
#
#    for i in range(len(solucion_inicial)):
#        if len(solucion_inicial[i]) <> len(solucion_vecina[i]):
#            print "Indice del Grupo modificado:" + str(i)
#            print "Tamanio Grupo " + str(i) + " de S0:" + str(len(solucion_inicial[i]))
#            print "Tamanio Grupo " + str(i) + " de S1:" + str(len(solucion_vecina[i]))
#
#    print "Indice del grupo escodigo:" + str(indice_grupo_escogido)
#    print "Tamanio Grupo Escogido" + str(i) + " de S0:" + str(len(solucion_inicial[indice_grupo_escogido]))
#    print "Tamanio Grupo Escodigo" + str(i) + " de S1:" + str(len(solucion_vecina[indice_grupo_escogido]))
#
#    print "Grupo Escogido de S0: " + str(solucion_inicial[indice_grupo_escogido])
#    print "Grupo Escogido de S1: " + str(solucion_vecina[indice_grupo_escogido])
#
#
#
#
#    print "Indice del grupo adyacente:" + str(indice_grupo_adyacente)
#
#    print "Tamanio Grupo "  + " de S0:" + str(len(solucion_inicial[indice_grupo_adyacente]))
#    print "Tamanio Grupo "  + " de S1:" + str(len(solucion_vecina[indice_grupo_adyacente]))
#    print "Grupo Adyacente de S0: " + str(solucion_inicial[indice_grupo_adyacente])
#    print "Grupo Adyacente de S1: " + str(solucion_vecina[indice_grupo_adyacente])
    #
#    print "Calculo Funcion Objetivo:" + str(funcionObjetivo.Calculo(solucion_vecina, manzanas))
#
#
#
#
#    file_sol = "D:/ArcGisShapesPruebas/Soluciones/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(
#        row[2]) + "SolucionVecina1.shp"
#
#    arcpy.CopyFeatures_management(fc, file_sol)
#
#
#    actualizar.ActualizarAER(file_sol, solucion_vecina)


    #print "Solucion vecina: "+str(solucion_vecina)


    # LUEGO CALCULAR LOS CIRCULOS MINIMOS DE CADA GRUPO

#
#



#
 #   for j in range(5):
 #       solucion_vecina=v.SolucionVecina(manzanas,solucion_vecina)[:]

#        file_sol = "D:/ArcGisShapesPruebas/Soluciones/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2]) + "SolucionVecina"+str(j+1)+".shp"
#        arcpy.CopyFeatures_management(fc, file_sol)
#
#        actualizar.ActualizarAER(file_sol, solucion_vecina)
#
#        print "Calculo Funcion Objetivo:" + str(funcionObjetivo.Calculo(solucion_vecina, manzanas))
#


    #print solucion_vecina


    #Algotirmo de Recocido Simulado









    #arcpy.MinimumBoundingGeometry_management(fc,fc_circles,"CIRCLE", "LIST",["GRUPO"])
    #arcpy.Buffer_analysis(fc_circles,fc_circles2,'0.5 METERS')


    #resultado = funcionObjetivo.Calculo(fc, fc_circles2) # se calcula la funcion objetivo de la solucion inicial
    #print resultado








    #arcpy.Delete_management(fc_circles)
    #arcpy.Delete_management(fc_circles2)


    i=i+1
    if i>max_zonas:
        break
del row