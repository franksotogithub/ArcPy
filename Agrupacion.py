import  numpy

manzanas=[ ["a",20],["b",19],["c",15],["d",20]]
manzanas_temporal=[ ["a",20],["b",19],["c",15],["d",20]]

i=0


particion = []

for manzana in manzanas:
    #manzanas_temporal = [["a", 20], ["b", 19], ["c", 15], ["d", 20]]
    #manzana_inicial=manzana
    #print manzana[0] + " " +manzana[1]
    flg_manzana_agrupada=0
    j=0
    temporal=0

    grupo=[]

    for grupo2 in particion:
        if manzana in grupo2:
            flg_manzana_agrupada = 1


    if flg_manzana_agrupada == 0:

        manzanas_temporal = manzanas
        manzanas_temporal.remove(manzana)

        for grupo3 in particion:
            for el in grupo3:
                if el in  manzanas_temporal:
                    manzanas_temporal.remove(el)


                #manzanas_temporal.remove(el)


        if (temporal+manzana[1])<=40:
            grupo.append(manzana)
            #manzanas.remove(manzana)
            temporal = temporal + manzana[1]
        else:
            temporal = temporal

        for manzana1 in manzanas_temporal:

            if (temporal + manzana1[1]) <= 40:
                grupo.append(manzana1)
                #manzanas.remove(manzana1)
                temporal = temporal + manzana1[1]
            else:
                temporal = temporal

        particion.append(grupo)

    else:
        continue


    #print temporal
    #for  j in range(i,len(manzanas)):
    #    temporal = manzanas[j][1] + temporal

    #print temporal
    i=i+1
    #if manzana[1]

print "Particion: "+ str(particion)
