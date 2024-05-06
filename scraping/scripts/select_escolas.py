from databases.postgis_handler import PostgisHandler
from helpers.payload import escolas

def select_table_escolas():
    print("Inciando banco!")
    with PostgisHandler() as db:
        query = "SELECT * FROM main.escolas"
        resultados = db.select(query)
   
    lista = []
    for resultado in resultados:
        dicionario = escolas(resultado)
        lista.append(dicionario)
    
    print(lista)