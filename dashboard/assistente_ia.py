import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from movimentacoes import listar_movimentacoes


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def responder_pergunta(pergunta, df):
    pergunta = pergunta.lower()

    receitas = df[df["tipo"] == "Receita"]["valor"].sum()
    despesas = df[df["tipo"] == "Despesa"]["valor"].sum()
    lucro = receitas - despesas

    df_despesas = df[df["tipo"] == "Despesa"]
    df_receitas = df[df["tipo"] == "Receita"]

    if "lucro" in pergunta:
        return f"Seu lucro total é de {formatar_moeda(lucro)}."

    if "receita" in pergunta or "ganhei" in pergunta or "entrada" in pergunta:
        return f"Sua receita total é de {formatar_moeda(receitas)}."

    if "despesa" in pergunta or "gastei" in pergunta or "gasto" in pergunta:
        return f"Suas despesas totais são de {formatar_moeda(despesas)}."

    if "maior despesa" in pergunta or "mais gastei" in pergunta:
        if df_despesas.empty:
            return "Você ainda não possui despesas cadastradas."

        resumo = df_despesas.groupby("categoria")["valor"].sum()
        categoria = resumo.idxmax()
        valor = resumo.max()

        return f"Sua maior despesa foi com {categoria}, totalizando {formatar_moeda(valor)}."

    if "maior receita" in pergunta or "mais ganhei" in pergunta:
        if df_receitas.empty:
            return "Você ainda não possui receitas cadastradas."

        resumo = df_receitas.groupby("categoria")["valor"].sum()
        categoria = resumo.idxmax()
        valor = resumo.max()

        return f"Sua maior receita foi em {categoria}, totalizando {formatar_moeda(valor)}."

    if "marketing" in pergunta:
        total = df[df["categoria"].str.lower() == "marketing"]["valor"].sum()
        return f"Você gastou {formatar_moeda(total)} com Marketing."

    if "saúde financeira" in pergunta or "situacao" in pergunta or "situação" in pergunta:
        if receitas == 0:
            return "Ainda não há receitas suficientes para avaliar sua saúde financeira."

        percentual_despesas = (despesas / receitas) * 100

        if lucro > 0 and percentual_despesas <= 50:
            return f"Sua situação financeira está saudável. As despesas representam {percentual_despesas:.1f}% das receitas."

        if lucro > 0 and percentual_despesas <= 80:
            return f"Sua situação exige atenção. As despesas representam {percentual_despesas:.1f}% das receitas."

        return f"Alerta financeiro: suas despesas representam {percentual_despesas:.1f}% das receitas."

    if "resumo" in pergunta:
        return (
            f"Resumo financeiro: receitas de {formatar_moeda(receitas)}, "
            f"despesas de {formatar_moeda(despesas)} e lucro de {formatar_moeda(lucro)}."
        )

    return (
        "Ainda não sei responder essa pergunta. "
        "Tente perguntar sobre lucro, receita, despesas, marketing, maior despesa, maior receita, resumo ou saúde financeira."
    )


def mostrar_assistente():
    st.title("🤖 Assistente Financeiro IA")
    st.write("Faça perguntas sobre os dados financeiros cadastrados no sistema.")

    df = listar_movimentacoes()

    if df.empty:
        st.warning("Nenhuma movimentação cadastrada ainda.")
        return

    df["valor"] = df["valor"].astype(float)

    pergunta = st.text_input("Digite sua pergunta:")

    if st.button("Perguntar"):
        if pergunta.strip() == "":
            st.warning("Digite uma pergunta antes de continuar.")
        else:
            resposta = responder_pergunta(pergunta, df)
            st.success(resposta)

    st.divider()

    st.subheader("💡 Perguntas que você pode testar")
    st.write("- Qual foi meu lucro?")
    st.write("- Quanto tive de receita?")
    st.write("- Quanto gastei?")
    st.write("- Qual minha maior despesa?")
    st.write("- Qual minha maior receita?")
    st.write("- Quanto gastei com marketing?")
    st.write("- Como está minha saúde financeira?")
    st.write("- Me dê um resumo financeiro.")