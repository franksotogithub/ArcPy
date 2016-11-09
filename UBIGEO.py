def ExpresionUbigeos(where_list):
    m=0
    where_expression=""
    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=\'%s\' ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=\'%s\' OR' % (where_list[m])

        m = m + 1

    return  where_expression



def Expresion(data,campos):
    m = 0
    where_expression = ""
    cant_campos=len(campos)

    #sql_query = """
    #exec ACTUALIZAR_CAMPO_MZS_CONDOMINIO '{ubigeo}'
    #""".format(ubigeo=str(row), zona="99999")

    for fila in data:
        if (m + 1) == len(data):
            fila_expresion=""
            n = 0
            for campo in campos:


                if (n+1)==len(campos):
                    fila_expresion = fila_expresion+""" \"{nombre_campo}\"=\'{data}\'  """.format(nombre_campo=campos[n],data=fila[n])
                else:
                    fila_expresion = fila_expresion+""" \"{nombre_campo}\"=\'{data}\' AND """.format(nombre_campo=campos[n],data=fila[n])
                n=n+1
            where_expression = where_expression + "("+fila_expresion+")"

        else:
            fila_expresion = ""
            n = 0
            for campo in campos:

                if (n+1) == len(campos):
                    fila_expresion = fila_expresion + """ \"{nombre_campo}\"=\'{data}\'  """.format(nombre_campo=campos[n],data=fila[n])
                else:
                    fila_expresion = fila_expresion + """ \"{nombre_campo}\"=\'{data}\' AND """.format(nombre_campo=campos[n],data=fila[n])
                n = n + 1

            where_expression = where_expression + "("+fila_expresion + ") OR "


        m = m + 1

    return where_expression






def ExpresionUbigeosImportacion(where_list):
    m=0
    where_expression = ""
    for x in where_list:
        if (m + 1) == len(where_list):
            where_expression = where_expression + ' "UBIGEO"=%s ' % where_list[m]
        else:
            where_expression = where_expression + ' "UBIGEO"=%s OR' % (where_list[m])

        m = m + 1

    return where_expression



def EtiquetaZona(zona):
    rango_equivalencia=[[1,'A'],[2,'B'],[3,'C'],[4,'D'],[5,'E'],[6,'F'],[7,'G'],[8,'H'],[9,'I'],[10,'J'],[11,'K'],[12,'L'],[13,'M'],[14,'N'],[15,'O'],[16,'P'],[17,'Q']]

    #zona='001001'

    zona_temp=zona[0:3]
    zona_int=int(zona[3:])
    zona_int_eq=""
    # busacar equivalencia
    for el in rango_equivalencia:
        if (el[0]==zona_int):
            zona_int_eq=el[1]

    zona_temp=zona_temp+str(zona_int_eq)

    return zona_temp

#print ExpresionUbigeos(['01','02','03'])

#print Expresion(data=[['01','02'],['01','03']],campos=['UBIGEO','ZONA'])