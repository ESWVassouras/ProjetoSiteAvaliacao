# 📊 Sistema de Avaliação entre Equipes

Sistema desenvolvido em Python com Streamlit para avaliação anônima entre membros de equipes do componente curricular **Práticas Extensionistas V** do curso de Engenharia de Software.

## 🎯 Funcionalidades

### Para Alunos
- ✅ Formulário de avaliação anônimo e intuitivo
- ✅ Seleção múltipla de colegas de equipe
- ✅ Sistema de pontuação de 0 a 2 pontos
- ✅ Critérios de avaliação específicos
- ✅ Campo de comentários opcional
- ✅ Geração de comprovante de envio
- ✅ Interface responsiva e amigável

### Para Professores
- ✅ Sistema de login seguro
- ✅ Dashboard com estatísticas em tempo real
- ✅ Visualizações gráficas das avaliações
- ✅ Ranking dos alunos mais bem avaliados
- ✅ Filtros avançados para análise
- ✅ Exportação de dados para Excel
- ✅ Acesso a todos os dados de forma consolidada

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe os arquivos do projeto**

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

4. **Acesse no navegador:**
   - A aplicação será aberta automaticamente em `http://localhost:8501`

## 🔐 Acesso do Professor

**Login:** `professor`  
**Senha:** `01230123`

## 📋 Critérios de Avaliação

Os alunos podem avaliar seus colegas baseados nos seguintes critérios:

1. **Comprometimento e responsabilidade** — comparecimento às reuniões, cumprimento de prazos, envolvimento com o projeto
2. **Trabalho em equipe e colaboração** — comunicação, respeito às ideias do grupo, apoio aos colegas
3. **Qualidade das entregas e contribuições técnicas** — qualidade e relevância das tarefas realizadas
4. **Proatividade e iniciativa** — participação ativa, busca de soluções, contribuição além do mínimo esperado
5. **Cumprimento de responsabilidades específicas** — execução das tarefas que lhe foram designadas

## 📊 Sistema de Pontuação

- **0 pontos:** Não contribuiu ou apresentou desempenho insatisfatório
- **1 ponto:** Contribuiu parcialmente / desempenho razoável
- **2 pontos:** Contribuiu plenamente / desempenho excelente

## 🗄️ Banco de Dados

O sistema utiliza **SQLite3** para armazenamento local, mas está preparado para migração para **NeonSQL** (PostgreSQL) conforme solicitado.

### Estrutura das Tabelas

- **professores:** Armazenamento de credenciais dos professores
- **equipes:** Registro das equipes/projetos
- **avaliacoes:** Todas as avaliações realizadas pelos alunos

## 📁 Estrutura do Projeto

```
├── app.py                 # Aplicação principal
├── auth.py               # Sistema de autenticação
├── database.py           # Gerenciamento do banco de dados
├── student_form.py       # Formulário para alunos
├── admin_dashboard.py    # Dashboard do professor
├── utils.py              # Funções utilitárias
├── requirements.txt      # Dependências do projeto
└── README.md            # Documentação
```

## 🔒 Confidencialidade

- ✅ Todas as avaliações são **100% anônimas**
- ✅ Apenas o professor tem acesso aos dados consolidados
- ✅ Dados armazenados de forma segura
- ✅ Comprovantes de envio gerados para cada aluno

## 📈 Relatórios e Análises

O sistema oferece:

- **Estatísticas em tempo real**
- **Gráficos interativos**
- **Ranking de desempenho**
- **Filtros por equipe, pontuação e critérios**
- **Exportação completa para Excel**

## 🛠️ Tecnologias Utilizadas

- **Streamlit** - Framework web para Python
- **SQLite3** - Banco de dados local
- **Pandas** - Manipulação de dados
- **Plotly** - Gráficos interativos
- **OpenPyXL** - Exportação para Excel
- **BCrypt** - Criptografia de senhas

## 📞 Suporte

Para dúvidas ou sugestões sobre o sistema, entre em contato com o professor da disciplina.

---

**Desenvolvido com ❤️ para a disciplina de Práticas Extensionistas V - Engenharia de Software**
