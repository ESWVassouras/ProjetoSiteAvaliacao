import streamlit as st
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def gerar_comprovante_pdf(avaliador_nome, avaliador_matricula, nome_equipe, avaliacoes_realizadas):
    """Gera um comprovante de envio do formulário em PDF"""
    
    # Criar buffer para o PDF
    buffer = io.BytesIO()
    
    # Criar documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para o título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Centralizado
        textColor=colors.darkblue
    )
    
    # Estilo para seções
    section_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=12,
        textColor=colors.darkblue
    )
    
    # Estilo para conteúdo
    content_style = ParagraphStyle(
        'CustomContent',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6,
        leftIndent=20
    )
    
    # Conteúdo do documento
    story = []
    
    # Título principal
    story.append(Paragraph("📋 COMPROVANTE DE AVALIAÇÃO", title_style))
    story.append(Spacer(1, 20))
    
    # Badge de sucesso
    story.append(Paragraph("✅ FORMULÁRIO ENVIADO COM SUCESSO", section_style))
    story.append(Spacer(1, 15))
    
    # Informações do avaliador
    story.append(Paragraph("👤 Informações do Avaliador:", section_style))
    story.append(Paragraph(f"<b>Nome:</b> {avaliador_nome}", content_style))
    story.append(Paragraph(f"<b>Matrícula:</b> {avaliador_matricula}", content_style))
    story.append(Paragraph(f"<b>Equipe/Projeto:</b> {nome_equipe}", content_style))
    story.append(Spacer(1, 15))
    
    # Data e hora
    story.append(Paragraph("📅 Data e Hora do Envio:", section_style))
    story.append(Paragraph(f"{datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", content_style))
    story.append(Spacer(1, 15))
    
    # Resumo das avaliações
    story.append(Paragraph("📊 Resumo das Avaliações Realizadas:", section_style))
    story.append(Paragraph(f"<b>Total de colegas avaliados:</b> {len(avaliacoes_realizadas)}", content_style))
    story.append(Spacer(1, 15))
    
    # Lista de colegas avaliados (apenas nomes)
    story.append(Paragraph("📝 Colegas Avaliados:", section_style))
    
    # Criar tabela com os nomes dos colegas
    colegas_data = [["Nome do Colega"]]
    for avaliacao in avaliacoes_realizadas:
        colegas_data.append([avaliacao['avaliado_nome']])
    
    # Estilo da tabela
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    
    colegas_table = Table(colegas_data, colWidths=[4*inch])
    colegas_table.setStyle(table_style)
    story.append(colegas_table)
    story.append(Spacer(1, 20))
    
    # Rodapé com informações de confidencialidade
    story.append(Spacer(1, 20))
    story.append(Paragraph("🔒 Confidencialidade Garantida", section_style))
    story.append(Paragraph("Este comprovante serve como registro de sua participação na avaliação.", content_style))
    story.append(Paragraph("Suas respostas foram armazenadas de forma anônima e confidencial.", content_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Sistema de Avaliação entre Equipes - Práticas Extensionistas V", content_style))
    story.append(Paragraph("Engenharia de Software", content_style))
    
    # Construir PDF
    doc.build(story)
    
    # Obter conteúdo do buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content

def gerar_comprovante(avaliador_nome, avaliador_matricula, nome_equipe, avaliacoes_realizadas):
    """Gera um comprovante de envio do formulário em PDF (versão simplificada para compatibilidade)"""
    return gerar_comprovante_pdf(avaliador_nome, avaliador_matricula, nome_equipe, avaliacoes_realizadas)

def exportar_para_excel():
    """Exporta todas as avaliações para Excel"""
    from database import DatabaseManager
    
    db = DatabaseManager()
    colunas, dados = db.obter_todas_avaliacoes()
    
    if not dados:
        return None
    
    # Criar DataFrame
    df = pd.DataFrame(dados, columns=colunas)
    
    # Converter booleanos para texto
    bool_columns = ['comprometimento', 'trabalho_equipe', 'qualidade_entregas', 
                   'proatividade', 'cumprimento_responsabilidades']
    
    for col in bool_columns:
        if col in df.columns:
            df[col] = df[col].map({1: 'Sim', 0: 'Não'})
    
    # Renomear colunas para português
    df = df.rename(columns={
        'id': 'ID',
        'avaliador_nome': 'Nome do Avaliador',
        'avaliador_matricula': 'Matrícula do Avaliador',
        'nome_equipe': 'Nome da Equipe',
        'avaliado_nome': 'Nome do Avaliado',
        'pontuacao': 'Pontuação (0-2)',
        'comprometimento': 'Comprometimento e Responsabilidade',
        'trabalho_equipe': 'Trabalho em Equipe e Colaboração',
        'qualidade_entregas': 'Qualidade das Entregas',
        'proatividade': 'Proatividade e Iniciativa',
        'cumprimento_responsabilidades': 'Cumprimento de Responsabilidades',
        'comentario': 'Comentário',
        'created_at': 'Data e Hora'
    })
    
    # Converter para Excel em memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Avaliações', index=False)
        
        # Ajustar largura das colunas
        worksheet = writer.sheets['Avaliações']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    return output.getvalue()
