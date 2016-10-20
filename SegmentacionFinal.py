

import arcpy
import  SolucionInicialUrbano as s
#import SolucionVecinaUrbano as v
#import  CalculoFuncionObjetivo2 as funcionObjetivo
import ActualizarAEU as a
import ConectionSQL as conx
import ImportarExportarSQL as ie

#where_list=["150133","002"]
#where_expression=' "IDDIST"=%s ' % (where_list[0])
#conx.InsertarAdyacencia()
#
ie.Importar_TB_MZ_TRABAJO()
ie.Importar_Lista_ADYACENCIA()

i=0
max_zonas=3

for row  in arcpy.da.SearchCursor("D:/ShapesPruebasSegmentacionUrbana/Zones/zona_censal.shp", ["UBIGEO","ZONA","CODCCPP"]):

    desc = "Shape" + str(row[0]) + "" + str(row[1]) + "" + str(row[2])+".shp"
    print "zona: "+desc
    # Algoritmo Normal

    fc = "D:/ShapesPruebasSegmentacionUrbana/Zones/" + desc

    manzanas = s.Manzanas_menores_iguales_16(fc)[:]
    manzanas1 = manzanas[:]
    componentes = s.Componentes_conexas(manzanas1)[:]

    SM_FINAL=[]
    for componente in componentes:
        if s.Total_Viviendas(componente) <= 16:
            SM_FINAL.append(componente)
            #SM_INICIAL.append(componente)
        else:
            SM=[]
            #SM=prueba.AgrupacionPrueba(componente)[:]
            #SM=s.Componentes_conexas_cantidad_viv(componente)
            SM=s.Agrupacion(componente)
            for el2 in SM:
                SM_FINAL.append(el2)

    a.ActualizarAEU2(fc, SM_FINAL, manzanas)

   # i=i+1
    #if i>max_zonas:
    #    break
del row
#
###########################
ie.Exportar_TB_MZS_TRABAJO()
conx.InsertarAEUMayores16()
conx.InsertarAEUMenores16()
conx.ActualizarCortes()
conx.ActualizarAEUManzanasIgual0() ###manzanas sin adyacencia
conx.Actualizar_MZS_AEU()
conx.ActualizarOrdenViviendas()
ie.Importar_Lista_MZS_AEU()
ie.Importar_Viviendas()
ie.Importar_Cortes()

############################
