import streamlit as st
from auth import login_professor, verificar_acesso_professor
from student_form import main_student_form
from admin_dashboard import mostrar_dashboard_professor

# Configuração da página
st.set_page_config(
    page_title="Sistema de Avaliação entre Equipes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    /* Estilo geral */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header personalizado */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Botões personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Formulários */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e1e8ed;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #2c3e50 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 3px solid #667eea;
        color: #2c3e50 !important;
    }
    
    .stTabs [aria-selected="false"] {
        color: #2c3e50 !important;
    }
    
    /* Força cor preta em todos os elementos de texto das abas */
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] span {
        color: #2c3e50 !important;
    }
    
    /* Slider personalizado */
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Checkbox personalizado */
    .stCheckbox > div > div > div {
        background-color: #667eea;
    }
    
    /* Multi-select personalizado */
    .stMultiSelect > div > div > div > div {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
    }
    
    /* Success messages */
    .success-message {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Warning messages */
    .warning-message {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Error messages */
    .error-message {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Loading spinner */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .header-container {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Função principal da aplicação"""
    
    # Header principal
    st.markdown("""
    <div class="header-container">
        <h1 style="margin: 0; font-size: 2.5rem;">📊 Sistema de Avaliação entre Equipes</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Práticas Extensionistas V - Engenharia de Software
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sistema de login do professor
    login_professor()
    
    # Verificar se o professor está logado
    professor_logado = verificar_acesso_professor()
    
    if professor_logado:
        # Dashboard do professor
        mostrar_dashboard_professor()
    else:
        # Formulário para alunos
        main_student_form()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; padding: 1rem;">
        <p style="margin: 0;">
            📚 Sistema desenvolvido para Práticas Extensionistas V<br>
            🎓 Curso de Engenharia de Software<br>
            🔒 Todos os dados são tratados com confidencialidade
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
