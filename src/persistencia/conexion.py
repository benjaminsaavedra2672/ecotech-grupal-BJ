

def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"