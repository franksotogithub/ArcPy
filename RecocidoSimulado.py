

import arcpy
import  SolucionInicialUrbano as s
import SolucionVecinaUrbano as v
import  CalculoFuncionObjetivo2 as funcionObjetivo
import ActualizarAEU as a


#where_list=["150133","002"]
#where_expression=' "IDDIST"=%s ' % (where_list[0])
i=0
max_zonas=0


for row  in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", ["UBIGEO","ZONA","CODCCPP"]):

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"
    print "zona: "+desc
    # Algoritmo de Recocido Simulado




    fc="D:/ShapesPruebasSegmentacionUrbana/Zones/"+desc

    manzanas=s.Manzanas_menores_16(fc)
    manzanas1=manzanas[:]
    componentes=s.Componentes_conexas(manzanas1)

    SM_FINAL=[]
    SM_INICIAL=[]
    file_sol="D:/ShapesPruebasSegmentacionUrbana/Soluciones/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+"SolucionInicial.shp"

    #arcpy.CopyFeatures_management(fc,file_sol)


    for componente in componentes:
        if s.Total_Viviendas(componente)<=16:
            SM_FINAL.append(componente)
            SM_INICIAL.append(componente)
        else:

            resultado = []
            solucion_inicial_zona = []
            #manzanas = []
            solucion_vecina = []
            componentes = []
            MaxSolRech = 50000
            SolRec = 0
            Lote = 30
            T0 = 0.05
            T = T0
            DecT = 0.95
            epsilon = 0.001

            resultado=s.SolucionInicial(componente)[:]  ## se obtiene una solucion inicial
            S0=resultado[:] # se guarda la solucion inicial
            #manzanas=resultado[1] # se guarda la lista de manzanas

            for elx in S0:
                SM_INICIAL.append(elx)

            #a.ActualizarAEU2(file_sol, SM_INICIAL, manzanas)
            ZS0=funcionObjetivo.Calculo(S0,componente)
            # guardamos la conformacion de So en SM

            SM=S0[:]
            #guardamos la funcion objetivo
            ZSM = ZS0



     #       fc = "D:/ShapesPruebasSegmentacionUrbana/Zones/" + desc
     #       file_sol = "D:/ShapesPruebasSegmentacionUrbana/Soluciones/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(
     #           row[2]) + "SolucionInicial.shp"
#


           # arcpy.CopyFeatures_management(fc, file_sol)





            #a.ActualizarAEU(fc, SM_FINAL, manzanas)

            #a.ActualizarAEU(file_sol, S0, manzanas)
            #a.ActualizarAER(file_sol,S0)
            #print "actualizado"

            ###primera iteracion

            while True:
                Prom2=0
                Lotes=0
                #print "Soluciones Rechazadas:" + str(SolRec)
                # segunda iteracion
                while True:
                    #print "Soluciones Rechazadas:" + str(SolRec)
                    SolAcept=0
                    Prom1=Prom2
                    AcumLote=0
                     #tercera iteracion
                    while (SolAcept<Lote) and (SolRec<MaxSolRech):
                        #print "Soluciones Rechazadas:" + str(SolRec)
                        S1=[]
                        S1=v.SolucionVecina2(componente,S0)[:]

                        ZS1=funcionObjetivo.Calculo(S1,componente)
                        if ZS1<(ZS0+T):
                            SolAcept=SolAcept+1
                            ZS0=ZS1

                            #print "Funcion Objetivo aceptada:"+str(ZS0)


            #               for i in range(0,len(S0)-1):
            #                   if len(S0[i])<>len(S1[i]):
            #                       print "Indice del Grupo modificado:"+str(i)
            #                       print "Tamanio Grupo "+str(i)+" de S0:" + str(len(S0[i]))
            #                       print "Tamanio Grupo "+str(i)+" de S1:" + str(len(S1[i]))




        #guradar la conformacion de s1 en s0


        #                    fc = "D:/ArcGisShapesPruebas/Zones/" + desc
        #                    file_sol = "D:/ArcGisShapesPruebas/Soluciones/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(
        #                        row[2]) + "SolucionVecina"+str(SolAcept)+".shp"
        #
        #                    arcpy.CopyFeatures_management(fc, file_sol)
        #
        #                    a.ActualizarAER(file_sol, S1)
        #


                            S0=[]

                            S0=S1[:]

                            if ZS0<ZSM:
                                SM=S1[:]
                                ZSM=ZS0

                            if SolAcept==1:
                                AcumLote=ZS0
                            else:
                                AcumLote=AcumLote+ZS0

                            if SolAcept==Lote:
                                Prom2=AcumLote/Lote
                                Lotes=Lotes+1

                        else:

                            SolRec=SolRec+1

        #                   tamanio=len(S0)
                            #print "Soluciones Rechazadas:" + str(SolRec)
        #                   for i in range(0,tamanio-1):
        #                      if len(S0[i])<>len(S1[i]):
        #                          print "Indice del Grupo de S0:"+str(i)
        #                          print "Tamanio Grupo de S0:" + str(len(S0[i]))
        #                          print "Tamanio Grupo de S1:" + str(len(S1[i]))






                    if ( (Lotes>=2) and (Prom2>(Prom1-epsilon))   ) or (SolRec>=MaxSolRech)  :
                        break
                        # fin de segunda iteracion
                T=T*DecT

                #print "Decremento temperatura"+str(T)
                if (T<(0.01*T0)) or (SolRec>=MaxSolRech):
                    break

       # fin de primera iteracion

            for el2 in SM:
                SM_FINAL.append(el2)


    #Guardar Conformacion











#    print "Fin de Zona"
#    print "Funcion Objetivo aceptada:" + str(ZSM)

    #print SM_INICIAL
    #print SM_FINAL
    #print manzanas
    a.ActualizarAEU2(file_sol, SM_INICIAL, manzanas)
    a.ActualizarAEU2(fc, SM_FINAL,manzanas)
    #a.ActualizarAEUViviendas(desc)





#    prom_viv=0
#
#    for el in SM:
#        sum=0
#        i=1
#        for el2 in el:
#            sum=el2[1]+sum
#
#        print "Grupo: "+str(i)+" Total de Viviendas: "+str(sum)
#
#        prom_viv=prom_viv+sum
#        i=i+1
#
#
#    print "Promedio de viviendas: " +  str(prom_viv/len(SM))


    i=i+1
    if i>max_zonas:
        break
#


    #arcpy.FeatureClassToFeatureClass_conversion("D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp", "D:/ShapesPruebasSegmentacionUrbana/Viviendas/", desc,where_clause)




del row

#arcpy.FeatureClassToGeodatabase_conversion(['D:/ShapesPruebasSegmentacionUrbana/Viviendas/TB_VIVIENDAS_U_TRABAJO.shp'],
#                                           'Database Connections/PruebaSegmentacion.sde/')
