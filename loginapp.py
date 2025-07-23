from PySide6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QCheckBox, 
                              QMessageBox, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QFile
from datetime import datetime, timedelta
import random
import re
from database import Database
from menuapp import MenuScreen 

class LoginScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Na Pele e na Consciência - Login")
        self.setFixedSize(1700, 950)
        
        # Configurações
        self.parent_window = parent
        self.db = parent.db if parent else Database()
        self.tentativas_senha = 0
        self.email_verificado = None
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(0)
        
        # Espaçamento superior
        main_layout.addItem(QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Container do formulário
        form_container = QWidget()
        form_container.setMaximumWidth(600)
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(0, 0, 0, 0)

        

        # Campo Email
        self.email_label = QLabel("Email:")
        self.email_label.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email cadastrado")
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #F06292, 
                                            stop:0.5 #FFD54F, 
                                            stop:1 #8E24AA);
                border: 1px solid white;
                border-radius: 15px;
                padding: 10px;
                color: white;
                font-size: 16px;
                font-family: 'Arial';
            }
        """)
        self.email_input.setFixedSize(400, 45)
        
        email_container = QWidget()
        email_layout = QVBoxLayout(email_container)
        email_layout.addWidget(self.email_label)
        email_layout.addWidget(self.email_input)
        form_layout.addWidget(email_container)

        # Campo Senha (visível desde o início)
        self.senha_label = QLabel("Senha:")
        self.senha_label.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Digite sua senha")
        self.senha_input.setEchoMode(QLineEdit.Password)
        self.senha_input.setStyleSheet(self.email_input.styleSheet())
        self.senha_input.setFixedSize(400, 45)
        
        senha_container = QWidget()
        senha_layout = QVBoxLayout(senha_container)
        senha_layout.addWidget(self.senha_label)
        senha_layout.addWidget(self.senha_input)
        form_layout.addWidget(senha_container)

        # Checkbox Mostrar Senha (visível desde o início)
        self.show_password_checkbox = QCheckBox("Mostrar Senha")
        self.show_password_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 16px;
                font-family: 'Arial';
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid white;
                border-radius: 5px;
                background-color: transparent;
            }
            QCheckBox::indicator:checked {
                background-color: white;
            }
        """)
        self.show_password_checkbox.stateChanged.connect(self._toggle_password_visibility)
        form_layout.addWidget(self.show_password_checkbox, 0, Qt.AlignLeft)

        # Botão Esqueceu Senha (oculto inicialmente)
        self.forgot_password_button = QPushButton("Esqueceu Senha?")
        self.forgot_password_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 16px;
                font-family: 'Arial';
                text-decoration: underline;
                background: transparent;
                border: none;
                padding: 0;
                margin-top: 10px;
            }
            QPushButton:hover {
                color: #FFD54F;
            }
        """)
        self.forgot_password_button.setVisible(False)
        self.forgot_password_button.clicked.connect(self._show_forgot_password_screen)
        form_layout.addWidget(self.forgot_password_button, 0, Qt.AlignLeft)

        # Container para os botões (Voltar e Entrar)
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 30, 0, 0)
        buttons_layout.setSpacing(20)
        
        # Botão VOLTAR
        self.back_button = QPushButton("VOLTAR")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #6D6D6D, 
                                            stop:0.5 #9E9E9E, 
                                            stop:1 #6D6D6D);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px 25px;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Arial';
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #8E8E8E, 
                                            stop:0.5 #BEBEBE, 
                                            stop:1 #8E8E8E);
            }
        """)
        self.back_button.setFixedSize(150, 50)
        self.back_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.back_button)
        
        # Botão ENTRAR
        self.enter_button = QPushButton("ENTRAR")
        self.enter_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #F06292, 
                                            stop:0.5 #FFD54F, 
                                            stop:1 #8E24AA);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px 25px;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Arial';
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #FF80AB, 
                                            stop:0.5 #FFEB3B, 
                                            stop:1 #AB47BC);
            }
        """)
        self.enter_button.setFixedSize(150, 50)
        self.enter_button.clicked.connect(self._verify_login)
        buttons_layout.addWidget(self.enter_button)
        
        buttons_layout.addStretch()
        form_layout.addWidget(buttons_container)

        main_layout.addWidget(form_container)
        
        # Espaçamento inferior
        main_layout.addItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Configurar fundo
        caminho_imagem = r"C:\Users\Clara\OneDrive\Área de Trabalho\KIVY\NA PELE E NA CONSCIÊNCIA (5).png"
        if QFile.exists(caminho_imagem):
            self.background_pixmap = QPixmap(caminho_imagem)
            self.setStyleSheet("background: transparent;")
        else:
            self.background_pixmap = None

        # Conectar eventos
        self.email_input.returnPressed.connect(lambda: self._verify_email(show_message=True))

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background_pixmap and not self.background_pixmap.isNull():
            painter.drawPixmap(self.rect(), self.background_pixmap)
        else:
            painter.fillRect(self.rect(), QColor(50, 50, 50))

    def _toggle_password_visibility(self, state):
        self.senha_input.setEchoMode(QLineEdit.Normal if state == Qt.Checked else QLineEdit.Password)

    def _verify_email(self, show_message=False):
        email = self.email_input.text().strip()
        
        if not email:
            self._show_message("Campo Vazio", "Por favor, digite seu email.", QMessageBox.Warning)
            return False
        
        if not self.db.verificar_email_existente(email):
            self._show_message("Email Não Cadastrado", "Email não cadastrado, volte e efetue seu cadastro.", QMessageBox.Warning)
            return False
        
        self.email_verificado = email
        self.senha_input.setFocus()
        
        if show_message:
            self._show_message("Email Verificado", "Email verificado com sucesso. Agora digite sua senha.", QMessageBox.Information)
        
        return True

    def _verify_login(self):
        if not hasattr(self, 'email_verificado') or not self.email_verificado:
            if not self._verify_email(show_message=True):
                return
    
        senha = self.senha_input.text()
    
        if not senha:
            self._show_message("Campo Vazio", "Por favor, digite sua senha.", QMessageBox.Warning)
            return
    
        if self.db.verificar_credenciais(self.email_verificado, senha):
        # Obter o apelido do usuário do banco de dados
            apelido = self.db.obter_apelido(self.email_verificado)
            if apelido:
            # Fechar a janela de login e abrir o menu
                self.menu = MenuScreen(apelido)  # Cria a tela de menu
                self.menu.show()                 # Mostra o menu
                self.close()                     # Fecha a tela de login atual
        else:
            self._handle_failed_login()
            self.forgot_password_button.setVisible(True)

    def _handle_failed_login(self):
        self.tentativas_senha += 1
        tentativas_restantes = 3 - self.tentativas_senha
        
        if self.tentativas_senha >= 3:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Tentativas Esgotadas")
            msg.setText(f"Você excedeu o número máximo de tentativas!")
            msg.setInformativeText(f"Tentativas realizadas: {self.tentativas_senha}\nTentativas restantes: 0\nSerá necessário redefinir sua senha.")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #333333;
                }
                QMessageBox QLabel {
                    color: white;
                }
            """)
            msg.exec_()
            self._show_reset_password_screen()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Senha Incorreta")
            msg.setText("Senha incorreta!")
            msg.setInformativeText(f"Tentativas realizadas: {self.tentativas_senha}\nTentativas restantes: {tentativas_restantes}")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #333333;
                }
                QMessageBox QLabel {
                    color: white;
                }
            """)
            msg.exec_()
            self.senha_input.clear()
            self.senha_input.setFocus()

    def _show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #333333;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #555555;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #777777;
            }
        """)
        msg.exec_()

    def _show_forgot_password_screen(self):
        self._show_reset_password_screen()

    def _show_reset_password_screen(self):
        reset_dialog = QDialog(self)
        reset_dialog.setWindowTitle("Redefinir Senha")
        reset_dialog.setFixedSize(500, 400)
        
        if hasattr(self, 'background_pixmap') and self.background_pixmap:
            reset_dialog.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(reset_dialog)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        titulo = QLabel("REDEFINIR SENHA")
        titulo.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 30px;
            }
        """)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Nova Senha
        nova_senha_label = QLabel("Nova Senha (6 dígitos - apenas números e caracteres especiais):")
        nova_senha_label.setStyleSheet("color: white; font-size: 16px;")
        nova_senha_input = QLineEdit()
        nova_senha_input.setEchoMode(QLineEdit.Password)
        nova_senha_input.setStyleSheet(self.email_input.styleSheet())
        nova_senha_input.setFixedSize(350, 45)
        nova_senha_input.setMaxLength(6)
        
        # Confirmar Senha
        confirmar_senha_label = QLabel("Confirmar Nova Senha:")
        confirmar_senha_label.setStyleSheet("color: white; font-size: 16px;")
        confirmar_senha_input = QLineEdit()
        confirmar_senha_input.setEchoMode(QLineEdit.Password)
        confirmar_senha_input.setStyleSheet(self.email_input.styleSheet())
        confirmar_senha_input.setFixedSize(350, 45)
        confirmar_senha_input.setMaxLength(6)
        
        # Checkbox Mostrar Senha
        show_password = QCheckBox("Mostrar Senha")
        show_password.setStyleSheet(self.show_password_checkbox.styleSheet())
        show_password.stateChanged.connect(lambda state: (
            nova_senha_input.setEchoMode(QLineEdit.Normal if state else QLineEdit.Password),
            confirmar_senha_input.setEchoMode(QLineEdit.Normal if state else QLineEdit.Password)
        ))
        
        # Botão Enviar Código
        enviar_button = QPushButton("ENVIAR CÓDIGO")
        enviar_button.setStyleSheet(self.enter_button.styleSheet())
        enviar_button.setFixedSize(200, 50)
        
        layout.addWidget(nova_senha_label)
        layout.addWidget(nova_senha_input)
        layout.addWidget(confirmar_senha_label)
        layout.addWidget(confirmar_senha_input)
        layout.addWidget(show_password, 0, Qt.AlignLeft)
        layout.addSpacing(20)
        layout.addWidget(enviar_button, 0, Qt.AlignCenter)
        
        # Função para validar a senha
        def validar_senha(senha):
            # Verifica se tem exatamente 6 caracteres
            if len(senha) != 6:
                return False
            
            # Verifica se contém apenas números e caracteres especiais
            if not re.match(r'^[\d\W_]+$', senha):
                return False
                
            return True
        
        # Função para enviar código
        def send_code():
            nova_senha = nova_senha_input.text()
            confirmar_senha = confirmar_senha_input.text()
            
            if not nova_senha or not confirmar_senha:
                self._show_message("Campos Vazios", "Preencha ambos os campos de senha.", QMessageBox.Warning)
                return
                
            if nova_senha != confirmar_senha:
                self._show_message("Senhas Diferentes", "As senhas não coincidem.", QMessageBox.Warning)
                return
                
            if not validar_senha(nova_senha):
                self._show_message("Senha Inválida", 
                                 "A senha deve conter exatamente 6 caracteres,\n"
                                 "compostos apenas por números e caracteres especiais.", QMessageBox.Warning)
                return
                
            self.codigo_reset = str(random.randint(100000, 999999))
            self.codigo_valido_ate = datetime.now() + timedelta(minutes=5)
            
            if self.parent_window.enviar_codigo_email(self.email_verificado, self.codigo_reset):
                reset_dialog.close()
                self._show_verify_code_screen(nova_senha)
            else:
                self._show_message("Erro", "Falha ao enviar código.", QMessageBox.Critical)
        
        enviar_button.clicked.connect(send_code)
        
        reset_dialog.exec_()

    def _show_verify_code_screen(self, nova_senha):
        verify_dialog = QDialog(self)
        verify_dialog.setWindowTitle("Verificação de Código")
        verify_dialog.setFixedSize(500, 400)
        
        if hasattr(self, 'background_pixmap') and self.background_pixmap:
            verify_dialog.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(verify_dialog)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        titulo = QLabel("VERIFICAÇÃO DE CÓDIGO")
        titulo.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 30px;
            }
        """)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        instrucao = QLabel(f"Enviamos um código de 6 dígitos para:\n{self.email_verificado}")
        instrucao.setStyleSheet("color: white; font-size: 14px; text-align: center;")
        layout.addWidget(instrucao)
        
        codigo_input = QLineEdit()
        codigo_input.setPlaceholderText("Digite o código")
        codigo_input.setMaxLength(6)
        codigo_input.setAlignment(Qt.AlignCenter)
        codigo_input.setStyleSheet(self.email_input.styleSheet())
        codigo_input.setFixedSize(200, 45)
        layout.addWidget(codigo_input, 0, Qt.AlignCenter)
        
        # Botão Verificar
        verify_button = QPushButton("VERIFICAR")
        verify_button.setStyleSheet(self.enter_button.styleSheet())
        verify_button.setFixedSize(200, 50)
        
        # Botão Reenviar
        resend_button = QPushButton("Reenviar Código")
        resend_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 12px;
                text-decoration: underline;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                color: #FFD54F;
            }
        """)
        
        layout.addWidget(verify_button, 0, Qt.AlignCenter)
        layout.addWidget(resend_button, 0, Qt.AlignCenter)
        
        # Função de verificação
        def verify_code():
            codigo = codigo_input.text()
            
            if len(codigo) != 6 or not codigo.isdigit():
                self._show_message("Código Inválido", "Digite um código de 6 dígitos.", QMessageBox.Warning)
                return
                
            if datetime.now() > self.codigo_valido_ate:
                self._show_message("Código Expirado", "Solicite um novo código.", QMessageBox.Warning)
                return
                
            if codigo == self.codigo_reset:
                if self.db.atualizar_senha(self.email_verificado, nova_senha):
                    self._show_message("Sucesso", "Senha redefinida com sucesso!", QMessageBox.Information)
                    verify_dialog.close()
                    self.tentativas_senha = 0
                else:
                    self._show_message("Erro", "Falha ao atualizar senha.", QMessageBox.Critical)
            else:
                self._show_message("Código Incorreto", "Verifique o código digitado.", QMessageBox.Warning)
        
        # Função para reenviar
        def resend_code():
            self.codigo_reset = str(random.randint(100000, 999999))
            self.codigo_valido_ate = datetime.now() + timedelta(minutes=5)
            
            if self.parent_window.enviar_codigo_email(self.email_verificado, self.codigo_reset):
                self._show_message("Sucesso", "Novo código enviado!", QMessageBox.Information)
            else:
                self._show_message("Erro", "Falha ao reenviar código.", QMessageBox.Critical)
        
        verify_button.clicked.connect(verify_code)
        resend_button.clicked.connect(resend_code)
        
        verify_dialog.exec()


