import arcpy
import  CirculoMinimo as circulo
import math

arcpy.env.workspace ="D:/ArcGisShapesPruebas"
# First, make a layer from the feature class



def Calculo(solucion,manzanas):
    arcpy.env.overwriteOutput = True



    #arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp", "temporal")

    #arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas/EnvolvesCircles/pruebacirclebuffers.shp", "temporal_circulos")
    #arcpy.MakeFeatureLayer_management("D:/ArcGisShapesPruebas/EnvolvesCircles/pruebacirclebuffers.shp", "temporal_circulo")


    Z=0#Valor funcion Objetivo
    #p=0.65
    #q=0.35

    p = 1
    q = 0

    #cant_max_viv=14

    cant_max_viv = 1
    AcumComp1=0
    AcumComp2=0
    Comp1=0
    Comp2=0

    n=0
    tot_viv=0

    m=len(solucion)


    # calculo del componente 1


    for grupo in solucion:
        tot_viv=0
        for manzana in grupo:
            tot_viv=(float(manzana[1])/float(14))+tot_viv


        #print "\n Grupo " + str(grupo) + " : " + " Tot_viv: "+str(tot_viv)

        x=float(tot_viv)/float(cant_max_viv)-1
        if x>0:
            x = pow(x, 2)

        else:
            x = pow(x, 2)


        AcumComp1=AcumComp1+x




    Comp1=AcumComp1/m


    # calculo del componente 2


    for grupo in solucion:

        resultado=circulo.CalculoRadioCirculo(grupo)
        centroide=resultado[0]
        radio=resultado[1]

        Area1=0
        Area2=0
        distancia = 0
        for manzana in manzanas:
            distancia=math.hypot(manzana[3]-centroide[0],manzana[4]-centroide[1])
            if distancia<=radio:
                if manzana in grupo:
                    Area1=Area1+manzana[2]
                else:
                    Area2=Area2+manzana[2]

        AcumComp2=AcumComp2+(Area1/(Area1+Area2))


    Comp2=AcumComp2/m


    Z=p*Comp1+q*Comp2

    return  Z


#print Calculo("D:/ArcGisShapesPruebas/Zones/Shape15013300200.shp","D:/ArcGisShapesPruebas/EnvolvesCirclesBuffers/Shape15013300200.shp")