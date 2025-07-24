
import sys
import re
import os
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from typing import Optional, Tuple, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QCheckBox, QMessageBox, QSpacerItem, QSizePolicy, QDialog)
from PySide6.QtGui import QPixmap, QPainter, QIcon, QFont, QLinearGradient, QColor
from PySide6.QtCore import QFile, Qt, QSize, QTimer

from loginapp import LoginScreen
from database import Database
# Carregar variáveis de ambiente
load_dotenv('cadastroapp.env')



class MinhaJanela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Na Pele e na Consciência - Painel de Acesso")
        self.setGeometry(0, 0, 1700, 950)
        
        # Configurações de email
        self.EMAIL_SENDER = os.getenv("EMAIL_SENDER")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
        
        if not all([self.EMAIL_SENDER, self.EMAIL_PASSWORD, self.SMTP_SERVER]):
            QMessageBox.critical(self, "Erro de Configuração", 
                               "Variáveis de ambiente não configuradas corretamente!")
            sys.exit(1)
        
        # Inicializar banco de dados
        self.db = Database()
        self.tentativas_login = 0
        self.janela_2fa = None
        self.dados_cadastro_temp = None
        self.current_field_index = 0
        self.background_pixmap = None

        caminho_imagem_fundo = r"C:/Users/Clara/OneDrive/Área de Trabalho/KIVY/NA PELE E NA CONSCIÊNCIA (1).png"
        caminho_icone_local = "C:/Users/Clara/OneDrive/Área de Trabalho/KIVY/logo.ico"
        caminho_checkmark_icon = "check.png"

        if not QFile.exists(caminho_imagem_fundo):
            QMessageBox.critical(self, "Erro de Imagem de Fundo",
                               f"A imagem de fundo não foi encontrada no caminho: \n{caminho_imagem_fundo}\n"
                               "Por favor, verifique o caminho e o nome do arquivo 'NA PELE E NA CONSCIÊNCIA (1).png'.")
            return

        self.background_pixmap = QPixmap(caminho_imagem_fundo)

        if self.background_pixmap.isNull():
            QMessageBox.critical(self, "Erro de Carregamento da Imagem de Fundo",
                               f"Não foi possível criar QPixmap a partir de: \n{caminho_imagem_fundo}\n"
                               "O arquivo pode estar corrompido ou em um formato não suportado pelo Qt.")
            self.background_pixmap = None

        if QFile.exists(caminho_icone_local):
            icone = QIcon(caminho_icone_local)
            self.setWindowIcon(icone)
        else:
            QMessageBox.warning(self, "Aviso de Ícone",
                              f"O ícone não foi encontrado no caminho: \n{caminho_icone_local}\n"
                              "A janela usará o ícone padrão do sistema.")

        self.setStyleSheet("QMainWindow { background: transparent; }")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(0)

        gradient_start_color = "#F06292"
        gradient_middle_color = "#FFD54F"
        gradient_end_color = "#8E24AA"

        self.form_stylesheet = f"""
            QLabel {{
                color: white;
                font-family: 'Arial';
                font-size: 16px;
                font-weight: normal;
            }}
            QLineEdit {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                                stop:0 {gradient_start_color}, 
                                                stop:0.5 {gradient_middle_color}, 
                                                stop:1 {gradient_end_color});
                border: 1px solid white;
                border-radius: 15px;
                padding: 10px;
                color: white;
                font-size: 14px;
                font-family: 'Arial';
            }}
            QPushButton {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                                stop:0 {gradient_start_color}, 
                                                stop:0.5 {gradient_middle_color}, 
                                                stop:1 {gradient_end_color});
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px 25px;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Arial';
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                                stop:0 #FF80AB, 
                                                stop:0.5 #FFEB3B, 
                                                stop:1 #AB47BC);
            }}
            QCheckBox {{
                color: white;
                font-size: 14px;
                font-family: 'Arial';
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid white;
                border-radius: 5px;
                background-color: transparent;
            }}
            QCheckBox::indicator:checked {{
                background-color: white;
                image: url({caminho_checkmark_icon});
            }}
        """
        central_widget.setStyleSheet(self.form_stylesheet)

        # Espaçamento grande no topo (40% da janela)
        top_spacer = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(top_spacer)

        # Novo container centralizado
        form_outer_container = QWidget()
        form_outer_layout = QHBoxLayout(form_outer_container)
        form_outer_layout.setContentsMargins(0, 0, 0, 0)
        form_outer_layout.addStretch()

        form_container = QWidget()
        form_container.setMaximumWidth(600)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(0, 0, 0, 0) 

        # Campos adicionados
        self.name_input = self._create_input_field("Nome:")
        self.apelido_input = self._create_input_field("Apelido:")
        self.email_input = self._create_input_field("Email:")
        self.senha_input = self._create_input_field("Senha:", is_password=True)
        self.confirm_senha_input = self._create_input_field("Confirme sua Senha:", is_password=True)
        
        # Inicialmente, mostrar apenas o primeiro campo
        self.name_input.setVisible(True)
        self.apelido_input.setVisible(False)
        self.email_input.setVisible(False)
        self.senha_input.setVisible(False)
        self.confirm_senha_input.setVisible(False)
        
        # Checkbox Mostrar Senha
        self.show_password_checkbox = QCheckBox("Mostrar Senha")
        self.show_password_checkbox.setVisible(False)
        self.show_password_checkbox.stateChanged.connect(self._toggle_password_visibility)
        
        # Adicionar checkbox ao layout com alinhamento à direita
        checkbox_container = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_container)
        checkbox_layout.addStretch()
        checkbox_layout.addWidget(self.show_password_checkbox)
        checkbox_layout.setContentsMargins(0, 0, 20, 0)
        
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.apelido_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.senha_input)
        form_layout.addWidget(self.confirm_senha_input)
        form_layout.addWidget(checkbox_container)

        form_outer_layout.addWidget(form_container)
        form_outer_layout.addStretch()
        main_layout.addWidget(form_outer_container)

        # Espaço entre formulário e botões
        middle_spacer = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(middle_spacer)

        # Botões
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(40)
        buttons_layout.addStretch()
        
        cadastrar_button = QPushButton("CADASTRAR")
        cadastrar_button.setFixedSize(200, 60)
        cadastrar_button.clicked.connect(self._register_user)
        buttons_layout.addWidget(cadastrar_button)

        login_button = QPushButton("LOGIN")
        login_button.setFixedSize(200, 60)
        login_button.clicked.connect(self._show_login_screen)
        buttons_layout.addWidget(login_button)
        buttons_layout.addStretch()

        main_layout.addWidget(buttons_container)

        # Espaço final
        bottom_spacer = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(bottom_spacer)
        
        # Mostrar critérios do primeiro campo após a janela estar totalmente carregada
        QTimer.singleShot(100, self.show_first_criteria)

    def gerar_codigo(self):
        return str(random.randint(100000, 999999))

    def enviar_codigo_email(self, destinatario, codigo):
        try:
            msg = MIMEText(
                f"Olá! Seja bem vindo (a) ao Na Pele e na Consciência\n Seu código de verificação é: {codigo}\n\nEste código é válido por 5 minutos.")
            msg['Subject'] = 'Código de Verificação - Na Pele e na Consciência'
            msg['From'] = self.EMAIL_SENDER
            msg['To'] = destinatario

            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
                server.sendmail(self.EMAIL_SENDER, destinatario, msg.as_string())
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False

    def criar_janela_2fa(self, nome, apelido, email, senha):
        self.janela_2fa = QDialog(self)
        self.janela_2fa.setWindowTitle("Autenticação em Duas Etapas")
        self.janela_2fa.setFixedSize(400, 350)

        QMessageBox.information(self, "Verificação Necessária",
                               f"Um código de verificação será enviado para:\n{email}\n\n"
                                "Por favor, verifique sua caixa de entrada para concluir o cadastro")
    
    # Configurar imagem de fundo
        caminho_imagem_fundo = r"C:/Users/Clara/OneDrive/Área de Trabalho/KIVY/NA PELE E NA CONSCIÊNCIA (3).png"
        if QFile.exists(caminho_imagem_fundo):
            self.janela_2fa.background_pixmap = QPixmap(caminho_imagem_fundo)
            self.janela_2fa.setStyleSheet("background: transparent;")
        else:
            QMessageBox.warning(self.janela_2fa, "Aviso", "Imagem de fundo não encontrada.")
            self.janela_2fa.background_pixmap = None
    
    # Armazenar dados temporários
        self.dados_cadastro_temp = {
            'nome': nome,
            'apelido': apelido,
            'email': email,
            'senha': senha
        }
    
    # Gerar e enviar código
        self.codigo_2fa = self.gerar_codigo()
        self.codigo_valido_ate = datetime.now() + timedelta(minutes=5)
    
        if not self.enviar_codigo_email(email, self.codigo_2fa):
            QMessageBox.critical(self.janela_2fa, "Erro", 
                           "Falha ao enviar código de verificação. Tente novamente.")
            self.janela_2fa.close()
            return
    
        layout = QVBoxLayout(self.janela_2fa)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(40)
    
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(top_spacer)
        
    
    # Campo de código
        self.codigo_entry = QLineEdit()
        self.codigo_entry.setMaxLength(6)
        self.codigo_entry.setAlignment(Qt.AlignCenter)
        self.codigo_entry.setStyleSheet("""
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
                min-width: 200px;
                max-width: 200px;
            }
        """)
        layout.addWidget(self.codigo_entry, 0, Qt.AlignCenter)
    
    # Botão de reenviar código
        btn_reenviar = QPushButton("Reenviar código de verificação")
        btn_reenviar.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 12px;
                font-family: 'Arial';
                text-decoration: underline;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                color: #FFD54F;
            }
        """)
        btn_reenviar.clicked.connect(self.solicitar_novo_codigo)
        layout.addWidget(btn_reenviar, 0, Qt.AlignCenter)
    
    # Botão de verificar
        btn_verificar = QPushButton("VERIFICAR CÓDIGO")
        btn_verificar.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #F06292, 
                                            stop:0.5 #FFD54F, 
                                            stop:1 #8E24AA);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px 25px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Arial';
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #FF80AB, 
                                            stop:0.5 #FFEB3B, 
                                            stop:1 #AB47BC);
            }
        """)
        btn_verificar.clicked.connect(self.verificar_codigo_2fa)
        layout.addWidget(btn_verificar, 0, Qt.AlignCenter)
    
    # Espaçador para empurrar tudo para cima
        layout.addStretch()
    
        def paintEvent(event):
            painter = QPainter(self.janela_2fa)
            if hasattr(self.janela_2fa, 'background_pixmap') and self.janela_2fa.background_pixmap and not self.janela_2fa.background_pixmap.isNull():
                painter.drawPixmap(self.janela_2fa.rect(), self.janela_2fa.background_pixmap)
            painter.end()
    
        self.janela_2fa.paintEvent = paintEvent
    
        self.janela_2fa.exec()

    def verificar_codigo_2fa(self):
        codigo_digitado = self.codigo_entry.text()
        
        if not codigo_digitado.isdigit() or len(codigo_digitado) != 6:
            QMessageBox.warning(self.janela_2fa, "Erro", 
                              "Código inválido. Deve conter 6 dígitos.")
            return
        
        if datetime.now() > self.codigo_valido_ate:
            QMessageBox.warning(self.janela_2fa, "Erro", 
                              "Código expirado. Solicite um novo.")
            return
        
        if codigo_digitado == self.codigo_2fa:
            try:
                if self.db.inserir_usuario(
                    self.dados_cadastro_temp['nome'],
                    self.dados_cadastro_temp['apelido'],
                    self.dados_cadastro_temp['email'],
                    self.dados_cadastro_temp['senha']
                ):
                    QMessageBox.information(self.janela_2fa, "Sucesso", 
                                          "Cadastro concluído com sucesso!")
                    self.janela_2fa.close()
                    # Limpar campos após cadastro bem-sucedido
                    self._limpar_campos_cadastro()
                else:
                    QMessageBox.critical(self.janela_2fa, "Erro", 
                                       "Falha ao cadastrar usuário. Email ou apelido já existente.")
            except Exception as e:
                QMessageBox.critical(self.janela_2fa, "Erro", 
                                   f"Erro ao cadastrar usuário: {str(e)}")
        else:
            QMessageBox.warning(self.janela_2fa, "Erro", 
                              "Código incorreto. Tente novamente.")

    def solicitar_novo_codigo(self):
        self.codigo_2fa = self.gerar_codigo()
        self.codigo_valido_ate = datetime.now() + timedelta(minutes=5)
        
        if self.enviar_codigo_email(self.dados_cadastro_temp['email'], self.codigo_2fa):
            QMessageBox.information(self.janela_2fa, "Sucesso", 
                                  "Novo código enviado para seu email!")
        else:
            QMessageBox.critical(self.janela_2fa, "Erro", 
                               "Falha ao enviar novo código. Tente novamente.")

    def verificar_login_2fa(self, email):
        """Verificação em duas etapas para login"""
        janela_2fa = QDialog(self)
        janela_2fa.setWindowTitle("Verificação de Segurança")
        janela_2fa.setFixedSize(400, 250)
        
        # Gerar e enviar código
        codigo = self.gerar_codigo()
        codigo_valido_ate = datetime.now() + timedelta(minutes=5)
        
        if not self.enviar_codigo_email(email, codigo):
            QMessageBox.critical(janela_2fa, "Erro", 
                               "Falha ao enviar código de verificação. Tente novamente.")
            return False
        
        layout = QVBoxLayout(janela_2fa)
        
        label_titulo = QLabel("🔒 Verificação de Segurança")
        label_titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label_titulo)
        
        label_info = QLabel(f"Enviamos um código de 6 dígitos para {email}.")
        layout.addWidget(label_info)
        
        label_instrucao = QLabel("Digite o código abaixo:")
        layout.addWidget(label_instrucao)
        
        codigo_entry = QLineEdit()
        codigo_entry.setMaxLength(6)
        codigo_entry.setAlignment(Qt.AlignCenter)
        layout.addWidget(codigo_entry)
        
        btn_verificar = QPushButton("Verificar")
        layout.addWidget(btn_verificar)
        
        btn_novo_codigo = QPushButton("Enviar novo código")
        layout.addWidget(btn_novo_codigo)
        
        label_validade = QLabel("O código é válido por 5 minutos.")
        label_validade.setStyleSheet("font-size: 10px;")
        layout.addWidget(label_validade)
        
        resultado = {'verificado': False}
        
        def verificar():
            codigo_digitado = codigo_entry.text()
            
            if not codigo_digitado.isdigit() or len(codigo_digitado) != 6:
                QMessageBox.warning(janela_2fa, "Erro", 
                                  "Código inválido. Deve conter 6 dígitos.")
                return
                
            if datetime.now() > codigo_valido_ate:
                QMessageBox.warning(janela_2fa, "Erro", 
                                  "Código expirado. Solicite um novo.")
                return
                
            if codigo_digitado == codigo:
                resultado['verificado'] = True
                janela_2fa.close()
            else:
                QMessageBox.warning(janela_2fa, "Erro", 
                                  "Código incorreto. Tente novamente.")
        
        def novo_codigo():
            nonlocal codigo, codigo_valido_ate
            codigo = self.gerar_codigo()
            codigo_valido_ate = datetime.now() + timedelta(minutes=5)
            
            if self.enviar_codigo_email(email, codigo):
                QMessageBox.information(janela_2fa, "Sucesso", 
                                      "Novo código enviado para seu email!")
            else:
                QMessageBox.critical(janela_2fa, "Erro", 
                                   "Falha ao enviar novo código. Tente novamente.")
        
        btn_verificar.clicked.connect(verificar)
        btn_novo_codigo.clicked.connect(novo_codigo)
        
        janela_2fa.exec_()
        return resultado['verificado']

    def _limpar_campos_cadastro(self):
        """Limpa todos os campos de cadastro e reseta a interface"""
        self.name_input.findChild(QLineEdit).clear()
        self.apelido_input.findChild(QLineEdit).clear()
        self.email_input.findChild(QLineEdit).clear()
        self.senha_input.findChild(QLineEdit).clear()
        self.confirm_senha_input.findChild(QLineEdit).clear()
        
        self.name_input.setVisible(True)
        self.apelido_input.setVisible(False)
        self.email_input.setVisible(False)
        self.senha_input.setVisible(False)
        self.confirm_senha_input.setVisible(False)
        self.show_password_checkbox.setVisible(False)
        self.show_password_checkbox.setChecked(False)
        self.current_field_index = 0

    def _show_login_screen(self):
        """Mostra a tela de login"""
        login_screen = LoginScreen(self)
        login_screen.exec()  # Isso agora é modal e não interfere com o menu

    def show_first_criteria(self):
        QMessageBox.information(self, "Critérios do Campo Nome", 
                              "Critérios para o campo Nome:\n"
                              "- Até 20 caracteres (espaços não contam)\n"
                              "- Somente letras maiúsculas ou minúsculas")
        
        # Conectar eventos de pressionar Enter
        self.name_input.findChild(QLineEdit).returnPressed.connect(self.validate_name)
        self.apelido_input.findChild(QLineEdit).returnPressed.connect(self.validate_apelido)
        self.email_input.findChild(QLineEdit).returnPressed.connect(self.validate_email)
        self.senha_input.findChild(QLineEdit).returnPressed.connect(self.validate_senha)
        self.confirm_senha_input.findChild(QLineEdit).returnPressed.connect(self.validate_confirm_senha)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background_pixmap and not self.background_pixmap.isNull():
            painter.drawPixmap(self.rect(), self.background_pixmap)
        else:
            painter.fillRect(self.rect(), self.palette().window().color())

    def _create_input_field(self, label_text, is_password=False):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(label_text)
        label.setFixedWidth(150)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        line_edit = QLineEdit()
        line_edit.setFixedSize(350, 45)
        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(label)
        layout.addWidget(line_edit)
        
        return container

    def _toggle_password_visibility(self, state):
        # Acessando os QLineEdit diretamente através de findChild
        senha_lineEdit = self.senha_input.findChild(QLineEdit)
        confirm_senha_lineEdit = self.confirm_senha_input.findChild(QLineEdit)

        if senha_lineEdit and confirm_senha_lineEdit:
            if state == Qt.Checked:
                senha_lineEdit.setEchoMode(QLineEdit.Normal)
                confirm_senha_lineEdit.setEchoMode(QLineEdit.Normal)
            else:
                senha_lineEdit.setEchoMode(QLineEdit.Password)
                confirm_senha_lineEdit.setEchoMode(QLineEdit.Password)

    def validate_name(self):
        name = self.name_input.findChild(QLineEdit).text().strip()
        name_no_spaces = name.replace(" ", "")
        
        if not name:
            QMessageBox.warning(self, "Campo Vazio", "Por favor, digite seu nome.")
            return
            
        if len(name_no_spaces) > 20:
            QMessageBox.warning(self, "Nome Inválido", "O nome deve ter até 20 caracteres (sem contar espaços).")
            return
            
        if not name_no_spaces.isalpha():
            QMessageBox.warning(self, "Nome Inválido", "O nome deve conter apenas letras (sem números ou caracteres especiais).")
            return
            
        # Nome válido, mostrar próximo campo
        self.apelido_input.setVisible(True)
        self.current_field_index = 1
        QMessageBox.information(self, "Critérios do Campo Apelido", 
                              "Critérios para o campo Apelido:\n"
                              "- Até 10 caracteres (espaços não são permitidos)\n"
                              "- Pode conter letras, números e caracteres especiais")

    def validate_apelido(self):
        apelido = self.apelido_input.findChild(QLineEdit).text().strip()
        
        if not apelido:
            QMessageBox.warning(self, "Campo Vazio", "Por favor, digite seu apelido.")
            return
            
        if " " in apelido:
            QMessageBox.warning(self, "Apelido Inválido", "O apelido não pode conter espaços.")
            return
            
        if len(apelido) > 10:
            QMessageBox.warning(self, "Apelido Inválido", "O apelido deve ter até 10 caracteres.")
            return
            
        # Apelido válido, mostrar próximo campo
        self.email_input.setVisible(True)
        self.current_field_index = 2
        QMessageBox.information(self, "Critérios do Campo Email", 
                              "Critérios para o campo Email:\n"
                              "- Deve conter @\n"
                              "- Domínios aceitos: gmail.com, hotmail.com ou ufrpe.br\n"
                              "- Não pode ter espaços")

    def validate_email(self):
        email = self.email_input.findChild(QLineEdit).text().strip()
        
        if not email:
            QMessageBox.warning(self, "Campo Vazio", "Por favor, digite seu email.")
            return
            
        if " " in email:
            QMessageBox.warning(self, "Email Inválido", "O email não pode conter espaços.")
            return
            
        if "@" not in email:
            QMessageBox.warning(self, "Email Inválido", "O email deve conter @.")
            return
            
        # Verificar domínio
        domain = email.split('@')[-1]
        valid_domains = ['gmail.com', 'hotmail.com', 'ufrpe.br']
        
        if domain not in valid_domains:
            QMessageBox.warning(self, "Email Inválido", 
                               f"Domínio não aceito. Domínios válidos: {', '.join(valid_domains)}")
            return
            
        # Email válido, mostrar próximo campo
        self.senha_input.setVisible(True)
        self.show_password_checkbox.setVisible(True)
        self.current_field_index = 3
        QMessageBox.information(self, "Critérios do Campo Senha", 
                              "Critérios para o campo Senha:\n"
                              "- Exatamente 6 dígitos\n"
                              "- Aceita apenas números e caracteres especiais\n"
                              "- Não pode ter espaços")

    def validate_senha(self):
        senha = self.senha_input.findChild(QLineEdit).text().strip()
        
        if not senha:
            QMessageBox.warning(self, "Campo Vazio", "Por favor, digite sua senha.")
            return
            
        if " " in senha:
            QMessageBox.warning(self, "Senha Inválida", "A senha não pode conter espaços.")
            return
            
        if len(senha) != 6:
            QMessageBox.warning(self, "Senha Inválida", "A senha deve ter exatamente 6 caracteres.")
            return
            
        # Verificar se contém apenas números e caracteres especiais
        if re.search(r'[a-zA-Z]', senha):
            QMessageBox.warning(self, "Senha Inválida", "A senha só pode conter números e caracteres especiais (não pode letras).")
            return
            
        # Senha válida, mostrar próximo campo
        self.confirm_senha_input.setVisible(True)
        self.current_field_index = 4

    def validate_confirm_senha(self):
        senha = self.senha_input.findChild(QLineEdit).text()
        confirm_senha = self.confirm_senha_input.findChild(QLineEdit).text()
        
        if senha != confirm_senha:
            QMessageBox.warning(self, "Senhas Diferentes", "As senhas não coincidem. Por favor, digite novamente.")
            self.confirm_senha_input.findChild(QLineEdit).clear()
            return

    def _register_user(self):
        # Verificar se todos os campos estão preenchidos
        name = self.name_input.findChild(QLineEdit).text().strip()
        apelido = self.apelido_input.findChild(QLineEdit).text().strip()
        email = self.email_input.findChild(QLineEdit).text().strip()
        senha = self.senha_input.findChild(QLineEdit).text()
        confirm_senha = self.confirm_senha_input.findChild(QLineEdit).text()
        
        if not name or not apelido or not email or not senha or not confirm_senha:
            QMessageBox.warning(self, "Campos Vazios", "Por favor, preencha todos os campos antes de cadastrar.")
            return
            
        if self.current_field_index < 4:
            QMessageBox.warning(self, "Campos Pendentes", "Por favor, preencha todos os campos corretamente antes de cadastrar.")
            return
            
        if senha != confirm_senha:
            QMessageBox.warning(self, "Erro de Senha", "As senhas não coincidem. Por favor, digite novamente.")
            return
        
        # Verificar se email já existe
        if self.db.verificar_email_existente(email):
            QMessageBox.warning(self, "Email Existente", 
                              "Este email já está cadastrado. Por favor, faça login.")
            return
        
        # Verificar se apelido já existe
        if self.db.verificar_apelido_existente(apelido):
            QMessageBox.warning(self, "Apelido Existente", 
                              "Este apelido já está em uso. Por favor, escolha outro.")
            return
        
        # Iniciar verificação em duas etapas
        self.criar_janela_2fa(name, apelido, email, senha)

    

    def closeEvent(self, event):
        """Fecha a conexão com o banco de dados quando a janela é fechada"""
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinhaJanela()
    window.show()
    sys.exit(app.exec())
