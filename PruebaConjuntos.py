import  ComparacionParticiones as p


lista1=[[["b","15"],["a","20"]],[["d",19],["c","18"]]]
lista2=[[["a","20"],["b","15"]],[["c",18],["d",19]]]

condicion_final=1
condicion=0
for el in lista1:
    for el2 in lista2:
        if p.CompararConjuntos(el,el2)==1:
           condicion=1
    condicion_final=condicion*condicion_final


print condicion_final


Particion1=[]
Particion2=[]


