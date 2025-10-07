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
- Conta no NeonSQL (para banco de dados)

### Instalação

1. **Clone ou baixe os arquivos do projeto**

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Sistema pronto para uso!**
   
   **✅ Não é necessário configurar nada!** O sistema já está configurado para usar o banco NeonSQL automaticamente.

4. **Execute o sistema:**
   ```bash
   streamlit run app.py
   ```

5. **Acesse no navegador:**
   - A aplicação será aberta automaticamente em `http://localhost:8501`

## 🔐 Acesso do Professor

**Usuário:** `professor`  
**Senha:** Gerenciada diretamente no banco de dados NeonSQL

### 📝 Primeiro Acesso:
- **Usuário:** `professor`
- **Senha:** `professor123` (senha padrão)
- **⚠️ IMPORTANTE:** Altere a senha após o primeiro login por segurança!

### ⚠️ IMPORTANTE - SEGURANÇA

**NUNCA commite credenciais no código!** Este sistema foi desenvolvido com foco em segurança.

## 🚀 Deploy

### **Streamlit Cloud:**
1. **Faça push do código para o GitHub**
2. **Acesse seu app no Streamlit Cloud**
3. **Faça o deploy** - o sistema funcionará automaticamente!

**✅ Não é necessário configurar nada!** O sistema já está configurado para usar o NeonSQL.

### **🛡️ Boas Práticas de Segurança:**

- ✅ **Use senhas fortes** (mínimo 12 caracteres)
- ✅ **Mantenha as credenciais seguras**
- ✅ **Use variáveis de ambiente**
- ✅ **Revise as permissões de acesso**
- ❌ **NUNCA commite o arquivo .env**
- ❌ **NUNCA compartilhe credenciais**
- ❌ **NUNCA use senhas fracas**
- ❌ **NUNCA deixe credenciais no código**

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

O sistema utiliza **NeonSQL (PostgreSQL)** como banco de dados principal.

### **🔧 Configuração:**
- ✅ **Credenciais configuradas diretamente** no código
- ✅ **Conexão automática** com o banco NeonSQL
- ✅ **Funciona imediatamente** sem configuração adicional
- ✅ **Dados persistem** entre sessões e deploys

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
