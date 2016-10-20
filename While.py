import random

lista=[1,2]
tamanio=len(lista)
while tamanio>0:
    print lista[0]
    lista.remove(lista[0])
    tamanio = len(lista)

