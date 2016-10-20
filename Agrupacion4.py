import random
import ComparacionParticiones as a
import arcpy
particiones=[]


manzanas=[]

manzanas_temporal=[["a",20],["b",19],["c",15],["d",20],["e",15],["f",16]]
manzanas_temporal_2=[["a",20],["b",19],["c",15],["d",20],["e",15],["f",16]]
max_viviendas=40


arcpy.env.workspace = r"D:/ArcGisShapesPruebas"

manzana_temporal=[]


for row1 in arcpy.da.SearchCursor("D:/ArcGisShapesPruebas/Zones/Shape15013300200.dbf", ["IDMANZANA", "TOT_VIV"]):
    manzana = []
    manzana.append(str(row1[0]))
    manzana.append(row1[1])
    manzanas.append(manzana)
    # where_expression = ' "IDMANZANA"=%s' % (str(row1[0]))
print manzanas

for i in range(10):

    manzanas_temporal_2 = []
    for manzana_temp in manzanas:
        manzanas_temporal_2.append(manzana_temp)

    cant_iteraciones = 0

    particion = []
    # manzana=["a",20]
    tamanio = len(manzanas)
    j = random.randint(0, tamanio - 1)

    manzana = manzanas[j]

    tamanio_temporal_2 = len(manzanas_temporal_2)

    if manzana in manzanas_temporal_2:
        manzanas_temporal_2.remove(manzana)

    if manzana in manzanas_temporal:
        manzanas_temporal.remove(manzana)

    while tamanio_temporal_2 > 0:

        manzanas_temporal = []

        for manzana_temp in manzanas_temporal_2:
            manzanas_temporal.append(manzana_temp)

        grupo = []

        if cant_iteraciones == 0:
            grupo.append(manzana)
            cant_viviendas = manzana[1]
        else:
            cant_viviendas = 0

        #tamanio_temporal = len(manzanas_temporal)


        while (tamanio_temporal > 0):

            k = random.randint(0, tamanio_temporal - 1)
            manzana2 = manzanas_temporal[k]
            manzanas_temporal.remove(manzana2)
            tamanio_temporal = len(manzanas_temporal)

            # print tamanio_temporal
            # print manzana2
            # print manzanas_temporal
            # print  manzanas_temporal_2

            if (cant_viviendas + manzana2[1]) < max_viviendas:
                # print str(manzana) + " - " + str(manzana2)
                grupo.append(manzana2)
                cant_viviendas = cant_viviendas + manzana2[1]
                manzanas_temporal_2.remove(manzana2)
            else:
                continue

        # print "Grupo: "+str(grupo)

        particion.append(grupo)
        # manzanas_temporal_2.remove(manzana)
        tamanio_temporal_2 = len(manzanas_temporal_2)

        cant_iteraciones = 1 + cant_iteraciones
    # Aqui discriminanmos los conjuntos repetidos

    res = 0
    if len(particiones) > 0:
        res = 0
        for particion_temporal in particiones:
            res = a.CompararConjuntos_nivel2(particion_temporal, particion)
            if res == 1:
                break

    if res == 0:
        particiones.append(particion)

        # print particion

# particion1=[[["b","15"],["a","20"]],[["d","19"],["c","18"]]]
# particion2=[[["a","20"],["b","15"]],[["c","18"],["d","19"]]]

# a.CompararConjuntos_nivel2()

for particion in particiones:
    print "particion :" + str(particion)



#manzana temporal define las manzanas con las cuales puede relacionarse
#manzana_temporal_2 define las manzanas del listado original , esta lista temporal se va a modificar a lo largo del tiempo, a medida que los
# elementos de esta se eliminan de la lista

