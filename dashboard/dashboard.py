import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from movimentacoes import listar_movimentacoes, excluir_movimentacao, atualizar_movimentacao


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def mostrar_dashboard():
    st.title("📊 Dashboard Financeiro")
    st.write("Análise geral das receitas, despesas e lucro.")

    df = listar_movimentacoes()

    if df.empty:
        st.warning("Nenhuma movimentação cadastrada ainda.")
        return

    df["data"] = pd.to_datetime(df["data"])
    df["mes"] = df["data"].dt.strftime("%Y-%m")
    df["valor"] = df["valor"].astype(float)

    st.sidebar.header("Filtros")

    meses = sorted(df["mes"].unique())
    mes_selecionado = st.sidebar.multiselect(
        "Selecione o mês:",
        meses,
        default=meses
    )

    categorias = sorted(df["categoria"].unique())
    categorias_selecionadas = st.sidebar.multiselect(
        "Selecione a categoria:",
        categorias,
        default=categorias
    )

    df_filtrado = df[
        (df["mes"].isin(mes_selecionado)) &
        (df["categoria"].isin(categorias_selecionadas))
    ]

    receitas = df_filtrado[df_filtrado["tipo"] == "Receita"]["valor"].sum()
    despesas = df_filtrado[df_filtrado["tipo"] == "Despesa"]["valor"].sum()
    lucro = receitas - despesas

    col1, col2, col3 = st.columns(3)

    col1.metric("Receitas", formatar_moeda(receitas))
    col2.metric("Despesas", formatar_moeda(despesas))
    col3.metric("Lucro", formatar_moeda(lucro))

    st.subheader("🧠 Análise Financeira Automática")

    if receitas == 0:
        st.warning("Ainda não há receitas suficientes para calcular a saúde financeira.")
    else:
        percentual_despesas = (despesas / receitas) * 100
        margem_lucro = (lucro / receitas) * 100

        if lucro > 0 and percentual_despesas <= 50:
            st.success(
                f"🟢 Situação saudável: suas despesas representam {percentual_despesas:.1f}% das receitas "
                f"e sua margem de lucro é de {margem_lucro:.1f}%."
            )

        elif lucro > 0 and percentual_despesas <= 80:
            st.warning(
                f"🟡 Atenção: suas despesas representam {percentual_despesas:.1f}% das receitas. "
                f"Ainda há lucro, mas os custos estão altos."
            )

        else:
            st.error(
                f"🔴 Alerta: suas despesas representam {percentual_despesas:.1f}% das receitas. "
                f"O negócio está com lucro baixo ou prejuízo."
            )

    st.subheader("🔔 Alertas Inteligentes")

    df_despesas = df_filtrado[df_filtrado["tipo"] == "Despesa"]
    df_receitas = df_filtrado[df_filtrado["tipo"] == "Receita"]

    if lucro > 0:
        st.success(f"✅ Você está com lucro positivo de {formatar_moeda(lucro)}.")
    elif lucro == 0:
        st.warning("⚠️ Suas receitas e despesas estão empatadas.")
    else:
        st.error(f"🚨 Você está no prejuízo de {formatar_moeda(abs(lucro))}.")

    if receitas > 0:
        percentual_despesas = (despesas / receitas) * 100

        if percentual_despesas > 80:
            st.error("🚨 Suas despesas estão muito altas em relação às receitas.")
        elif percentual_despesas > 50:
            st.warning("⚠️ Suas despesas já passaram de 50% das receitas.")
        else:
            st.success("✅ Suas despesas estão em um nível controlado.")

    if not df_despesas.empty:
        gastos_categoria = df_despesas.groupby("categoria")["valor"].sum()
        maior_categoria = gastos_categoria.idxmax()
        maior_valor = gastos_categoria.max()

        st.info(
            f"📌 Sua maior categoria de despesa é **{maior_categoria}**, "
            f"com total de {formatar_moeda(maior_valor)}."
        )

    if not df_receitas.empty:
        receitas_categoria = df_receitas.groupby("categoria")["valor"].sum()
        maior_receita = receitas_categoria.idxmax()
        maior_receita_valor = receitas_categoria.max()

        st.info(
            f"💰 Sua maior fonte de receita é **{maior_receita}**, "
            f"com total de {formatar_moeda(maior_receita_valor)}."
        )

    st.divider()

    resumo_mensal = df_filtrado.groupby(["mes", "tipo"])["valor"].sum().reset_index()

    grafico_mensal = px.bar(
        resumo_mensal,
        x="mes",
        y="valor",
        color="tipo",
        barmode="group",
        title="Receitas x Despesas por mês"
    )

    st.plotly_chart(grafico_mensal, use_container_width=True)

    df_fluxo = df_filtrado.copy()
    df_fluxo["valor_fluxo"] = df_fluxo.apply(
        lambda linha: linha["valor"] if linha["tipo"] == "Receita" else -linha["valor"],
        axis=1
    )

    fluxo_diario = df_fluxo.groupby("data")["valor_fluxo"].sum().reset_index()
    fluxo_diario["saldo_acumulado"] = fluxo_diario["valor_fluxo"].cumsum()

    grafico_fluxo = px.line(
        fluxo_diario,
        x="data",
        y="saldo_acumulado",
        markers=True,
        title="Fluxo de caixa acumulado"
    )

    st.plotly_chart(grafico_fluxo, use_container_width=True)

    despesas_categoria = (
        df_filtrado[df_filtrado["tipo"] == "Despesa"]
        .groupby("categoria")["valor"]
        .sum()
        .reset_index()
    )

    if not despesas_categoria.empty:
        grafico_categoria = px.pie(
            despesas_categoria,
            names="categoria",
            values="valor",
            title="Despesas por categoria"
        )

        st.plotly_chart(grafico_categoria, use_container_width=True)

    st.subheader("💳 Movimentações cadastradas")

    for _, linha in df_filtrado.iterrows():

        icone = "💰" if linha["tipo"] == "Receita" else "💸"

        with st.expander(
            f"{icone} {linha['tipo']} | {linha['categoria']} | {formatar_moeda(float(linha['valor']))} | {linha['data'].strftime('%d/%m/%Y')}"
        ):

            col_info, col_edicao = st.columns([1, 2])

            with col_info:
                st.markdown(f"### {icone} {linha['tipo']}")
                st.write(f"**Categoria:** {linha['categoria']}")
                st.write(f"**Descrição:** {linha['descricao']}")
                st.write(f"**Valor:** {formatar_moeda(float(linha['valor']))}")
                st.write(f"**Data:** {linha['data'].strftime('%d/%m/%Y')}")
                st.write(f"**Forma de pagamento:** {linha['forma_pagamento']}")

            with col_edicao:
                nova_data = st.date_input(
                    "Data",
                    value=linha["data"],
                    key=f"data_{linha['id']}"
                )

                novo_tipo = st.selectbox(
                    "Tipo",
                    ["Receita", "Despesa"],
                    index=0 if linha["tipo"] == "Receita" else 1,
                    key=f"tipo_{linha['id']}"
                )

                nova_categoria = st.text_input(
                    "Categoria",
                    value=linha["categoria"],
                    key=f"categoria_{linha['id']}"
                )

                nova_descricao = st.text_area(
                    "Descrição",
                    value=linha["descricao"],
                    key=f"descricao_{linha['id']}"
                )

                novo_valor = st.number_input(
                    "Valor",
                    min_value=0.0,
                    value=float(linha["valor"]),
                    step=10.0,
                    key=f"valor_{linha['id']}"
                )

                nova_forma = st.selectbox(
                    "Forma de pagamento",
                    ["Pix", "Boleto", "Cartão", "Transferência", "Dinheiro"],
                    index=["Pix", "Boleto", "Cartão", "Transferência", "Dinheiro"].index(linha["forma_pagamento"]),
                    key=f"forma_{linha['id']}"
                )

                col_editar, col_excluir = st.columns(2)

                if col_editar.button("✏️ Salvar edição", key=f"editar_{linha['id']}"):
                    atualizar_movimentacao(
                        linha["id"],
                        nova_data,
                        novo_tipo,
                        nova_categoria,
                        nova_descricao,
                        novo_valor,
                        nova_forma
                    )

                    st.success("Movimentação atualizada com sucesso!")
                    st.rerun()

                if col_excluir.button("🗑️ Excluir", key=f"excluir_{linha['id']}"):
                    excluir_movimentacao(linha["id"])
                    st.success("Movimentação excluída com sucesso!")
                    st.rerun()