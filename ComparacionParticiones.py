#conjuntos

#B=set(lista2)
#print B
#print A==B

def CompararConjuntos(lista1,lista2):
    condicion_final=1
    condicion=0
    for elemento in lista1:

        el=set(elemento)
        condicion=0
        for elemento2 in lista2:
            el2=set(elemento2)
            if el==el2:
                condicion=1
                break


        condicion_final=condicion*condicion_final

        #print condicion_final

        if condicion_final==0:
            return 0

    return condicion_final


def CompararConjuntos_nivel2(lista1,lista2):
    condicion_final = 1
    condicion = 0
    for el in lista1:
        condicion = 0
        for el2 in lista2:
            #print CompararConjuntos(el, el2)
            if CompararConjuntos(el, el2) == 1:
                condicion = 1
                break
        condicion_final = condicion * condicion_final

        if condicion_final==0:
            return 0

    return condicion_final



def CopiarElementos_nivel1(lista1,lista2):
    lista1 = []
    for row4 in lista2:
        lista1.append(row4)
    del row4
    return lista1

#lista1=[["a","15"],["b","15"]]
#A=set(lista1)
#print A
#lista2=[["b","15"],["a","15"]]

#print CompararConjuntos(lista1,lista2)

#particion1=[[["b","15"],["a","20"]],[["d","19"],["c","18"]]]
#particion2=[[["a","20"],["b","15"]],[["c","18"],["d","19"]]]

#print CompararConjuntos_nivel2(particion1,particion2)


def diferencia_listas(lista1, lista2):
    lista_temporal = []
    for row1 in lista1:
        for row2 in lista2:
            if set(row1) == set(row2):
                lista_temporal.append(row1)
                break

    for row in lista_temporal:
        lista1.remove(row)

    return lista1


