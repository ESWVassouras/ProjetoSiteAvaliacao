import streamlit as st
from database import DatabaseManager, ALUNOS
from utils import gerar_comprovante

def mostrar_formulario_avaliacao():
    """Interface principal do formulário de avaliação para alunos"""
    
    # Título principal
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <div style="background-color: #ecf0f1; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <p style="font-size: 16px; line-height: 1.6; color: #34495e;">
                Este formulário tem como objetivo promover uma avaliação justa e reflexiva entre os membros das equipes do componente curricular <strong>Práticas Extensionistas V</strong>, do curso de Engenharia de Software.
            </p>
            <p style="font-size: 16px; line-height: 1.6; color: #34495e;">
                Cada aluno deverá avaliar individualmente os colegas de equipe, atribuindo uma pontuação de 0 a 2 para cada critério proposto, conforme sua percepção sobre o desempenho, comprometimento e colaboração de cada membro durante o projeto.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sistema de pontuação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #e74c3c; color: white; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; color: white;">🔴 0 Pontos</h3>
            <p style="margin: 5px 0 0 0; font-size: 14px;">Não contribuiu / desempenho insatisfatório</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f39c12; color: white; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; color: white;">🟡 1 Ponto</h3>
            <p style="margin: 5px 0 0 0; font-size: 14px;">Contribuiu parcialmente / desempenho razoável</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #27ae60; color: white; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; color: white;">🟢 2 Pontos</h3>
            <p style="margin: 5px 0 0 0; font-size: 14px;">Contribuiu plenamente / desempenho excelente</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Aviso importante
    st.markdown("""
    <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin: 20px 0;">
        <h4 style="color: #856404; margin-top: 0;">⚠️ Atenção:</h4>
        <ul style="color: #856404; margin-bottom: 0;">
            <li>Seja honesto e responsável em suas respostas.</li>
            <li>As respostas serão confidenciais e utilizadas apenas para fins avaliativos internos.</li>
            <li>Avalie cada membro da equipe <strong>(exceto você mesmo)</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Seção de seleção de equipe (fora do form)
    st.markdown("### 🏢 Seleção de Equipe")
    
    # Campo para selecionar equipe existente ou cadastrar nova
    from database import DatabaseManager
    db = DatabaseManager()
    equipes_existentes = db.listar_todas_equipes()
    
    # Se não há equipes cadastradas, inicializar com lista vazia
    if not equipes_existentes:
        equipes_existentes = []
    
    # Campo de seleção de equipes existentes
    if equipes_existentes:
        st.markdown("**Equipes que já foram cadastradas - Selecione:**")
        
        equipe_selecionada = st.selectbox(
            "Escolha sua equipe:",
            options=[""] + equipes_existentes,
            key="equipe_selectbox",
            help="Selecione sua equipe da lista ou escolha 'Cadastrar nova equipe' abaixo",
            index=0
        )
        
        # Se uma equipe foi selecionada, definir como nome_equipe
        if equipe_selecionada:
            nome_equipe = equipe_selecionada
        else:
            nome_equipe = ""
    else:
        st.info("📭 Nenhuma equipe foi cadastrada ainda. Cadastre a primeira equipe abaixo!")
        nome_equipe = ""
    
    # Botão para cadastrar nova equipe
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🆕 Cadastrar nova equipe", type="primary", width='stretch'):
            st.session_state.cadastrar_nova_equipe = True
            st.rerun()
    
    # Formulário para nova equipe (aparece quando botão é clicado)
    if st.session_state.get('cadastrar_nova_equipe', False):
        st.markdown("---")
        st.markdown("### ✏️ Cadastrar Nova Equipe")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            nome_nova_equipe = st.text_input(
                "Nome da nova equipe/projeto:",
                placeholder="Digite o nome da nova equipe",
                key="nova_equipe_input"
            )
        
        with col2:
            st.markdown("")  # Espaçamento
            st.markdown("")  # Espaçamento
            
            col2_1, col2_2 = st.columns(2)
            
            with col2_1:
                if st.button("✅ Confirmar", type="primary", width='stretch'):
                    if nome_nova_equipe and nome_nova_equipe.strip():
                        # Salvar nova equipe
                        db.salvar_equipe(nome_nova_equipe.strip())
                        st.session_state.nova_equipe_cadastrada = nome_nova_equipe.strip()
                        st.session_state.cadastrar_nova_equipe = False
                        st.success(f"✅ Equipe '{nome_nova_equipe.strip()}' cadastrada com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Por favor, digite um nome para a equipe!")
            
            with col2_2:
                if st.button("❌ Cancelar", type="secondary", width='stretch'):
                    st.session_state.cadastrar_nova_equipe = False
                    st.rerun()
        
        # Se uma nova equipe foi cadastrada, usar ela
        if st.session_state.get('nova_equipe_cadastrada'):
            nome_equipe = st.session_state.nova_equipe_cadastrada
            del st.session_state.nova_equipe_cadastrada
    
    # Validação: verificar se uma equipe foi selecionada
    if not nome_equipe or nome_equipe == "":
        st.warning("⚠️ Por favor, selecione uma equipe existente ou cadastre uma nova equipe para continuar.")
        return
    
    # Mostrar equipe selecionada
    st.success(f"✅ Equipe selecionada: **{nome_equipe}**")
    
    st.markdown("---")
    
    # Formulário principal
    with st.form("formulario_avaliacao"):
        st.markdown("### 📝 Dados do Avaliador")
        
        col1, col2 = st.columns(2)
        
        with col1:
            avaliador_nome = st.text_input(
                "Seu nome completo:",
                placeholder="Digite seu nome completo",
                help="Seu nome como consta na lista da turma"
            )
        
        with col2:
            avaliador_matricula = st.text_input(
                "Sua matrícula:",
                placeholder="Digite sua matrícula",
                help="Número da sua matrícula acadêmica"
            )
        
        
        st.markdown("### 👥 Selecione os colegas de equipe para avaliar")
        st.markdown("*Selecione todos os membros da sua equipe (exceto você mesmo):*")
        
        # Lista de alunos para seleção
        colegas_selecionados = st.multiselect(
            "Colegas de equipe:",
            options=ALUNOS,
            default=[],
            help="Selecione todos os membros da sua equipe que você deseja avaliar"
        )
        
        # Verificar se o avaliador não está na lista de colegas
        if avaliador_nome and avaliador_nome in colegas_selecionados:
            st.warning("⚠️ Você não pode se avaliar! Remova seu nome da lista de colegas selecionados.")
            return
        
        submitted = st.form_submit_button("Continuar para Avaliações", type="primary")
        
        if submitted:
            # Validações
            if not avaliador_nome or not avaliador_matricula or not nome_equipe:
                st.error("❌ Por favor, preencha todos os campos obrigatórios!")
                return
            
            if not colegas_selecionados:
                st.error("❌ Por favor, selecione pelo menos um colega para avaliar!")
                return
            
            if avaliador_nome in colegas_selecionados:
                st.error("❌ Você não pode se avaliar! Remova seu nome da lista de colegas selecionados.")
                return
            
            # Salvar dados na sessão
            st.session_state.formulario_dados = {
                'avaliador_nome': avaliador_nome,
                'avaliador_matricula': avaliador_matricula,
                'nome_equipe': nome_equipe,
                'colegas_selecionados': colegas_selecionados
            }
            st.session_state.etapa_atual = 'avaliacoes'
            st.rerun()

def mostrar_avaliacoes():
    """Interface para preenchimento das avaliações individuais"""
    
    if 'formulario_dados' not in st.session_state:
        st.error("❌ Dados do formulário não encontrados. Por favor, volte ao início.")
        return
    
    dados = st.session_state.formulario_dados
    colegas = dados['colegas_selecionados']
    
    # Header
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: #2c3e50;">📊 Avaliações Individuais</h2>
        <p style="color: #7f8c8d; font-size: 16px;">
            <strong>Avaliador:</strong> {dados['avaliador_nome']} | 
            <strong>Equipe:</strong> {dados['nome_equipe']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulário de avaliações
    with st.form("avaliacoes_form"):
        avaliacoes = {}
        
        for i, colega in enumerate(colegas):
            st.markdown(f"### 👤 Avaliando: {colega}")
            
            # Pontuação
            pontuacao = st.slider(
                f"Arraste aqui para pontuar {colega.split()[0]}:",
                min_value=0,
                max_value=2,
                value=0,
                key=f"pontuacao_{i}",
                help="0 = Não contribuiu / 1 = Contribuiu parcialmente / 2 = Contribuiu plenamente"
            )
            
            # Critérios
            st.markdown("**Critérios considerados para esta pontuação:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                comprometimento = st.checkbox(
                    "Comprometimento e responsabilidade",
                    key=f"comp_{i}",
                    help="Comparecimento às reuniões, cumprimento de prazos, envolvimento com o projeto"
                )
                
                trabalho_equipe = st.checkbox(
                    "Trabalho em equipe e colaboração",
                    key=f"trab_{i}",
                    help="Comunicação, respeito às ideias do grupo, apoio aos colegas"
                )
                
                qualidade_entregas = st.checkbox(
                    "Qualidade das entregas e contribuições técnicas",
                    key=f"qual_{i}",
                    help="Qualidade e relevância das tarefas realizadas"
                )
            
            with col2:
                proatividade = st.checkbox(
                    "Proatividade e iniciativa",
                    key=f"proa_{i}",
                    help="Participação ativa, busca de soluções, contribuição além do mínimo esperado"
                )
                
                cumprimento_responsabilidades = st.checkbox(
                    "Cumprimento de responsabilidades específicas",
                    key=f"resp_{i}",
                    help="Execução das tarefas que lhe foram designadas"
                )
            
            # Comentário opcional
            comentario = st.text_area(
                f"Comentário sobre {colega.split()[0]} (opcional):",
                placeholder="Deixe aqui comentários adicionais sobre o desempenho deste colega...",
                key=f"coment_{i}",
                height=100
            )
            
            # Salvar avaliação
            avaliacoes[colega] = {
                'pontuacao': pontuacao,
                'comprometimento': comprometimento,
                'trabalho_equipe': trabalho_equipe,
                'qualidade_entregas': qualidade_entregas,
                'proatividade': proatividade,
                'cumprimento_responsabilidades': cumprimento_responsabilidades,
                'comentario': comentario
            }
            
            st.markdown("---")
        
        # Botão de envio
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.form_submit_button("🚀 Enviar Formulário", type="primary", width='stretch'):
                # Validar se pelo menos um critério foi selecionado para cada avaliação
                validacao_ok = True
                for colega, aval in avaliacoes.items():
                    criterios_selecionados = sum([
                        aval['comprometimento'],
                        aval['trabalho_equipe'],
                        aval['qualidade_entregas'],
                        aval['proatividade'],
                        aval['cumprimento_responsabilidades']
                    ])
                    
                    if criterios_selecionados == 0:
                        st.error(f"❌ Selecione pelo menos um critério para {colega}")
                        validacao_ok = False
                
                if validacao_ok:
                    # Salvar no banco de dados
                    db = DatabaseManager()
                    
                    try:
                        for colega, aval in avaliacoes.items():
                            dados_avaliacao = {
                                'avaliador_nome': dados['avaliador_nome'],
                                'avaliador_matricula': dados['avaliador_matricula'],
                                'nome_equipe': dados['nome_equipe'],
                                'avaliado_nome': colega,
                                'pontuacao': aval['pontuacao'],
                                'comprometimento': aval['comprometimento'],
                                'trabalho_equipe': aval['trabalho_equipe'],
                                'qualidade_entregas': aval['qualidade_entregas'],
                                'proatividade': aval['proatividade'],
                                'cumprimento_responsabilidades': aval['cumprimento_responsabilidades'],
                                'comentario': aval['comentario']
                            }
                            
                            db.salvar_avaliacao(dados_avaliacao)
                        
                        # Salvar dados para comprovante
                        st.session_state.avaliacoes_realizadas = [
                            {
                                'avaliado_nome': colega,
                                'pontuacao': aval['pontuacao'],
                                'comprometimento': aval['comprometimento'],
                                'trabalho_equipe': aval['trabalho_equipe'],
                                'qualidade_entregas': aval['qualidade_entregas'],
                                'proatividade': aval['proatividade'],
                                'cumprimento_responsabilidades': aval['cumprimento_responsabilidades'],
                                'comentario': aval['comentario']
                            }
                            for colega, aval in avaliacoes.items()
                        ]
                        
                        st.session_state.etapa_atual = 'sucesso'
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao salvar avaliações: {str(e)}")
    
    # Botão para voltar
    if st.button("← Voltar"):
        st.session_state.etapa_atual = 'formulario'
        st.rerun()

def mostrar_sucesso():
    """Interface de sucesso após envio"""
    
    if 'formulario_dados' not in st.session_state or 'avaliacoes_realizadas' not in st.session_state:
        st.error("❌ Dados não encontrados.")
        return
    
    dados = st.session_state.formulario_dados
    avaliacoes = st.session_state.avaliacoes_realizadas
    
    # Mensagem de sucesso
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; color: white; margin-bottom: 30px;">
        <h1 style="color: white; margin-bottom: 20px;">🎉 Formulário Enviado com Sucesso!</h1>
        <p style="font-size: 18px; margin-bottom: 0;">
            Suas avaliações foram registradas de forma segura e anônima.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mensagem tranquilizadora
    st.markdown("""
    <div style="background-color: #d5f4e6; border: 2px solid #27ae60; border-radius: 15px; 
                padding: 25px; margin: 20px 0; text-align: center;">
        <h3 style="color: #27ae60; margin-top: 0;">🔒 Sua Privacidade Está Protegida</h3>
        <p style="color: #2c3e50; font-size: 16px; line-height: 1.6; margin-bottom: 0;">
            ✨ <strong>Relaxe!</strong> Todas as suas respostas foram armazenadas de forma <strong>100% anônima</strong> e confidencial.<br>
            🌟 Apenas o professor terá acesso aos dados consolidados, sem identificação individual.<br>
            💫 Sua honestidade contribui para um ambiente mais justo e colaborativo na equipe!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gerar comprovante
    comprovante_html = gerar_comprovante(
        dados['avaliador_nome'],
        dados['avaliador_matricula'],
        dados['nome_equipe'],
        avaliacoes
    )
    
    # Botões de ação
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.download_button(
            label="📄 Baixar Comprovante de Envio (PDF)",
            data=comprovante_html,
            file_name=f"comprovante_avaliacao_{dados['avaliador_nome'].replace(' ', '_')}.pdf",
            mime="application/pdf",
            type="primary",
            width='stretch'
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🏠 Nova Avaliação", width='stretch'):
            # Limpar dados da sessão
            if 'formulario_dados' in st.session_state:
                del st.session_state.formulario_dados
            if 'avaliacoes_realizadas' in st.session_state:
                del st.session_state.avaliacoes_realizadas
            st.session_state.etapa_atual = 'formulario'
            st.rerun()

def main_student_form():
    """Função principal do formulário do aluno"""
    
    # Inicializar estado da sessão
    if 'etapa_atual' not in st.session_state:
        st.session_state.etapa_atual = 'formulario'
    
    # Navegação baseada na etapa atual
    if st.session_state.etapa_atual == 'formulario':
        mostrar_formulario_avaliacao()
    elif st.session_state.etapa_atual == 'avaliacoes':
        mostrar_avaliacoes()
    elif st.session_state.etapa_atual == 'sucesso':
        mostrar_sucesso()
