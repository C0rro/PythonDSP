
def loadData(channel):
    nome_file = "Esempio_filtri_REW/filtro" + channel + ".txt"
    dati_clean = []
    with open(nome_file, "r") as f:
        dati_grezzi = f.readlines()
        for index, dato in enumerate(dati_grezzi):
            if index%6 != 0:
                valore = (float(dato.split('=')[1].strip(', \n')))
                dati_clean.append(valore)
                
    return dati_clean
    




