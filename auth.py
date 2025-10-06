import streamlit as st
import bcrypt

def login_professor():
    """Interface de login para o professor"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Login Professor")
    
    if 'professor_logado' not in st.session_state:
        st.session_state.professor_logado = False
    
    if not st.session_state.professor_logado:
        with st.sidebar:
            # Inicializar variáveis de controle
            if 'login_attempted' not in st.session_state:
                st.session_state.login_attempted = False
            
            # CSS específico para esconder apenas a mensagem do formulário
            st.markdown("""
            <style>
            /* Esconder apenas a mensagem "Press Enter to submit form" */
            .stForm > div > div > div > div > p {
                display: none !important;
            }
            
            /* Esconder texto de ajuda do formulário sem afetar botões */
            .stForm .stMarkdown:not(.stButton .stMarkdown) p {
                display: none !important;
            }
            
            /* Garantir que botões não sejam afetados */
            .stButton .stMarkdown p {
                display: block !important;
            }
            
            .stButton button {
                color: white !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Formulário que detecta Enter automaticamente
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("Usuário", key="prof_username", placeholder="Digite seu usuário")
                password = st.text_input("Senha", type="password", key="prof_password", placeholder="Digite sua senha")
                
                # Botão de submit que funciona com Enter
                submitted = st.form_submit_button("Entrar", type="primary", width='stretch')
                
                # Processar login quando formulário for submetido (Enter ou clique)
                if submitted:
                    from database import DatabaseManager
                    db = DatabaseManager()
                    
                    if db.verificar_login_professor(username, password):
                        st.session_state.professor_logado = True
                        st.session_state.username = username
                        st.session_state.login_attempted = False
                        st.rerun()
                    else:
                        st.session_state.login_attempted = True
            
            # Mostrar erro se login falhou
            if st.session_state.get('login_attempted', False):
                st.error("Usuário ou senha incorretos!")
    else:
        st.sidebar.success(f"👋 Bem-vindo, Professor!")
        if st.sidebar.button("Sair", key="logout_btn"):
            st.session_state.professor_logado = False
            st.session_state.username = None
            st.rerun()

def verificar_acesso_professor():
    """Verifica se o professor está logado"""
    return st.session_state.get('professor_logado', False)
