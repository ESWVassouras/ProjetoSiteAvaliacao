# 📊 Sistema de Avaliação entre Equipes
Criado por: Tiago Castro - Professor - UNIVASSOURAS - MARICÁ

Protótipo funcional V.1.0.5
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

3. **Execute o sistema:**
   
   
   **Windows (Manual):**
   ```bash
   streamlit run app.py
   ```
   
   **Linux/Mac:**
   ```bash
   # Configure as variáveis de ambiente manualmente
   streamlit run app.py
   ```

4. **Acesse no navegador:**
   - A aplicação será aberta automaticamente em `http://localhost:8501`

## 🔐 Acesso do Professor

Para acessar o dashboard do professor, use as credenciais configuradas no sistema. 
(Acesso restrito ao professor)


### Configuração de Variáveis de Ambiente

Para maior segurança, configure as seguintes variáveis de ambiente:

#### **Windows (Recomendado):**
Execute um dos scripts de configuração:
- **Batch:** `setup_env.bat`
- **PowerShell:** `setup_env.ps1`

#### **Linux/Mac:**
```bash
# Banco de dados NeonSQL
export NEON_HOST="seu_host_aqui"
export NEON_PORT="5432"
export NEON_DATABASE="seu_database_aqui"
export NEON_USER="seu_usuario_aqui"
export NEON_PASSWORD="sua_senha_do_banco_aqui"
export NEON_SSLMODE="require"
export NEON_CHANNEL_BINDING="require"

# Senha do professor (opcional, padrão: professor123)
export PROFESSOR_PASSWORD="sua_senha_segura_aqui"
```

#### **Configuração Manual no Windows:**
```powershell
$env:NEON_HOST="seu_host_aqui"
$env:NEON_PORT="5432"
$env:NEON_DATABASE="seu_database_aqui"
$env:NEON_USER="seu_usuario_aqui"
$env:NEON_PASSWORD="sua_senha_do_banco_aqui"
$env:NEON_SSLMODE="require"
$env:NEON_CHANNEL_BINDING="require"
$env:PROFESSOR_PASSWORD="sua_senha_segura_aqui"
```

**Importante:** As credenciais do banco e senha do professor devem ser alteradas em ambiente de produção.

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

O sistema utiliza **SQLite3** para armazenamento local, mas está preparado para migração para **NeonSQL** (PostgreSQL).

### Estrutura das Tabelas

- **professores:** Armazenamento de credenciais dos professores (com autorização)
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

Para dúvidas ou sugestões sobre o sistema, entre em contato com o professor Tiago.
tiago.castro@univassouras.edu.br

---

## © Copyright

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  🎓 SISTEMA DE AVALIAÇÃO ENTRE EQUIPES                                      ║
║  📚 Práticas Extensionistas V - Engenharia de Software                      ║
║                                                                              ║
║  👨‍🏫 Desenvolvido por: Tiago Castro                                           ║
║  🏛️  Universidade Vassouras - Campus Maricá                                  ║
║  📧 tiago.castro@univassouras.edu.br                                        ║
║                                                                              ║
║  📅 Copyright © 2025 Tiago Castro. Todos os direitos reservados.            ║
║                                                                              ║
║  🛡️  Este software foi desenvolvido exclusivamente para fins acadêmicos      ║
║      e educacionais, como parte do componente curricular de Práticas        ║
║      Extensionistas V do curso de Engenharia de Software.                   ║
║                                                                              ║
║  ⚖️  É vedada a reprodução, distribuição ou modificação deste código        ║
║      sem autorização expressa do autor.                                     ║
║                                                                              ║
║  🚀 Versão: 1.0.5 | Python 3.x | Streamlit Framework                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 📜 Licença Acadêmica

Este projeto foi desenvolvido como parte do componente curricular **Práticas Extensionistas V** do curso de **Engenharia de Software** da **Universidade Vassouras - Campus Maricá**.

**Características da Licença:**
- ✅ **Uso Acadêmico:** Permitido para fins educacionais e de pesquisa
- ✅ **Modificação:** Permitida com citação do autor original
- ✅ **Distribuição:** Permitida dentro do ambiente acadêmico
- ❌ **Comercialização:** Proibida sem autorização expressa
- ❌ **Uso Comercial:** Proibido em projetos comerciais

### 🎯 Objetivos Educacionais

Este sistema foi desenvolvido com o objetivo de:
- 📊 Facilitar a avaliação entre pares em projetos de equipe
- 🎓 Promover a transparência e feedback construtivo
- 💻 Demonstrar aplicação prática de conceitos de desenvolvimento de software
- 🔒 Garantir confidencialidade e anonimato nas avaliações

---

**Desenvolvido com ❤️ para a disciplina de Práticas Extensionistas V - Engenharia de Software**
