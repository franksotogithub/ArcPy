manzanas_temporal=[["a",20],["b",19],["c",15],["d",20],["e",15],["f",16]]
manzanas_temporal_2=[["a",20],["b",19],["m",15],["n",20],["o",15],["p",16]]
#diferencia de temporal-temporal2


def diferencia_listas(lista1,lista2):
    lista_temporal=[]
    for row1 in lista1:
        for row2 in lista2:
            if set(row1)==set(row2):
                lista_temporal.append(row1)
                break

    for row in lista_temporal:
        lista1.remove(row)

    return lista1



diferencia_listas(manzanas_temporal,manzanas_temporal_2)
print manzanas_temporal