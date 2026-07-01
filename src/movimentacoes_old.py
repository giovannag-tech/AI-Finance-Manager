def atualizar_movimentacao(id_movimentacao, data, tipo, categoria, descricao, valor, forma_pagamento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE movimentacoes
    SET data = %s,
        tipo = %s,
        categoria = %s,
        descricao = %s,
        valor = %s,
        forma_pagamento = %s
    WHERE id = %s
    """

    cursor.execute(sql, (
        data,
        tipo,
        categoria,
        descricao,
        valor,
        forma_pagamento,
        id_movimentacao
    ))

    conexao.commit()
    cursor.close()
    conexao.close()