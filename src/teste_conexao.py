from conexao import conectar

try:
    conexao = conectar()
    print("✅ Conexão realizada com sucesso!")

    conexao.close()

except Exception as erro:
    print("Erro:", erro)