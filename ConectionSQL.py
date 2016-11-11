import pymssql
def Conexion():
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    connx = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    return connx


def ActualizarCantViviendasMzs():
    conn=Conexion()
    cursor = conn.cursor()
    cursor.execute("""
    exec ACTUALIZAR_CANTIDAD_VIVIENDAS
    """)
    conn.commit()
    conn.close()

def ActualizarCantViviendasMzsCondominios(data):
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()


    for row in data:
        if len(row) == 1:
            sql_query = """
            exec ACTUALIZAR_CANTIDAD_VIVIENDAS_CONDOMINIOS '{ubigeo}', '{zona}'
            """.format(ubigeo=str(row[0]), zona="99999")
            cursor.execute(sql_query)
        elif len(row) == 2:
            sql_query = """
            exec ACTUALIZAR_CANTIDAD_VIVIENDAS_CONDOMINIOS '{ubigeo}', '{zona}'
                """.format(ubigeo=str(row[0]), zona=str(row[1]))
            cursor.execute(sql_query)

        conn.commit()
    conn.close()


def ActualizarCampoMzCondominio(data):
    conn = Conexion()
    cursor = conn.cursor()
    for row in data:
        if len(row) == 1:
            sql_query = """
                exec ACTUALIZAR_CAMPO_MZS_CONDOMINIO '{ubigeo}' '{zona}'
                """.format(ubigeo=str(row), zona="99999")
            cursor.execute(sql_query)
            conn.commit()
        elif len(row) == 2:
            sql_query = """
            exec ACTUALIZAR_CAMPO_MZS_CONDOMINIO '{ubigeo}' '{zona}'
                """.format(ubigeo=str(row[0]), zona=str(row[1]))
            cursor.execute(sql_query)

        conn.commit()
    conn.close()



def Actualizar_MZS_AEU():
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
        exec ACTUALIZAR_MZS_AEU
        """)
    conn.commit()
    conn.close()


def LimpiarRegistrosSegmentacionTabularUbigeo(data):
    conn = Conexion()
    cursor = conn.cursor()

    for row in data:
        if len(row) == 1:
            sql_query = """
            exec LIMPIAR_REGISTROS_SEGM_TAB '{ubigeo}','{zona}'
            """.format(ubigeo=str(row[0]), zona="99999")
            cursor.execute(sql_query)
        elif len(row) == 2:
            sql_query = """
                exec LIMPIAR_REGISTROS_SEGM_TAB '{ubigeo}','{zona}'
                """.format(ubigeo=str(row[0]), zona=str(row[1]))
            cursor.execute(sql_query)

        conn.commit()
    conn.close()


def InsertarAdyacencia():
    conn = Conexion()
    cursor = conn.cursor()
    cursor.execute("""
    exec INSERTAR_LISTA_ADYACENCIA
    """)
    conn.commit()
    conn.close()

def LimpiarRegistrosSegmentacionEspUbigeo(data):
    conn = Conexion()
    cursor = conn.cursor()

    for row in data:

        if len(row)==1:
            sql_query="""
            exec LIMPIAR_REGISTROS_SEGM_ESP '{ubigeo}','{zona}'
            """.format(ubigeo=str(row[0]),zona="99999")
            cursor.execute(sql_query)
        elif len(row)==2:
            sql_query = """
                exec LIMPIAR_REGISTROS_SEGM_ESP '{ubigeo}','{zona}'
                """.format(ubigeo=str(row[0]), zona=str(row[1]))
            cursor.execute(sql_query)

        conn.commit()
    conn.close()



def LimpiarRegistrosMatrizAdyacencia(data):
    conn = Conexion()
    cursor = conn.cursor()

    for row in data:
        if len(row)==1:
            sql_query="""
            exec LIMPIAR_REGISTROS_MATRIZ_ADYACENCIA '{ubigeo}','{zona}'
            """.format(ubigeo=str(row[0]),zona="99999")
            cursor.execute(sql_query)
        elif len(row)==2:
            sql_query = """
                exec LIMPIAR_REGISTROS_MATRIZ_ADYACENCIA '{ubigeo}','{zona}'
                """.format(ubigeo=str(row[0]), zona=str(row[1]))
            cursor.execute(sql_query)

        conn.commit()
    conn.close()


def ActualizarEstadoAEUSegmEsp(data):
    conn = Conexion()
    cursor = conn.cursor()
    for row in data:
        if len(row) == 1:
            sql_query = """
            exec ACTUALIZAR_ESTADO_AEU_SEGM_ESP '{ubigeo}','{zona}'
            """.format(ubigeo=str(row[0]), zona="99999")
            cursor.execute(sql_query)
        elif len(row) == 2:
            sql_query = """
                exec ACTUALIZAR_ESTADO_AEU_SEGM_ESP '{ubigeo}','{zona}'
                """.format(ubigeo=str(row[0]), zona=str(row[1]))
            cursor.execute(sql_query)

        conn.commit()
    conn.close()



def ActualizarEstadoAEUSegmTab(data):
    conn = Conexion()
    cursor = conn.cursor()
    for row in data:
        if len(row) == 1:
            sql_query = """
            exec ACTUALIZAR_ESTADO_AEU_SEGM_TAB '{ubigeo}','{zona}'
            """.format(ubigeo=str(row[0]), zona="99999")
            cursor.execute(sql_query)
        elif len(row) == 2:
            sql_query = """
                exec ACTUALIZAR_ESTADO_AEU_SEGM_TAB '{ubigeo}','{zona}'
                """.format(ubigeo=str(row[0]), zona=str(row[1]))
            cursor.execute(sql_query)

        conn.commit()
    conn.close()



#cursor.executemany(
#    "INSERT INTO persons VALUES (%d, %s, %s)",
#    [(1, 'John Smith', 'John Doe'),
#     (2, 'Jane Doe', 'Joe Dog'),
#     (3, 'Mike T.', 'Sarah H.')])
# you must call commit() to persist your data if you don't set autocommit to True



#LimpiarRegistrosSegmentacionTabular(['050601'])


#cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
#row = cursor.fetchone()
#while row:
#    print("ID=%s, UBIGEO=%s" % (str(row[0]), str(row[1])))
    #row = cursor.fetchone()

