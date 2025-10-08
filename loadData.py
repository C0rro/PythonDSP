import os

# Funzione per la lettura dei file presenti nella cartella Filtri
def get_files_name():
    folder = "Filtri"
    files = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(".txt")
    ]
    return files

# Funzione per caricare e formattare dati dal filtro
def loadData(filter_name):
    nome_file = "Filtri/" + filter_name 
    dati_clean = []
    with open(nome_file, "r") as f:
        dati_grezzi = f.readlines()
        for index, dato in enumerate(dati_grezzi):
            if index%6 != 0:
                valore = (float(dato.split('=')[1].strip(', \n')))
                dati_clean.append(valore)
                
    return dati_clean
    




