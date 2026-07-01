import streamlit as st
import sys
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from movimentacoes import listar_movimentacoes


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_pdf(df):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    largura, altura = A4
    y = altura - 50

    receitas = df[df["tipo"] == "Receita"]["valor"].sum()
    despesas = df[df["tipo"] == "Despesa"]["valor"].sum()
    lucro = receitas - despesas

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Relatorio Financeiro")
    y -= 40

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Receitas: {formatar_moeda(receitas)}")
    y -= 20
    pdf.drawString(50, y, f"Despesas: {formatar_moeda(despesas)}")
    y -= 20
    pdf.drawString(50, y, f"Lucro: {formatar_moeda(lucro)}")
    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Movimentacoes")
    y -= 25

    pdf.setFont("Helvetica", 9)

    for _, linha in df.iterrows():
        texto = (
            f"{linha['data']} | {linha['tipo']} | {linha['categoria']} | "
            f"{formatar_moeda(float(linha['valor']))}"
        )

        pdf.drawString(50, y, texto)
        y -= 18

        if y < 60:
            pdf.showPage()
            y = altura - 50
            pdf.setFont("Helvetica", 9)

    pdf.save()
    buffer.seek(0)

    return buffer


def mostrar_relatorios():
    st.title("📄 Relatórios")
    st.write("Exporte suas movimentações financeiras.")

    df = listar_movimentacoes()

    if df.empty:
        st.warning("Nenhuma movimentação cadastrada ainda.")
        return

    df["valor"] = df["valor"].astype(float)

    st.subheader("Resumo financeiro")

    receitas = df[df["tipo"] == "Receita"]["valor"].sum()
    despesas = df[df["tipo"] == "Despesa"]["valor"].sum()
    lucro = receitas - despesas

    col1, col2, col3 = st.columns(3)
    col1.metric("Receitas", formatar_moeda(receitas))
    col2.metric("Despesas", formatar_moeda(despesas))
    col3.metric("Lucro", formatar_moeda(lucro))

    st.subheader("Prévia dos dados")
    st.dataframe(df)

    arquivo_excel = BytesIO()
    df.to_excel(arquivo_excel, index=False, engine="openpyxl")
    arquivo_excel.seek(0)

    st.download_button(
        label="⬇️ Baixar relatório em Excel",
        data=arquivo_excel,
        file_name="relatorio_financeiro.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    arquivo_pdf = gerar_pdf(df)

    st.download_button(
        label="⬇️ Baixar relatório em PDF",
        data=arquivo_pdf,
        file_name="relatorio_financeiro.pdf",
        mime="application/pdf"
    )