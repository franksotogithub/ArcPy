import math



def CalculoRadioCirculo(grupo):
    #print "Grupo:"+str(grupo)
    CentroParX=0
    CentroParY=0

    CntManzanas=0


    #obtenemos el centroide de las manzanas del grupo
    for el in grupo:
        CentroParX=CentroParX+el[3]
        CentroParY = CentroParY + el[4]
        CntManzanas=CntManzanas+1


    CentroParX=CentroParX/CntManzanas
    CentroParY = CentroParY/CntManzanas

    Radio=0
    Distancia=0

    for el in grupo:
        Distancia=math.hypot(el[3]-CentroParX,el[4]-CentroParY)
        if Distancia>Radio:
            Radio=Distancia

    resultado=[]
    centroide=[]
    centroide.append(CentroParX)
    centroide.append(CentroParY)

    resultado.append(centroide)
    resultado.append(Radio)

    return resultado



