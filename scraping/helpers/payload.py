def escolas(row):
    return {
    'id': row[0],
    'geom': row[1],
    'nome': row[2],
    'cnpj': row[3],
    'email': row[4],
    'telefone': row[5]
}