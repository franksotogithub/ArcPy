import pymssql

def ActualizarCantViviendasMzs():

    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
    exec ACTUALIZAR_CANTIDAD_VIVIENDAS
    """)
    conn.commit()
    conn.close()

def ActualizarTipoVivienda():

    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
    exec ACTUALIZAR_TIPO_VIVIENDA
    """)
    conn.commit()
    conn.close()

def InsertarAdyacencia():
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
    exec INSERTAR_LISTA_ADYACENCIA
    """)
    conn.commit()
    conn.close()

def InsertarAEUMayores16():
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
    exec INSERTAR_AEU_MANZANAS_MAYORES_16V
    """)
    conn.commit()
    conn.close()

def ActualizarCortes():
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
    exec ACTUALIZAR_CORTES_MANZANA_MAYORES_16V
    """)
    conn.commit()
    conn.close()

def ActualizarOrdenViviendas():
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
    exec ACTUALIZAR_ORDEN_VIVIENDAS
    """)
    conn.commit()
    conn.close()



def InsertarAEUMenores16():
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
    exec INSERTAR_AEU_MANZANAS_MENORES_16V
    """)
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

def ActualizarAEUManzanasIgual0():
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()
    cursor.execute("""
        exec ACTUALIZA_AEU_MZS_VIV_IGUAL_0
        """)
    conn.commit()
    conn.close()

def LimpiarRegistrosSegmentacionTabularUbigeo(ubigeos):
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()

    for row in ubigeos:
        sql_query="""
        exec LIMPIAR_REGISTROS_SEGM_TAB '{ubigeo}','{zona}'
        """.format(ubigeo=str(row),zona="99999")
        cursor.execute(sql_query)
        conn.commit()
    conn.close()


def LimpiarRegistrosSegmentacionEspUbigeo(ubigeos):
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"

    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()

    for row in ubigeos:
        sql_query="""
        exec LIMPIAR_REGISTROS_SEGM_ESP '{ubigeo}','{zona}'
        """.format(ubigeo=str(row),zona="99999")
        cursor.execute(sql_query)
        conn.commit()
    conn.close()

def LimpiarRegistrosMatrizAdyacencia(ubigeos):
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"
    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()

    for row in ubigeos:
        sql_query="""
        exec LIMPIAR_REGISTROS_MATRIZ_ADYACENCIA '{ubigeo}','{zona}'
        """.format(ubigeo=str(row),zona="99999")
        cursor.execute(sql_query)
        conn.commit()
    conn.close()


def ActualizarEstadoAEUSegmEsp(ubigeos):
    server = "192.168.200.250"
    user = "sde"
    password = "$deDEs4Rr0lLo"
    conn = pymssql.connect(server, user, password, "CPV_SEGMENTACION")
    cursor = conn.cursor()

    for row in ubigeos:
        sql_query="""
        exec ACTUALIZAR_ESTADO_AEU_SEGM_ESP '{ubigeo}','{zona}'
        """.format(ubigeo=str(row),zona="99999")
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

