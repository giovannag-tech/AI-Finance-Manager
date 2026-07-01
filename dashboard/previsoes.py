import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from sklearn.linear_model import LinearRegression

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from movimentacoes import listar_movimentacoes


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def mostrar_previsoes():
    st.title("📈 Previsões Financeiras")
    st.write("Previsão simples de receita usando Machine Learning.")

    df = listar_movimentacoes()

    if df.empty:
        st.warning("Nenhuma movimentação cadastrada ainda.")
        return

    df["data"] = pd.to_datetime(df["data"])
    df["valor"] = df["valor"].astype(float)

    receitas = df[df["tipo"] == "Receita"].copy()

    if receitas.empty:
        st.warning("Cadastre receitas para gerar uma previsão.")
        return

    receitas["mes"] = receitas["data"].dt.to_period("M").astype(str)
    receitas["mes_numero"] = range(1, len(receitas) + 1)

    resumo = receitas.groupby("mes")["valor"].sum().reset_index()
    resumo["mes_numero"] = range(1, len(resumo) + 1)

    if len(resumo) < 3:
        st.warning("Cadastre receitas em pelo menos 3 meses diferentes para gerar uma previsão.")
        return

    X = resumo[["mes_numero"]]
    y = resumo["valor"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    proximo_mes_numero = resumo["mes_numero"].max() + 1
    previsao = modelo.predict([[proximo_mes_numero]])[0]

    st.metric("Receita prevista para o próximo mês", formatar_moeda(previsao))

    resumo_grafico = resumo.copy()
    resumo_grafico["tipo"] = "Receita Real"

    previsao_df = pd.DataFrame({
        "mes": ["Próximo mês"],
        "valor": [previsao],
        "mes_numero": [proximo_mes_numero],
        "tipo": ["Previsão"]
    })

    dados_grafico = pd.concat([resumo_grafico, previsao_df], ignore_index=True)

    grafico = px.line(
        dados_grafico,
        x="mes",
        y="valor",
        color="tipo",
        markers=True,
        title="Receitas reais x previsão"
    )

    st.plotly_chart(grafico, use_container_width=True)

    st.subheader("Dados usados no modelo")
    st.dataframe(resumo)

    st.info(
        "Esta previsão usa regressão linear simples. "
        "O objetivo é demonstrar Machine Learning aplicado a dados financeiros."
    )