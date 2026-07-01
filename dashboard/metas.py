import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from movimentacoes import listar_movimentacoes
from metas_db import inserir_meta, listar_metas, excluir_meta


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def mostrar_metas():
    st.title("🎯 Metas Financeiras")
    st.write("Acompanhe seus objetivos financeiros com base no lucro atual.")

    df_mov = listar_movimentacoes()

    if df_mov.empty:
        st.warning("Cadastre movimentações antes de criar metas.")
        return

    receitas = df_mov[df_mov["tipo"] == "Receita"]["valor"].sum()
    despesas = df_mov[df_mov["tipo"] == "Despesa"]["valor"].sum()
    lucro = receitas - despesas

    st.metric("Lucro atual disponível", formatar_moeda(lucro))

    st.subheader("Criar nova meta")

    nome_meta = st.text_input("Nome da meta")
    valor_meta = st.number_input("Valor da meta", min_value=0.0, step=100.0)

    if st.button("Salvar meta"):
        if nome_meta.strip() == "":
            st.warning("Digite o nome da meta.")
        elif valor_meta <= 0:
            st.warning("Digite um valor válido.")
        else:
            inserir_meta(nome_meta, valor_meta)
            st.success("Meta salva com sucesso!")
            st.rerun()

    st.divider()

    st.subheader("Minhas metas")

    df_metas = listar_metas()

    if df_metas.empty:
        st.info("Nenhuma meta cadastrada ainda.")
        return

    for _, meta in df_metas.iterrows():
        progresso = min((lucro / float(meta["valor_meta"])) * 100, 100)
        falta = max(float(meta["valor_meta"]) - lucro, 0)

        with st.expander(f"🎯 {meta['nome_meta']}"):
            st.progress(int(progresso))

            st.write(f"**Meta:** {formatar_moeda(float(meta['valor_meta']))}")
            st.write(f"**Lucro atual:** {formatar_moeda(lucro)}")
            st.write(f"**Progresso:** {progresso:.1f}%")
            st.write(f"**Falta:** {formatar_moeda(falta)}")

            if st.button("🗑️ Excluir meta", key=f"excluir_meta_{meta['id']}"):
                excluir_meta(meta["id"])
                st.success("Meta excluída com sucesso!")
                st.rerun()