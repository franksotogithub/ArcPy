

import arcpy
import  SolucionInicial2 as s
import SolucionVecina as v
import  CalculoFuncionObjetivo2 as funcionObjetivo
import ActualizarAER as a


where_list=["150133","002"]
where_expression=' "IDDIST"=%s ' % (where_list[0])
i=0
max_zonas=0


for row  in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/Zones/zona_censal.shp", ["UBIGEO","ZONA","CODCCPP"]):

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"
    print "zona: "+desc
    # Algoritmo de Recocido Simulado
    resultado=[]
    solucion_inicial_zona=[]
    manzanas=[]
    solucion_vecina = []

    MaxSolRech=25000
    SolRec = 0
    Lote=30
    T0=0.05
    T = T0
    DecT=0.95
    epsilon=0.001




    fc="D:/ArcGisShapesPruebas/Zones/"+desc


  #  file_sol="D:/ArcGisShapesPruebas/Soluciones/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+"SolucionInicial.shp"

 #   arcpy.CopyFeatures_management(fc,file_sol)



    resultado=s.SolucionInicial2(fc)  ## se obtiene una solucion inicial
    S0=resultado[0] # se guarda la solucion inicial
    manzanas=resultado[1] # se guarda la lista de manzanas

    ZS0=funcionObjetivo.Calculo(S0,manzanas)
    # guardamos la conformacion de So en SM


    SM=S0[:]
    #guardamos la funcion objetivo
    ZSM = ZS0



    fc = "D:/ArcGisShapesPruebas/Zones/" + desc
    file_sol = "D:/ArcGisShapesPruebas/Soluciones/Shape" + str(row[0]) + "" + str(row[1]) + "" + str(
        row[2]) + "SolucionInicial.shp"

    arcpy.CopyFeatures_management(fc, file_sol)

    a.ActualizarAER(file_sol, S0, manzanas)
    #a.ActualizarAER(file_sol,S0)


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
                S1=v.SolucionVecina(manzanas,S0)[:]

                ZS1=funcionObjetivo.Calculo(S1,manzanas)
                if ZS1<(ZS0+T):
                    SolAcept=SolAcept+1
                    ZS0=ZS1

                    print "Funcion Objetivo aceptada:"+str(ZS0)


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

          #          tamanio=len(S0)
                    print "Soluciones Rechazadas:" + str(SolRec)
          #         for i in range(0,tamanio-1):
          #             if len(S0[i])<>len(S1[i]):
          #                 print "Indice del Grupo de S0:"+str(i)
          #                 print "Tamanio Grupo de S0:" + str(len(S0[i]))
          #                 print "Tamanio Grupo de S1:" + str(len(S1[i]))






            if ( (Lotes>=2) and (Prom2>(Prom1-epsilon))   ) or (SolRec>=MaxSolRech)  :
                break
                # fin de segunda iteracion
        T=T*DecT

        print "Decremento temperatura"+str(T)
        if (T<(0.001*T0)) or (SolRec>=MaxSolRech):
            break

    # fin de primera iteracion

    #Guardar Conformacion


    print "Fin de Zona"
    print "Funcion Objetivo aceptada:" + str(ZSM)
    a.ActualizarAER(fc, SM,manzanas)






    prom_viv=0

    for el in SM:
        sum=0
        i=1
        for el2 in el:
            sum=el2[1]+sum

        print "Grupo: "+str(i)+" Total de Viviendas: "+str(sum)

        prom_viv=prom_viv+sum
        i=i+1


    print "Promedio de viviendas: " +  str(prom_viv/len(SM))


    i=i+1
    if i>max_zonas:
        break





del row