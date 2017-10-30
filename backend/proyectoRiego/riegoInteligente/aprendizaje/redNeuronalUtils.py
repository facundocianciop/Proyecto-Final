

def obtener_eto(mes):

    if mes:
        return 1


def obtener_kc(mes):

    if mes:
        return 1


def obtener_eficiencia_riego(mecanismo):

    if mecanismo == 1:
        # Aspersion
        return 0.8

    if mecanismo == 1:
        # Goteo
        return 0.9

    if mecanismo == 1:
        # Surco
        return 0.5
