import streamlit as st
from datetime import date
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from movimentacoes import inserir_movimentacao


def mostrar_cadastro():

    st.title("💵 Nova Movimentação")
    st.write("Cadastre receitas e despesas no sistema.")

    with st.container(border=True):

        with st.form("form_movimentacao"):

            col1, col2 = st.columns(2)

            with col1:
                data = st.date_input("Data", value=date.today())

                tipo = st.selectbox(
                    "Tipo",
                    ["Receita", "Despesa"]
                )

                if tipo == "Receita":
                    categoria = st.selectbox(
                        "Categoria",
                        ["Freelance", "Salário", "Vendas", "Serviços", "Investimentos", "Outros"]
                    )
                else:
                    categoria = st.selectbox(
                        "Categoria",
                        ["Aluguel", "Marketing", "Fornecedores", "Salários", "Transporte", "Alimentação", "Impostos", "Serviços", "Outros"]
                    )

            with col2:
                valor = st.number_input(
                    "Valor",
                    min_value=0.0,
                    step=10.0
                )

                forma_pagamento = st.selectbox(
                    "Forma de pagamento",
                    ["Pix", "Boleto", "Cartão", "Transferência", "Dinheiro"]
                )

            descricao = st.text_area("Descrição")

            salvar = st.form_submit_button("Salvar movimentação", use_container_width=True)

            if salvar:
                if valor <= 0:
                    st.warning("Digite um valor maior que zero.")
                elif descricao.strip() == "":
                    st.warning("Digite uma descrição para a movimentação.")
                else:
                    inserir_movimentacao(
                        data,
                        tipo,
                        categoria,
                        descricao,
                        valor,
                        forma_pagamento
                    )

                    st.success("✅ Movimentação salva com sucesso no banco de dados!")