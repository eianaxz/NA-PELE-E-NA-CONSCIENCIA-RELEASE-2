import sqlite3
from typing import Optional, Tuple, Dict, Any

class Database:
    def __init__(self, db_name: str = "usuarios1.db") -> None:
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self) -> None:
        """Estabelece uma nova conexão com o banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def _ensure_connection(self) -> None:
        """Garante que a conexão esteja ativa"""
        if self.conn is None:
            self._connect()

    def create_table(self) -> None:
        """Cria a tabela de usuários se não existir"""
        try:
            self._ensure_connection()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    apelido TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")
            raise

    def obter_apelido(self, email: str) -> Optional[str]:
        """Obtém o apelido do usuário pelo email"""
        try:
            self._ensure_connection()
            self.cursor.execute("SELECT apelido FROM usuarios WHERE email = ?", (email,))
            resultado = self.cursor.fetchone()
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            print(f"Erro ao obter apelido: {e}")
            return None

    def verificar_email_existente(self, email: str) -> bool:
        """Verifica se um email já está cadastrado"""
        try:
            self._ensure_connection()
            self.cursor.execute('SELECT 1 FROM usuarios WHERE email = ?', (email,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Erro ao verificar email: {e}")
            return False

    def verificar_apelido_existente(self, apelido: str) -> bool:
        """Verifica se um apelido já está cadastrado"""
        try:
            self._ensure_connection()
            self.cursor.execute('SELECT 1 FROM usuarios WHERE apelido = ?', (apelido,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Erro ao verificar apelido: {e}")
            return False

    def inserir_usuario(self, nome: str, apelido: str, email: str, senha: str) -> bool:
        """Insere um novo usuário no banco de dados"""
        try:
            self._ensure_connection()
            self.cursor.execute('''
                INSERT INTO usuarios (nome, apelido, email, senha)
                VALUES (?, ?, ?, ?)
            ''', (nome, apelido, email, senha))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Erro de integridade ao inserir usuário: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao inserir usuário: {e}")
            return False

    def verificar_credenciais(self, email: str, senha: str) -> bool:
        """Verifica se as credenciais de login são válidas"""
        try:
            self._ensure_connection()
            self.cursor.execute('SELECT 1 FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Erro ao verificar credenciais: {e}")
            return False

    def obter_senha_atual(self, email: str) -> Optional[str]:
        """Obtém a senha atual de um usuário"""
        try:
            self._ensure_connection()
            self.cursor.execute('SELECT senha FROM usuarios WHERE email = ?', (email,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Erro ao obter senha: {e}")
            return None

    def atualizar_senha(self, email: str, nova_senha: str) -> bool:
        """Atualiza a senha de um usuário"""
        try:
            self._ensure_connection()
            self.cursor.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha, email))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar senha: {e}")
            return False

    def close(self) -> None:
        """Fecha a conexão com o banco de dados"""
        try:
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao fechar conexão: {e}")
        finally:
            self.conn = None
            self.cursor = None

    def __enter__(self):
        self._ensure_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        """Destrutor que garante o fechamento da conexão"""
        self.close()

        