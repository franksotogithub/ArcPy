import random
#print(random.randint(0,9))
manzanas=[["a",20],["b",19],["c",15],["d",20]]
manzanas_temporal=[["a",20],["b",19],["c",15],["d",20]]


#for manzana in manzanas:
#    manzanas.remove(manzana)
#    i=i+1


#print "Particion: "+ str(particion)

tamanio_original= len(manzanas)
#manzana1=[]
#manzana2=[]

manzana=[]

cant_viviendas=0

particion=[]


for i in range(tamanio_original*3):
    manzanas_temporal = [["a", 20], ["b", 19], ["c", 15], ["d", 20]]

    tamanio = len(manzanas)
    j=random.randint(0, tamanio-1)
    manzana=manzanas[j]


    #print manzanas
    #print manzanas_temporal

    manzanas_temporal.remove(manzana)
    print manzanas_temporal


    tamanio_temporal = len(manzanas_temporal)

    print tamanio_temporal

    grupos=[]




    grupo=[]

    grupo.append(manzana)
    cant_viviendas = manzana[1]

    for n in range(tamanio_temporal):
        tamanio_temporal=len(manzanas_temporal)
        k = random.randint(0, tamanio_temporal - 1)
        manzana2 = manzanas_temporal[k]

        if (cant_viviendas+manzana2[1])<40:
            #print str(manzana) + " - " + str(manzana2)
            grupo.append(manzana2)
            cant_viviendas = cant_viviendas + manzana2[1]
        else:
            break

        manzanas_temporal.remove(manzana2)


    print grupo






  #  manzana1=manzanas[j]
 #   manzanas_temporal.remove(manzana1)
#manzanas.remove('["a",20]')

#tamanio_temporal= len(manzanas_temporal)

#for i in range(tamanio_temporal*3):
#    j = random.randint(0, tamanio_temporal - 1)
#    manzana2 = manzanas[j]


#print manzana1 + " - "  +manzana2