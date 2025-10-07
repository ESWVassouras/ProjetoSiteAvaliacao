import psycopg2
import psycopg2.extras
import os
from datetime import datetime
from config import USE_NEON_DB, NEON_CONFIG, NEON_CONNECTION_STRING

class DatabaseManager:
    def __init__(self, db_path=None):
        # Usar sempre NeonSQL (PostgreSQL)
        print("✅ Conectando ao banco NeonSQL (PostgreSQL)")
        self.connection = None
        self.init_database()
    
    def get_connection(self):
        """Obtém conexão com o banco de dados NeonSQL"""
        return psycopg2.connect(
            host=NEON_CONFIG['host'],
            port=NEON_CONFIG['port'],
            database=NEON_CONFIG['database'],
            user=NEON_CONFIG['user'],
            password=NEON_CONFIG['password'],
            sslmode=NEON_CONFIG['sslmode']
        )
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # PostgreSQL - Tabela de professores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS professores (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # PostgreSQL - Tabela de equipes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS equipes (
                    id SERIAL PRIMARY KEY,
                    nome_equipe VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # PostgreSQL - Tabela de avaliações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS avaliacoes (
                    id SERIAL PRIMARY KEY,
                    avaliador_nome VARCHAR(255) NOT NULL,
                    avaliador_matricula VARCHAR(255) NOT NULL,
                    nome_equipe VARCHAR(255) NOT NULL,
                    avaliado_nome VARCHAR(255) NOT NULL,
                    pontuacao INTEGER NOT NULL CHECK (pontuacao >= 0 AND pontuacao <= 2),
                    comprometimento BOOLEAN DEFAULT FALSE,
                    trabalho_equipe BOOLEAN DEFAULT FALSE,
                    qualidade_entregas BOOLEAN DEFAULT FALSE,
                    proatividade BOOLEAN DEFAULT FALSE,
                    cumprimento_responsabilidades BOOLEAN DEFAULT FALSE,
                    comentario TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Verificar se existe pelo menos um professor cadastrado
            cursor.execute('SELECT COUNT(*) FROM professores')
            count = cursor.fetchone()[0]
            
            # Se não houver nenhum professor, criar um com senha padrão
            if count == 0:
                import bcrypt
                # Senha padrão para o primeiro professor (deve ser alterada após o primeiro login)
                default_password = 'professor123'
                password_hash = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                cursor.execute('''
                    INSERT INTO professores (username, password_hash) 
                    VALUES (%s, %s)
                ''', ('professor', password_hash))
                
                print("⚠️  ATENÇÃO: Usuário professor criado com senha padrão 'professor123'")
                print("⚠️  ALTERE A SENHA APÓS O PRIMEIRO LOGIN POR SEGURANÇA!")
            
            conn.commit()
            conn.close()
            
            # Migrar equipes existentes da tabela avaliacoes para a tabela equipes
            self.migrar_equipes_existentes()
            
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def alterar_senha_professor(self, username, nova_senha):
        """Altera a senha de um professor"""
        import bcrypt
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Gerar hash da nova senha
            password_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Atualizar senha no banco
            if self.use_neon:
                cursor.execute('''
                    UPDATE professores 
                    SET password_hash = %s 
                    WHERE username = %s
                ''', (password_hash, username))
            else:
                cursor.execute('''
                    UPDATE professores 
                    SET password_hash = ? 
                    WHERE username = ?
                ''', (password_hash, username))
            
            conn.commit()
            print(f"Senha do professor '{username}' alterada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao alterar senha: {e}")
            return False
        finally:
            conn.close()
    
    def verificar_login_professor(self, username, password):
        """Verifica se o login do professor está correto"""
        import bcrypt
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT password_hash FROM professores WHERE username = %s', (username,))
            
            result = cursor.fetchone()
            
            if result:
                try:
                    # Verificar se o hash é válido
                    stored_hash = result[0]
                    if isinstance(stored_hash, str):
                        stored_hash = stored_hash.encode('utf-8')
                    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
                except Exception as e:
                    print(f"Erro na verificação da senha: {e}")
                    return False
            return False
        except Exception as e:
            print(f"Erro ao verificar login: {e}")
            return False
        finally:
            conn.close()
    
    def salvar_avaliacao(self, dados_avaliacao):
        """Salva uma avaliação no banco de dados"""
        # Primeiro, salvar a equipe se não existir
        self.salvar_equipe(dados_avaliacao['nome_equipe'])
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO avaliacoes (
                    avaliador_nome, avaliador_matricula, nome_equipe, avaliado_nome,
                    pontuacao, comprometimento, trabalho_equipe, qualidade_entregas,
                    proatividade, cumprimento_responsabilidades, comentario
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                dados_avaliacao['avaliador_nome'],
                dados_avaliacao['avaliador_matricula'],
                dados_avaliacao['nome_equipe'],
                dados_avaliacao['avaliado_nome'],
                dados_avaliacao['pontuacao'],
                dados_avaliacao['comprometimento'],
                dados_avaliacao['trabalho_equipe'],
                dados_avaliacao['qualidade_entregas'],
                dados_avaliacao['proatividade'],
                dados_avaliacao['cumprimento_responsabilidades'],
                dados_avaliacao.get('comentario', '')
            ))
            result = cursor.fetchone()
            conn.commit()
            return result[0] if result else None
        except Exception as e:
            print(f"Erro ao salvar avaliação: {e}")
            raise
        finally:
            conn.close()
    
    def obter_todas_avaliacoes(self):
        """Obtém todas as avaliações para o dashboard do professor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM avaliacoes ORDER BY created_at DESC
            ''')
            
            colunas = [desc[0] for desc in cursor.description]
            dados = cursor.fetchall()
            
            return colunas, dados
        except Exception as e:
            print(f"Erro ao obter avaliações: {e}")
            return [], []
        finally:
            conn.close()
    
    def obter_estatisticas(self):
        """Obtém estatísticas das avaliações"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Total de avaliações
            cursor.execute('SELECT COUNT(*) FROM avaliacoes')
            total_avaliacoes = cursor.fetchone()[0]
            
            # Total de avaliadores únicos
            cursor.execute('SELECT COUNT(DISTINCT avaliador_nome) FROM avaliacoes')
            total_avaliadores = cursor.fetchone()[0]
            
            # Total de equipes
            cursor.execute('SELECT COUNT(DISTINCT nome_equipe) FROM avaliacoes')
            total_equipes = cursor.fetchone()[0]
            
            # Média de pontuação
            cursor.execute('SELECT AVG(pontuacao) FROM avaliacoes')
            media_pontuacao = cursor.fetchone()[0] or 0
            
            return {
                'total_avaliacoes': total_avaliacoes,
                'total_avaliadores': total_avaliadores,
                'total_equipes': total_equipes,
                'media_pontuacao': round(float(media_pontuacao), 2)
            }
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {
                'total_avaliacoes': 0,
                'total_avaliadores': 0,
                'total_equipes': 0,
                'media_pontuacao': 0
            }
        finally:
            conn.close()
    
    def deletar_todas_avaliacoes(self):
        """Deleta todas as avaliações do banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM avaliacoes')
            deleted_count = cursor.rowcount
            
            conn.commit()
            return deleted_count
        except Exception as e:
            print(f"Erro ao deletar todas as avaliações: {e}")
            return 0
        finally:
            conn.close()
    
    def deletar_avaliacao_por_id(self, avaliacao_id):
        """Deleta uma avaliação específica pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM avaliacoes WHERE id = %s', (avaliacao_id,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            
            return deleted_count > 0
        except Exception as e:
            print(f"Erro ao deletar avaliação: {e}")
            return False
        finally:
            conn.close()
    
    def migrar_equipes_existentes(self):
        """Migra equipes existentes da tabela avaliacoes para a tabela equipes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Buscar todas as equipes distintas da tabela avaliacoes
            cursor.execute('SELECT DISTINCT nome_equipe FROM avaliacoes')
            equipes_avaliacoes = cursor.fetchall()
            
            # Inserir cada equipe na tabela equipes se não existir
            for (nome_equipe,) in equipes_avaliacoes:
                if nome_equipe and nome_equipe.strip():  # Verificar se não é vazio
                    cursor.execute('SELECT COUNT(*) FROM equipes WHERE nome_equipe = %s', (nome_equipe,))
                    count = cursor.fetchone()[0]
                    
                    if count == 0:  # Se não existir, inserir
                        cursor.execute('INSERT INTO equipes (nome_equipe) VALUES (%s)', (nome_equipe,))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao migrar equipes: {e}")
        finally:
            conn.close()
    
    def salvar_equipe(self, nome_equipe):
        """Salva uma equipe na tabela equipes se não existir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se a equipe já existe
            cursor.execute('SELECT COUNT(*) FROM equipes WHERE nome_equipe = %s', (nome_equipe,))
            count = cursor.fetchone()[0]
            
            # Se não existir, inserir
            if count == 0:
                cursor.execute('''
                    INSERT INTO equipes (nome_equipe) 
                    VALUES (%s)
                ''', (nome_equipe,))
                
                conn.commit()
            
        except Exception as e:
            print(f"Erro ao salvar equipe: {e}")
        finally:
            conn.close()
    
    def obter_sugestoes_equipes(self, texto_parcial=""):
        """Obtém sugestões de nomes de equipes baseado no texto parcial"""
        if not texto_parcial or len(texto_parcial) < 2:
            return []
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Buscar todas as equipes primeiro
            cursor.execute('SELECT nome_equipe FROM equipes ORDER BY nome_equipe')
            todas_equipes = [row[0] for row in cursor.fetchall()]
            
            # Filtrar manualmente (mais simples)
            sugestoes = []
            texto_lower = texto_parcial.lower()
            
            for equipe in todas_equipes:
                if texto_lower in equipe.lower():
                    sugestoes.append(equipe)
            
            return sugestoes[:10]  # Limitar a 10 sugestões
            
        except Exception as e:
            print(f"Erro ao obter sugestões de equipes: {e}")
            return []
        finally:
            conn.close()
    
    def listar_todas_equipes(self):
        """Lista todas as equipes cadastradas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT nome_equipe FROM equipes ORDER BY nome_equipe')
            resultados = cursor.fetchall()
            return [resultado[0] for resultado in resultados]
            
        except Exception as e:
            print(f"Erro ao listar equipes: {e}")
            return []
        finally:
            conn.close()
    
    def deletar_todas_equipes(self):
        """Deleta todas as equipes do banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM equipes')
            deleted_count = cursor.rowcount
            
            conn.commit()
            return deleted_count
        except Exception as e:
            print(f"Erro ao deletar todas as equipes: {e}")
            return 0
        finally:
            conn.close()
    
    def deletar_equipe_por_nome(self, nome_equipe):
        """Deleta uma equipe específica pelo nome"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM equipes WHERE nome_equipe = %s', (nome_equipe,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            
            return deleted_count > 0
        except Exception as e:
            print(f"Erro ao deletar equipe: {e}")
            return False
        finally:
            conn.close()
    
    def obter_estatisticas_por_aluno(self, nome_aluno=None):
        """Obtém estatísticas das avaliações por aluno específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if nome_aluno:
                # Estatísticas para um aluno específico
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_avaliacoes,
                        AVG(pontuacao) as media_pontuacao,
                        SUM(CASE WHEN pontuacao = 2 THEN 1 ELSE 0 END) as pontuacao_2,
                        SUM(CASE WHEN pontuacao = 1 THEN 1 ELSE 0 END) as pontuacao_1,
                        SUM(CASE WHEN pontuacao = 0 THEN 1 ELSE 0 END) as pontuacao_0
                    FROM avaliacoes 
                    WHERE avaliado_nome = %s OR avaliado_nome = %s
                ''', (nome_aluno, nome_aluno))
                
                result = cursor.fetchone()
                
                if result and result[0] > 0:
                    return {
                        'aluno': nome_aluno,
                        'total_avaliacoes': result[0],
                        'media_pontuacao': round(float(result[1] or 0), 2),
                        'pontuacao_2': result[2],
                        'pontuacao_1': result[3],
                        'pontuacao_0': result[4]
                    }
                else:
                    return {
                        'aluno': nome_aluno,
                        'total_avaliacoes': 0,
                        'media_pontuacao': 0,
                        'pontuacao_2': 0,
                        'pontuacao_1': 0,
                        'pontuacao_0': 0
                    }
            else:
                # Estatísticas para todos os alunos
                cursor.execute('''
                    SELECT 
                        avaliado_nome,
                        COUNT(*) as total_avaliacoes,
                        AVG(pontuacao) as media_pontuacao
                    FROM avaliacoes 
                    GROUP BY avaliado_nome
                    ORDER BY media_pontuacao DESC, total_avaliacoes DESC
                ''')
                
                results = cursor.fetchall()
                return [
                    {
                        'aluno': row[0],
                        'total_avaliacoes': row[1],
                        'media_pontuacao': round(float(row[2] or 0), 2)
                    }
                    for row in results
                ]
                
        except Exception as e:
            print(f"Erro ao obter estatísticas por aluno: {e}")
            return []
        finally:
            conn.close()
    
    def obter_lista_alunos_avaliados(self):
        """Obtém lista de todos os alunos que foram avaliados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT DISTINCT avaliado_nome FROM avaliacoes ORDER BY avaliado_nome')
            results = cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            print(f"Erro ao obter lista de alunos: {e}")
            return []
        finally:
            conn.close()

# Lista de todos os alunos
ALUNOS = [
    "Alexander Nunes Guido",
    "Alexia Sousa Ramos Oliveira", 
    "Amanda Nick de Oliveira Caldas",
    "Ana Carolina Gomes Soares",
    "Ana Carolina Mendes de Sousa Silva",
    "Ana Clara Moledo Neves",
    "Bruno Barral Palmeira",
    "Caio Correia Duque",
    "Caio Magalhães",
    "Caio Marques Lourenço",
    "Cauã Victor Pereira do Nascimento",
    "Daniel Alvarez gonçalves",
    "Daniel Augusto Ribeiro Oliveira",
    "Daniel Cardoso da Silva",
    "Deyvison Fonseca de Miranda",
    "Élisson Jorge de Brito Conceição",
    "Erika Sebould Gomes Pereira",
    "Fábio Figueiredo",
    "Francisco Miguez Bigio",
    "Gabriel Cardoso de Lemos",
    "Gabriel Martins Giglio",
    "Gabriel Miquelam Carvalho Knust",
    "Gabriel Silva Santana",
    "Gabriel Teixeira",
    "Gabriel Velasco Leonel",
    "Guilherme Viana Ramos Mello",
    "Hendryl Alves",
    "Ian Shtorache Cabral",
    "Igor de Oliveira Barata",
    "Jeferson Rosa",
    "João Victor Santos Borges",
    "João Matheus Moraes Bonato da Costa",
    "João Pedro Portela",
    "João Victor Oliveira da Silva",
    "João Vitor Cleto",
    "José Felipe de Mattos Alves",
    "Kauã Mendes da Silva",
    "Luana de Pinho Zenha",
    "Lucas Oliveira Mendes de Marins",
    "Lucas Valença Oliveira",
    "Lucas de Santana",
    "Marlon da Silva Machado",
    "Matheus Beiruth",
    "Matheus Campos",
    "Mizael Marques",
    "Moizes Baptista da Silva",
    "Nathan Inacio de Oliveira",
    "Patrick Oliveira",
    "Paulo Victor Silva Gonçalves",
    "Pedro Timon da Costa",
    "Rafael Dias",
    "Ramon Souza",
    "Renan Monteiro Silva",
    "Richarle Fagunde do Amaral",
    "Ruan Abreu Frederico Pereira",
    "Sara Macharete da Silva",
    "Sergio Murilo Nogueira",
    "Sky Crizosti",
    "Thiago Marinho da Silva",
    "Victor Hugo Reis Alves",
    "Vitor Amparo",
    "Vitor Emanuel Nunes",
    "Vitória Alves Pinheiro",
    "Wesley Bastos",
    "Yago da Costa Jardim",
    "Yago Ferreira Correa",
    "Yuri Ferraz de Almeida de Souza"
]
