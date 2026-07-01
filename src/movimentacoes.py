import pandas as pd
from conexao import conectar


def inserir_movimentacao(data, tipo, categoria, descricao, valor, forma_pagamento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO movimentacoes
    (data, tipo, categoria, descricao, valor, forma_pagamento)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        data,
        tipo,
        categoria,
        descricao,
        valor,
        forma_pagamento
    ))

    conexao.commit()
    cursor.close()
    conexao.close()


def listar_movimentacoes():
    conexao = conectar()

    sql = """
    SELECT
        id,
        data,
        tipo,
        categoria,
        descricao,
        valor,
        forma_pagamento
    FROM movimentacoes
    ORDER BY data ASC
    """

    df = pd.read_sql(sql, conexao)

    conexao.close()

    return df


def excluir_movimentacao(id_movimentacao):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    DELETE FROM movimentacoes
    WHERE id = %s
    """

    cursor.execute(sql, (id_movimentacao,))

    conexao.commit()
    cursor.close()
    conexao.close()


def atualizar_movimentacao(id_movimentacao, data, tipo, categoria, descricao, valor, forma_pagamento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE movimentacoes
    SET
        data = %s,
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