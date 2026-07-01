import psycopg2

def conectar():

    conexao = psycopg2.connect(
        host="localhost",
        database="ai_finance",
        user="postgres",
        password="postgres123"
    )

    return conexao