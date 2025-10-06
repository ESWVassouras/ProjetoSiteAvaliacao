import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import DatabaseManager
from utils import exportar_para_excel

def mostrar_dashboard_professor():
    """Dashboard principal para o professor visualizar as avaliações"""
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #2c3e50;">📊 Dashboard - Avaliações entre Equipes</h1>
        <p style="color: #7f8c8d; font-size: 16px;">
            Visão geral das avaliações realizadas pelos alunos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Obter dados
    db = DatabaseManager()
    colunas, dados = db.obter_todas_avaliacoes()
    estatisticas = db.obter_estatisticas()
    
    if not dados:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: #f8f9fa; 
                    border-radius: 15px; border: 2px dashed #dee2e6;">
            <h3 style="color: #6c757d;">📭 Nenhuma avaliação encontrada</h3>
            <p style="color: #6c757d;">Os alunos ainda não enviaram nenhuma avaliação.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Converter para DataFrame
    df = pd.DataFrame(dados, columns=colunas)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total de Avaliações",
            value=estatisticas['total_avaliacoes'],
            help="Número total de avaliações individuais realizadas"
        )
    
    with col2:
        st.metric(
            label="👥 Alunos que Avaliaram",
            value=estatisticas['total_avaliadores'],
            help="Número de alunos únicos que já enviaram avaliações"
        )
    
    with col3:
        st.metric(
            label="🏢 Equipes Ativas",
            value=estatisticas['total_equipes'],
            help="Número de equipes que já realizaram avaliações"
        )
    
    with col4:
        st.metric(
            label="⭐ Média de Pontuação",
            value=f"{estatisticas['media_pontuacao']}/2",
            help="Média geral das pontuações atribuídas"
        )
    
    st.markdown("---")
    
    # Abas para diferentes visualizações
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📈 Gráficos", "📋 Dados Detalhados", "🏆 Ranking", "👤 Filtro por Aluno", "⚙️ Exportar", "🗑️ Gerenciar", "🏢 Equipes"])
    
    with tab1:
        mostrar_graficos(df)
    
    with tab2:
        mostrar_dados_detalhados(df)
    
    with tab3:
        mostrar_ranking(df)
    
    with tab4:
        mostrar_filtro_por_aluno()
    
    with tab5:
        mostrar_exportacao()
    
    with tab6:
        mostrar_gerenciar_avaliacoes(df)
    
    with tab7:
        mostrar_equipes_cadastradas()

def mostrar_graficos(df):
    """Mostra gráficos das avaliações"""
    
    st.markdown("### 📊 Análise Visual das Avaliações")
    
    # Gráfico de distribuição de pontuações
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição de pontuações
        pontuacao_counts = df['pontuacao'].value_counts().sort_index()
        
        fig_pontuacao = px.bar(
            x=pontuacao_counts.index,
            y=pontuacao_counts.values,
            title="Distribuição de Pontuações",
            labels={'x': 'Pontuação', 'y': 'Quantidade'},
            color=pontuacao_counts.values,
            color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60']
        )
        fig_pontuacao.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Pontuação (0-2)",
            yaxis_title="Número de Avaliações"
        )
        st.plotly_chart(fig_pontuacao, use_container_width=True)
    
    with col2:
        # Avaliações por equipe
        equipe_counts = df['nome_equipe'].value_counts()
        
        fig_equipes = px.pie(
            values=equipe_counts.values,
            names=equipe_counts.index,
            title="Avaliações por Equipe"
        )
        fig_equipes.update_layout(height=400)
        st.plotly_chart(fig_equipes, use_container_width=True)
    
    # Gráfico de critérios mais mencionados
    st.markdown("### 📋 Critérios Mais Avaliados")
    
    criterios_data = {
        'Comprometimento': df['comprometimento'].sum(),
        'Trabalho em Equipe': df['trabalho_equipe'].sum(),
        'Qualidade das Entregas': df['qualidade_entregas'].sum(),
        'Proatividade': df['proatividade'].sum(),
        'Cumprimento de Responsabilidades': df['cumprimento_responsabilidades'].sum()
    }
    
    fig_criterios = px.bar(
        x=list(criterios_data.keys()),
        y=list(criterios_data.values()),
        title="Frequência dos Critérios de Avaliação",
        labels={'x': 'Critérios', 'y': 'Número de Menções'}
    )
    fig_criterios.update_layout(
        height=400,
        xaxis_tickangle=-45,
        yaxis_title="Número de Avaliações"
    )
    st.plotly_chart(fig_criterios, use_container_width=True)

def mostrar_dados_detalhados(df):
    """Mostra os dados detalhados das avaliações"""
    
    st.markdown("### 📋 Dados Detalhados das Avaliações")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        equipes_unicas = ['Todas'] + sorted(df['nome_equipe'].unique().tolist())
        equipe_filtro = st.selectbox("Filtrar por Equipe:", equipes_unicas)
    
    with col2:
        pontuacoes_unicas = ['Todas'] + sorted(df['pontuacao'].unique().tolist())
        pontuacao_filtro = st.selectbox("Filtrar por Pontuação:", pontuacoes_unicas)
    
    with col3:
        mostrar_comentarios = st.checkbox("Mostrar apenas avaliações com comentários")
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if equipe_filtro != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['nome_equipe'] == equipe_filtro]
    
    if pontuacao_filtro != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['pontuacao'] == pontuacao_filtro]
    
    if mostrar_comentarios:
        df_filtrado = df_filtrado[df_filtrado['comentario'].notna() & (df_filtrado['comentario'] != '')]
    
    # Mostrar tabela
    if len(df_filtrado) > 0:
        # Converter booleanos para texto
        df_display = df_filtrado.copy()
        bool_columns = ['comprometimento', 'trabalho_equipe', 'qualidade_entregas', 
                       'proatividade', 'cumprimento_responsabilidades']
        
        for col in bool_columns:
            if col in df_display.columns:
                df_display[col] = df_display[col].map({1: 'Sim', 0: 'Não'})
        
        # Renomear colunas
        df_display = df_display.rename(columns={
            'avaliador_nome': 'Avaliador',
            'avaliador_matricula': 'Matrícula',
            'nome_equipe': 'Equipe',
            'avaliado_nome': 'Avaliado',
            'pontuacao': 'Pontuação',
            'comprometimento': 'Comprometimento',
            'trabalho_equipe': 'Trabalho em Equipe',
            'qualidade_entregas': 'Qualidade das Entregas',
            'proatividade': 'Proatividade',
            'cumprimento_responsabilidades': 'Cumprimento de Responsabilidades',
            'comentario': 'Comentário',
            'created_at': 'Data/Hora'
        })
        
        # Selecionar colunas para exibição
        colunas_exibir = ['Avaliador', 'Matrícula', 'Equipe', 'Avaliado', 'Pontuação',
                         'Comprometimento', 'Trabalho em Equipe', 'Qualidade das Entregas',
                         'Proatividade', 'Cumprimento de Responsabilidades', 'Comentário', 'Data/Hora']
        
        st.dataframe(
            df_display[colunas_exibir],
            use_container_width=True,
            height=400
        )
        
        st.markdown(f"**Total de registros encontrados: {len(df_filtrado)}**")
    else:
        st.info("Nenhum registro encontrado com os filtros aplicados.")

def mostrar_ranking(df):
    """Mostra ranking dos alunos mais bem avaliados"""
    
    st.markdown("### 🏆 Ranking dos Alunos Mais Bem Avaliados")
    
    # Calcular média por aluno avaliado
    ranking = df.groupby('avaliado_nome').agg({
        'pontuacao': ['mean', 'count'],
        'comprometimento': 'sum',
        'trabalho_equipe': 'sum',
        'qualidade_entregas': 'sum',
        'proatividade': 'sum',
        'cumprimento_responsabilidades': 'sum'
    }).round(2)
    
    # Flatten column names
    ranking.columns = ['Media_Pontuacao', 'Total_Avaliacoes', 'Comprometimento', 
                      'Trabalho_Equipe', 'Qualidade_Entregas', 'Proatividade', 
                      'Cumprimento_Responsabilidades']
    
    # Filtrar apenas alunos com pelo menos 2 avaliações
    ranking = ranking[ranking['Total_Avaliacoes'] >= 2]
    
    # Ordenar por média de pontuação
    ranking = ranking.sort_values('Media_Pontuacao', ascending=False)
    
    if len(ranking) > 0:
        # Top 10
        top_ranking = ranking.head(10)
        
        # Criar gráfico
        fig = px.bar(
            top_ranking,
            x='Media_Pontuacao',
            y=top_ranking.index,
            orientation='h',
            title="Top 10 Alunos Mais Bem Avaliados",
            labels={'Media_Pontuacao': 'Média de Pontuação', 'index': 'Aluno'},
            color='Media_Pontuacao',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Média de Pontuação (0-2)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("#### 📊 Detalhamento do Ranking")
        
        ranking_display = ranking.copy()
        ranking_display = ranking_display.reset_index()
        ranking_display = ranking_display.rename(columns={
            'avaliado_nome': 'Aluno',
            'Media_Pontuacao': 'Média de Pontuação',
            'Total_Avaliacoes': 'Total de Avaliações',
            'Comprometimento': 'Menções - Comprometimento',
            'Trabalho_Equipe': 'Menções - Trabalho em Equipe',
            'Qualidade_Entregas': 'Menções - Qualidade das Entregas',
            'Proatividade': 'Menções - Proatividade',
            'Cumprimento_Responsabilidades': 'Menções - Cumprimento de Responsabilidades'
        })
        
        st.dataframe(
            ranking_display,
            use_container_width=True,
            height=400
        )
    else:
        st.info("Não há dados suficientes para gerar o ranking (mínimo de 2 avaliações por aluno).")

def mostrar_exportacao():
    """Interface para exportação de dados"""
    
    st.markdown("### ⚙️ Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #e8f5e8; border: 2px solid #27ae60; border-radius: 10px; 
                    padding: 20px; text-align: center;">
            <h4 style="color: #27ae60; margin-top: 0;">📊 Exportar para Excel</h4>
            <p style="color: #2c3e50; margin-bottom: 15px;">
                Baixe todos os dados das avaliações em formato Excel para análise externa.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📥 Baixar Arquivo Excel", type="primary", width='stretch'):
            try:
                excel_data = exportar_para_excel()
                if excel_data:
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=excel_data,
                        file_name=f"avaliacoes_equipes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary",
                        width='stretch'
                    )
                else:
                    st.error("❌ Nenhum dado encontrado para exportar.")
            except Exception as e:
                st.error(f"❌ Erro ao exportar dados: {str(e)}")
    
    with col2:
        st.markdown("""
        <div style="background-color: #fff3cd; border: 2px solid #f39c12; border-radius: 10px; 
                    padding: 20px; text-align: center;">
            <h4 style="color: #f39c12; margin-top: 0;">📈 Relatórios Automáticos</h4>
            <p style="color: #2c3e50; margin-bottom: 15px;">
                Em breve: relatórios automáticos com insights e análises avançadas.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.button("🚧 Em Desenvolvimento", disabled=True, width='stretch')
    
    # Informações sobre a exportação
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #f8f9fa; border-radius: 10px; padding: 20px;">
        <h4 style="color: #2c3e50;">ℹ️ Informações sobre a Exportação</h4>
        <ul style="color: #34495e;">
            <li><strong>Formato:</strong> Excel (.xlsx) compatível com Microsoft Excel e Google Sheets</li>
            <li><strong>Dados incluídos:</strong> Todas as avaliações, critérios, pontuações e comentários</li>
            <li><strong>Confidencialidade:</strong> Os dados exportados mantêm a mesma confidencialidade do sistema</li>
            <li><strong>Atualização:</strong> Os dados são exportados no momento da solicitação</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def mostrar_gerenciar_avaliacoes(df):
    """Interface para gerenciar (deletar) avaliações"""
    
    st.markdown("### 🗑️ Gerenciar Avaliações")
    
    if len(df) == 0:
        st.info("Não há avaliações para gerenciar.")
        return
    
    # Seção para deletar todas as avaliações
    st.markdown("#### ⚠️ Deletar Todas as Avaliações")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background-color: #fdf2f2; border: 2px solid #f87171; border-radius: 10px; 
                    padding: 20px; margin-bottom: 20px;">
            <h4 style="color: #dc2626; margin-top: 0;">⚠️ Ação Irreversível</h4>
            <p style="color: #7f1d1d; margin-bottom: 0;">
                Esta ação irá <strong>deletar permanentemente</strong> todas as avaliações do sistema.<br>
                <strong>Esta operação não pode ser desfeita!</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🗑️ Deletar Todas", type="secondary", width='stretch'):
            if 'confirmar_deletar_todas' not in st.session_state:
                st.session_state.confirmar_deletar_todas = True
                st.rerun()
            else:
                # Confirmar exclusão
                db = DatabaseManager()
                deleted_count = db.deletar_todas_avaliacoes()
                st.success(f"✅ {deleted_count} avaliações foram deletadas permanentemente!")
                del st.session_state.confirmar_deletar_todas
                st.rerun()
    
    # Confirmação para deletar todas
    if st.session_state.get('confirmar_deletar_todas', False):
        st.warning("⚠️ Tem certeza que deseja deletar TODAS as avaliações?")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Sim, Deletar Todas", type="primary"):
                db = DatabaseManager()
                deleted_count = db.deletar_todas_avaliacoes()
                st.success(f"✅ {deleted_count} avaliações foram deletadas permanentemente!")
                del st.session_state.confirmar_deletar_todas
                st.rerun()
        
        with col2:
            if st.button("❌ Cancelar"):
                del st.session_state.confirmar_deletar_todas
                st.rerun()
    
    st.markdown("---")
    
    # Seção para deletar avaliações individuais
    st.markdown("#### 📝 Deletar Avaliações Individuais")
    
    # Converter booleanos para texto
    df_display = df.copy()
    bool_columns = ['comprometimento', 'trabalho_equipe', 'qualidade_entregas', 
                   'proatividade', 'cumprimento_responsabilidades']
    
    for col in bool_columns:
        if col in df_display.columns:
            df_display[col] = df_display[col].map({1: 'Sim', 0: 'Não'})
    
    # Renomear colunas
    df_display = df_display.rename(columns={
        'id': 'ID',
        'avaliador_nome': 'Avaliador',
        'avaliador_matricula': 'Matrícula',
        'nome_equipe': 'Equipe',
        'avaliado_nome': 'Avaliado',
        'pontuacao': 'Pontuação',
        'comprometimento': 'Comprometimento',
        'trabalho_equipe': 'Trabalho em Equipe',
        'qualidade_entregas': 'Qualidade das Entregas',
        'proatividade': 'Proatividade',
        'cumprimento_responsabilidades': 'Cumprimento de Responsabilidades',
        'comentario': 'Comentário',
        'created_at': 'Data/Hora'
    })
    
    # Mostrar tabela com botões de deletar
    for idx, row in df_display.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background-color: #f8f9fa; color: black; padding: 10px; border-radius: 5px; 
                            border-left: 4px solid #007bff; margin-bottom: 10px;">
                    <strong>ID {row['ID']}</strong> | 
                    <strong>{row['Avaliador']}</strong> avaliou <strong>{row['Avaliado']}</strong> | 
                    Pontuação: <strong>{row['Pontuação']}/2</strong> | 
                    Equipe: <strong>{row['Equipe']}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🗑️", key=f"delete_{row['ID']}", help="Deletar esta avaliação"):
                    if f'confirm_delete_{row["ID"]}' not in st.session_state:
                        st.session_state[f'confirm_delete_{row["ID"]}'] = True
                        st.rerun()
                    else:
                        # Confirmar exclusão
                        db = DatabaseManager()
                        if db.deletar_avaliacao_por_id(row['ID']):
                            st.success(f"✅ Avaliação ID {row['ID']} deletada!")
                            del st.session_state[f'confirm_delete_{row["ID"]}']
                            st.rerun()
                        else:
                            st.error("❌ Erro ao deletar avaliação!")
            
            with col3:
                if st.session_state.get(f'confirm_delete_{row["ID"]}', False):
                    if st.button("✅", key=f"confirm_{row['ID']}", help="Confirmar exclusão"):
                        db = DatabaseManager()
                        if db.deletar_avaliacao_por_id(row['ID']):
                            st.success(f"✅ Avaliação ID {row['ID']} deletada!")
                            del st.session_state[f'confirm_delete_{row["ID"]}']
                            st.rerun()
                        else:
                            st.error("❌ Erro ao deletar avaliação!")
            
            # Confirmação individual
            if st.session_state.get(f'confirm_delete_{row["ID"]}', False):
                st.warning(f"⚠️ Tem certeza que deseja deletar a avaliação ID {row['ID']}?")
    
    st.markdown(f"**Total de avaliações: {len(df)}**")

def mostrar_equipes_cadastradas():
    """Mostra todas as equipes cadastradas"""
    
    st.markdown("### 🏢 Equipes Cadastradas")
    
    try:
        db = DatabaseManager()
        equipes = db.listar_todas_equipes()
        
        if equipes:
            st.markdown(f"**Total de equipes cadastradas: {len(equipes)}**")
            
            # Botão para deletar todas as equipes
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🗑️ Deletar Todas as Equipes", type="secondary", width='stretch'):
                    st.session_state.confirmar_deletar_todas_equipes = True
                    st.rerun()
            
            # Confirmação para deletar todas
            if st.session_state.get('confirmar_deletar_todas_equipes', False):
                st.warning("⚠️ **ATENÇÃO:** Tem certeza que deseja deletar TODAS as equipes? Esta ação não pode ser desfeita!")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("✅ SIM, Deletar Todas", type="primary", width='stretch'):
                        deleted_count = db.deletar_todas_equipes()
                        st.success(f"✅ {deleted_count} equipes foram deletadas permanentemente!")
                        del st.session_state.confirmar_deletar_todas_equipes
                        st.rerun()
                    if st.button("❌ Cancelar", type="secondary", width='stretch'):
                        del st.session_state.confirmar_deletar_todas_equipes
                        st.rerun()
            
            st.markdown("---")
            
            # Mostrar equipes com botões de exclusão individual
            st.markdown("#### 📋 Lista de Equipes:")
            
            for i, equipe in enumerate(equipes):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; color: black; padding: 15px; border-radius: 10px; 
                                border-left: 4px solid #007bff; margin-bottom: 10px;">
                        <strong>🏢 {equipe}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Botão de exclusão individual
                    if st.button("🗑️", key=f"delete_equipe_{i}", help="Deletar esta equipe"):
                        st.session_state[f'confirm_delete_equipe_{i}'] = True
                        st.rerun()
                
                # Confirmação individual
                if st.session_state.get(f'confirm_delete_equipe_{i}', False):
                    st.warning(f"⚠️ Tem certeza que deseja deletar a equipe '{equipe}'?")
                    col_confirm1, col_confirm2 = st.columns(2)
                    
                    with col_confirm1:
                        if st.button("✅ SIM", key=f"confirm_yes_{i}", type="primary"):
                            if db.deletar_equipe_por_nome(equipe):
                                st.success(f"✅ Equipe '{equipe}' deletada!")
                                del st.session_state[f'confirm_delete_equipe_{i}']
                                st.rerun()
                            else:
                                st.error("❌ Erro ao deletar equipe!")
                    
                    with col_confirm2:
                        if st.button("❌ Cancelar", key=f"confirm_no_{i}", type="secondary"):
                            del st.session_state[f'confirm_delete_equipe_{i}']
                            st.rerun()
            
            # Estatísticas das equipes
            st.markdown("---")
            st.markdown("### 📊 Estatísticas das Equipes")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="📋 Total de Equipes",
                    value=len(equipes)
                )
            
            with col2:
                # Contar avaliações por equipe
                if len(equipes) > 0:
                    db = DatabaseManager()
                    colunas, dados = db.obter_todas_avaliacoes()
                    df = pd.DataFrame(dados, columns=colunas)
                    
                    if len(df) > 0:
                        avaliacoes_por_equipe = df['nome_equipe'].value_counts()
                        equipe_mais_ativa = avaliacoes_por_equipe.index[0] if len(avaliacoes_por_equipe) > 0 else "N/A"
                        st.metric(
                            label="🏆 Equipe Mais Ativa",
                            value=equipe_mais_ativa
                        )
                    else:
                        st.metric(
                            label="🏆 Equipe Mais Ativa",
                            value="N/A"
                        )
                else:
                    st.metric(
                        label="🏆 Equipe Mais Ativa",
                        value="N/A"
                    )
            
            with col3:
                if len(df) > 0:
                    media_avaliacoes = len(df) / len(equipes) if len(equipes) > 0 else 0
                    st.metric(
                        label="📈 Média de Avaliações/Equipe",
                        value=f"{media_avaliacoes:.1f}"
                    )
                else:
                    st.metric(
                        label="📈 Média de Avaliações/Equipe",
                        value="0"
                    )
        
        else:
            st.info("📭 Nenhuma equipe cadastrada ainda.")
            st.markdown("""
            <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; 
                        padding: 20px; margin: 20px 0;">
                <h4 style="color: #856404; margin-top: 0;">ℹ️ Como funciona:</h4>
                <p style="color: #856404; margin-bottom: 0;">
                    As equipes são cadastradas automaticamente quando os alunos preenchem o formulário de avaliação.
                    Cada vez que um aluno digita o nome de uma equipe, ela é salva na tabela de equipes para futuras sugestões.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar equipes: {str(e)}")

def mostrar_filtro_por_aluno():
    """Interface para filtrar avaliações por aluno específico"""
    
    st.markdown("### 👤 Filtro por Aluno")
    
    try:
        db = DatabaseManager()
        
        # Obter lista de alunos que foram avaliados
        alunos_avaliados = db.obter_lista_alunos_avaliados()
        
        if not alunos_avaliados:
            st.markdown("""
            <div style="text-align: center; padding: 40px; background-color: #f8f9fa; 
                        border-radius: 15px; border: 2px dashed #dee2e6;">
                <h3 style="color: #6c757d;">📭 Nenhum aluno avaliado encontrado</h3>
                <p style="color: #6c757d;">Ainda não há avaliações para filtrar por aluno.</p>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Interface de filtro
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🔍 Selecione um aluno para visualizar suas estatísticas:")
            
            # Selectbox para escolher aluno
            aluno_selecionado = st.selectbox(
                "Aluno:",
                options=["Todos os Alunos"] + sorted(alunos_avaliados),
                help="Escolha um aluno específico ou visualize todos"
            )
        
        with col2:
            st.markdown("#### 📊 Opções de Visualização:")
            mostrar_detalhado = st.checkbox("Mostrar detalhamento por pontuação", value=True)
            mostrar_grafico = st.checkbox("Mostrar gráfico", value=True)
        
        st.markdown("---")
        
        # Processar seleção
        if aluno_selecionado == "Todos os Alunos":
            mostrar_estatisticas_gerais_alunos(db, mostrar_detalhado, mostrar_grafico)
        else:
            mostrar_estatisticas_aluno_especifico(db, aluno_selecionado, mostrar_detalhado, mostrar_grafico)
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar filtro por aluno: {str(e)}")

def mostrar_estatisticas_gerais_alunos(db, mostrar_detalhado, mostrar_grafico):
    """Mostra estatísticas de todos os alunos"""
    
    st.markdown("#### 📊 Estatísticas de Todos os Alunos")
    
    # Obter estatísticas de todos os alunos
    estatisticas = db.obter_estatisticas_por_aluno()
    
    if not estatisticas:
        st.info("Nenhuma estatística encontrada.")
        return
    
    # Métricas gerais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="👥 Total de Alunos Avaliados",
            value=len(estatisticas),
            help="Número de alunos únicos que receberam avaliações"
        )
    
    with col2:
        total_avaliacoes = sum(stat['total_avaliacoes'] for stat in estatisticas)
        st.metric(
            label="📝 Total de Avaliações",
            value=total_avaliacoes,
            help="Número total de avaliações recebidas por todos os alunos"
        )
    
    with col3:
        media_geral = sum(stat['media_pontuacao'] for stat in estatisticas) / len(estatisticas) if estatisticas else 0
        st.metric(
            label="⭐ Média Geral",
            value=f"{media_geral:.2f}/2",
            help="Média geral das pontuações de todos os alunos"
        )
    
    st.markdown("---")
    
    # Tabela com estatísticas de todos os alunos
    st.markdown("#### 📋 Ranking de Alunos")
    
    # Preparar dados para tabela
    df_estatisticas = pd.DataFrame(estatisticas)
    df_estatisticas = df_estatisticas.rename(columns={
        'aluno': 'Aluno',
        'total_avaliacoes': 'Total de Avaliações',
        'media_pontuacao': 'Média de Pontuação'
    })
    
    # Adicionar ranking
    df_estatisticas['Ranking'] = range(1, len(df_estatisticas) + 1)
    
    # Reordenar colunas
    df_estatisticas = df_estatisticas[['Ranking', 'Aluno', 'Total de Avaliações', 'Média de Pontuação']]
    
    st.dataframe(
        df_estatisticas,
        use_container_width=True,
        height=400
    )
    
    # Gráfico se solicitado
    if mostrar_grafico and len(estatisticas) > 0:
        st.markdown("#### 📈 Gráfico de Médias por Aluno")
        
        # Limitar a top 15 para melhor visualização
        top_15 = estatisticas[:15]
        
        fig = px.bar(
            top_15,
            x='media_pontuacao',
            y='aluno',
            orientation='h',
            title="Top 15 Alunos por Média de Pontuação",
            labels={'media_pontuacao': 'Média de Pontuação', 'aluno': 'Aluno'},
            color='media_pontuacao',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            height=max(400, len(top_15) * 25),
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Média de Pontuação (0-2)"
        )
        st.plotly_chart(fig, use_container_width=True)

def mostrar_estatisticas_aluno_especifico(db, nome_aluno, mostrar_detalhado, mostrar_grafico):
    """Mostra estatísticas de um aluno específico"""
    
    st.markdown(f"#### 👤 Estatísticas de: **{nome_aluno}**")
    
    # Obter estatísticas do aluno específico
    estatisticas = db.obter_estatisticas_por_aluno(nome_aluno)
    
    if not estatisticas or estatisticas['total_avaliacoes'] == 0:
        st.markdown("""
        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; 
                    padding: 20px; text-align: center;">
            <h4 style="color: #856404;">⚠️ Aluno não encontrado</h4>
            <p style="color: #856404;">Este aluno ainda não recebeu nenhuma avaliação.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📝 Total de Avaliações",
            value=estatisticas['total_avaliacoes'],
            help="Quantidade total de avaliações recebidas"
        )
    
    with col2:
        st.metric(
            label="⭐ Média de Pontuação",
            value=f"{estatisticas['media_pontuacao']}/2",
            help="Média das pontuações recebidas",
            delta=f"{(estatisticas['media_pontuacao'] - 1):.2f}" if estatisticas['media_pontuacao'] != 1 else None
        )
    
    with col3:
        porcentagem_pontuacao_2 = (estatisticas['pontuacao_2'] / estatisticas['total_avaliacoes']) * 100 if estatisticas['total_avaliacoes'] > 0 else 0
        st.metric(
            label="🌟 Pontuação 2 (Excelente)",
            value=estatisticas['pontuacao_2'],
            help=f"{porcentagem_pontuacao_2:.1f}% das avaliações",
            delta=f"{porcentagem_pontuacao_2:.1f}%"
        )
    
    with col4:
        porcentagem_pontuacao_0 = (estatisticas['pontuacao_0'] / estatisticas['total_avaliacoes']) * 100 if estatisticas['total_avaliacoes'] > 0 else 0
        st.metric(
            label="⚠️ Pontuação 0 (Precisa Melhorar)",
            value=estatisticas['pontuacao_0'],
            help=f"{porcentagem_pontuacao_0:.1f}% das avaliações",
            delta=f"{porcentagem_pontuacao_0:.1f}%"
        )
    
    st.markdown("---")
    
    # Detalhamento por pontuação
    if mostrar_detalhado:
        st.markdown("#### 📊 Detalhamento por Pontuação")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 10px; 
                        padding: 15px; text-align: center;">
                <h4 style="color: #155724; margin: 0;">🌟 Excelente (2 pontos)</h4>
                <h2 style="color: #155724; margin: 5px 0;">{}</h2>
                <p style="color: #155724; margin: 0;">{:.1f}% das avaliações</p>
            </div>
            """.format(estatisticas['pontuacao_2'], porcentagem_pontuacao_2), unsafe_allow_html=True)
        
        with col2:
            porcentagem_pontuacao_1 = (estatisticas['pontuacao_1'] / estatisticas['total_avaliacoes']) * 100 if estatisticas['total_avaliacoes'] > 0 else 0
            st.markdown("""
            <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; 
                        padding: 15px; text-align: center;">
                <h4 style="color: #856404; margin: 0;">⚡ Bom (1 ponto)</h4>
                <h2 style="color: #856404; margin: 5px 0;">{}</h2>
                <p style="color: #856404; margin: 0;">{:.1f}% das avaliações</p>
            </div>
            """.format(estatisticas['pontuacao_1'], porcentagem_pontuacao_1), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 10px; 
                        padding: 15px; text-align: center;">
                <h4 style="color: #721c24; margin: 0;">⚠️ Precisa Melhorar (0 pontos)</h4>
                <h2 style="color: #721c24; margin: 5px 0;">{}</h2>
                <p style="color: #721c24; margin: 0;">{:.1f}% das avaliações</p>
            </div>
            """.format(estatisticas['pontuacao_0'], porcentagem_pontuacao_0), unsafe_allow_html=True)
    
    # Gráfico se solicitado
    if mostrar_grafico:
        st.markdown("#### 📈 Distribuição de Pontuações")
        
        # Dados para o gráfico
        dados_grafico = {
            'Pontuação': ['2 (Excelente)', '1 (Bom)', '0 (Precisa Melhorar)'],
            'Quantidade': [estatisticas['pontuacao_2'], estatisticas['pontuacao_1'], estatisticas['pontuacao_0']],
            'Porcentagem': [porcentagem_pontuacao_2, porcentagem_pontuacao_1, porcentagem_pontuacao_0]
        }
        
        fig = px.pie(
            values=dados_grafico['Quantidade'],
            names=dados_grafico['Pontuação'],
            title=f"Distribuição das Avaliações de {nome_aluno}",
            color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de barras também
        fig_bar = px.bar(
            x=dados_grafico['Pontuação'],
            y=dados_grafico['Quantidade'],
            title=f"Quantidade de Avaliações por Pontuação - {nome_aluno}",
            labels={'x': 'Pontuação', 'y': 'Quantidade'},
            color=dados_grafico['Quantidade'],
            color_continuous_scale=['#dc3545', '#ffc107', '#28a745']
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
