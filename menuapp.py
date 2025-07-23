# menuapp.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QPixmap, QPainter, QFont, QColor
from PySide6.QtCore import Qt, QFile, QSize
from mundoconsciencias import WorldOfConsciousnessScreen  # Importe a nova tela

class MenuScreen(QMainWindow):
    def __init__(self, apelido_usuario="Usuário"):
        super().__init__()
        self.setWindowTitle("Na Pele e na Consciência - Menu")
        self.setGeometry(0, 0, 1700, 950)
        self.setMinimumSize(1200, 700)

        # Configuração do fundo
        self.set_background(r"C:\Users\Clara\OneDrive\Área de Trabalho\KIVY\NA PELE E NA CONSCIÊNCIA (9).png")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal (horizontal)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- COLUNA ESQUERDA (Menu) ---
        left_column = QFrame()
        left_column.setFixedWidth(400)
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(60, 60, 40, 60)
        left_layout.setSpacing(20)

        # Título "MENU"
        menu_title = QLabel("MENU")
        menu_title.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 32px;
                font-weight: normal;
                padding-bottom: 5px;
            }
        """)
        menu_title.setAlignment(Qt.AlignLeft)
        
        title_h_layout = QHBoxLayout()
        title_h_layout.addWidget(menu_title)
        title_h_layout.addStretch()
        left_layout.addLayout(title_h_layout)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: white;")
        divider.setFixedHeight(1)
        left_layout.addWidget(divider)

        # Itens do menu
        menu_items_text = [
            "MUNDO DE CONSCIÊNCIAS",
            "PERFIL PERSONALIZADO",
            "COMUNIDADE",
            "CONFIGURAÇÕES DE PERFIL",
            "AJUDA",
            "SOBRE"
        ]

        button_gradients = [
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF8C00, stop:1 #FF4500)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF69B4, stop:1 #FF1493)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9370DB, stop:1 #8A2BE2)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8A2BE2, stop:1 #4B0082)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4B0082, stop:1 #6A5ACD)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6A5ACD, stop:1 #DDA0DD)"
        ]
        
        button_hover_gradients = [
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFA07A, stop:1 #FF6347)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFB6C1, stop:1 #FF69B4)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #BA55D3, stop:1 #9932CC)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9370DB, stop:1 #6A5ACD)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6A5ACD, stop:1 #836FFF)",
            "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #DDA0DD, stop:1 #EE82EE)"
        ]

        # Criar botões do menu
        self.menu_buttons = []
        for i, item_text in enumerate(menu_items_text):
            button = QPushButton(item_text)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {button_gradients[i % len(button_gradients)]};
                    color: white;
                    border: none;
                    border-radius: 18px;
                    padding: 10px 20px;
                    font-family: 'Arial';
                    font-size: 18px;
                    font-weight: bold;
                    text-align: left;
                    min-height: 40px;
                }}
                QPushButton:hover {{
                    background-color: {button_hover_gradients[i % len(button_hover_gradients)]};
                }}
            """)
            button.setFixedSize(300, 50)
            left_layout.addWidget(button, alignment=Qt.AlignLeft)
            self.menu_buttons.append(button)

        left_layout.addStretch()
        main_layout.addWidget(left_column)

        # Linha vertical divisória
        vertical_divider = QFrame()
        vertical_divider.setFrameShape(QFrame.VLine)
        vertical_divider.setStyleSheet("background-color: white;")
        vertical_divider.setFixedWidth(1)
        main_layout.addWidget(vertical_divider)

        # --- COLUNA DIREITA (Conteúdo) ---
        right_column = QFrame()
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(100, 150, 100, 100)
        right_layout.setSpacing(50)

        right_layout.addStretch(2)

        welcome_msg = QLabel(f"SEJA BEM VINDO (A) {apelido_usuario.upper()} !")
        welcome_msg.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Arial';
                font-size: 32px;
                font-weight: bold;
            }
        """)
        welcome_msg.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(welcome_msg)

        start_button = QPushButton("INICIAR JORNADA")
        start_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                 stop:0 #8A2BE2,
                                                 stop:0.5 #FF1493,
                                                 stop:1 #FF8C00);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 15px 30px;
                font-family: 'Arial';
                font-size: 20px;
                font-weight: bold;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                 stop:0 #9932CC,
                                                 stop:0.5 #FF69B4,
                                                 stop:1 #FFA500);
            }
        """)
        start_button.setFixedSize(300, 60)
        right_layout.addWidget(start_button, alignment=Qt.AlignCenter)

        right_layout.addStretch(3)
        main_layout.addWidget(right_column)

        # Conectar os botões do menu às funções correspondentes
        self.menu_buttons[0].clicked.connect(self.show_world_of_consciousness)  # MUNDO DE CONSCIÊNCIAS
        # Os outros botões podem ser conectados aqui quando suas telas estiverem prontas

    def show_world_of_consciousness(self):
        """Mostra a tela Mundo de Consciências"""
        self.world_of_consciousness_screen = WorldOfConsciousnessScreen()
        self.world_of_consciousness_screen.go_back_to_menu.connect(self.show)  # Conecta o sinal de voltar
        self.world_of_consciousness_screen.show()
        self.hide()

    def set_background(self, image_path):
        """Configura o background da janela para preencher a tela."""
        if QFile.exists(image_path):
            self.background_pixmap = QPixmap(image_path)
            self.setStyleSheet("background: transparent;")
        else:
            self.background_pixmap = None
            self.setStyleSheet("background-color: #2c3e50;")

    def paintEvent(self, event):
        """Desenha o background, ajustando para cobrir a janela."""
        painter = QPainter(self)
        if self.background_pixmap and not self.background_pixmap.isNull():
            scaled_pixmap = self.background_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            x = (self.width() - scaled_pixmap.width()) / 2
            y = (self.height() - scaled_pixmap.height()) / 2

            painter.drawPixmap(int(x), int(y), scaled_pixmap)
        painter.end()

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MenuScreen("SeuApelidoAqui")
    window.showMaximized()
    sys.exit(app.exec()) 

