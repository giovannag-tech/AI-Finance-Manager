import streamlit as st
from style import aplicar_estilo

st.set_page_config(
    page_title="Gerente de Finanças com IA",
    page_icon="💰",
    layout="wide"
)
aplicar_estilo()

if "logado" not in st.session_state:
    st.session_state.logado = False


def tela_login():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("# 💰 Gerente de Finanças com IA")
        st.write("Acesse seu painel financeiro inteligente.")

        with st.container(border=True):
            st.subheader("🔐 Login")

            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")

            if st.button("Entrar", use_container_width=True):
                if email == "admin@email.com" and senha == "123456":
                    st.session_state.logado = True
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Email ou senha inválidos.")

        st.info("Usuário de teste: admin@email.com | Senha: 123456")


if not st.session_state.logado:
    tela_login()

else:
    st.sidebar.title("💰 Gerente de Finanças com IA")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    pagina = st.sidebar.radio(
        "Cardápio",
        [
            "Dashboard",
            "Nova Movimentação",
            "Relatórios",
            "Assistente IA",
            "Metas",
            "Previsoes"
        ]
    )

    if pagina == "Dashboard":
        from dashboard import mostrar_dashboard
        mostrar_dashboard()

    elif pagina == "Nova Movimentação":
        from cadastro import mostrar_cadastro
        mostrar_cadastro()

    elif pagina == "Relatórios":
        from relatorios import mostrar_relatorios
        mostrar_relatorios()

    elif pagina == "Assistente IA":
        from assistente_ia import mostrar_assistente
        mostrar_assistente()

    elif pagina == "Metas":
        from metas import mostrar_metas
        mostrar_metas()

    elif pagina == "Previsoes":
         from previsoes import mostrar_previsoes
         mostrar_previsoes()    