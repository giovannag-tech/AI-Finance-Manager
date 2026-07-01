import pandas as pd
from conexao import conectar


def inserir_meta(nome_meta, valor_meta):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO metas (nome_meta, valor_meta)
    VALUES (%s, %s)
    """

    cursor.execute(sql, (nome_meta, valor_meta))

    conexao.commit()
    cursor.close()
    conexao.close()


def listar_metas():
    conexao = conectar()

    sql = """
    SELECT id, nome_meta, valor_meta
    FROM metas
    ORDER BY id ASC
    """

    df = pd.read_sql(sql, conexao)

    conexao.close()

    return df


def excluir_meta(id_meta):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    DELETE FROM metas
    WHERE id = %s
    """

    cursor.execute(sql, (id_meta,))

    conexao.commit()
    cursor.close()
    conexao.close()