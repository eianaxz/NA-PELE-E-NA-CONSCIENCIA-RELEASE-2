from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy, QScrollArea
)
from PySide6.QtGui import QIcon, QLinearGradient, QColor
from PySide6.QtCore import Qt, Signal
from typing import Dict, Any

from background_widget import BackgroundWidget

class ProfileScreen(QMainWindow):
    back_to_main_menu = Signal()

    def __init__(self, user_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.setWindowTitle(f"Perfil de {user_data.get('apelido', 'Usuário')}")
        self.setMinimumSize(1400, 700)

        self.setup_ui()

    def setup_ui(self):
        self.background_widget = BackgroundWidget("assets/bg_story.jpg")
        self.setCentralWidget(self.background_widget)

        self.main_layout = QVBoxLayout(self.background_widget)
        self.main_layout.setContentsMargins(40, 20, 40, 20)
        self.main_layout.setSpacing(20)

        self.setup_top_bar()
        self.setup_content_area()
        self.display_profile_data()

    def setup_top_bar(self):
        self.top_bar_frame = QFrame()
        self.top_bar_frame.setFixedHeight(80)
        self.top_bar_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 45, 0.9);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            }
        """)
        self.main_layout.addWidget(self.top_bar_frame)

        top_bar_layout = QHBoxLayout(self.top_bar_frame)
        top_bar_layout.setContentsMargins(20, 10, 20, 10)
        top_bar_layout.setSpacing(20)

        self.back_button = QPushButton("Voltar ao Menu")
        self.back_button.setFixedSize(220, 45)
        self.back_button.setIcon(QIcon("assets/icon_back.png"))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 90, 0.7);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 22px;
                font-size: 15px;
                font-weight: bold;
                padding-left: 10px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 110, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        top_bar_layout.addWidget(self.back_button)

        self.title_label = QLabel(f"Perfil de {self.user_data.get('apelido', 'Usuário')}")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-size: 26px;
                font-weight: bold;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
            }
        """)
        top_bar_layout.addWidget(self.title_label, 1)

        top_bar_layout.addSpacerItem(QSpacerItem(220, 45, QSizePolicy.Fixed, QSizePolicy.Fixed))

    def setup_content_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(255, 255, 255, 0.15);
                width: 10px;
                margin: 5px 0px 5px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.4);
                min-height: 40px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.scroll_area.setWidget(self.content_widget)

        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(30, 30, 30, 30)

        self.main_layout.addWidget(self.scroll_area, 1)

    def display_profile_data(self):
        """Exibe os dados do perfil do usuário."""
        # Informações básicas do usuário
        profile_frame = QFrame()
        profile_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 45, 0.85);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.4);
            }
        """)
        profile_layout = QVBoxLayout(profile_frame)
        profile_layout.setContentsMargins(25, 20, 25, 20)

        name_label = QLabel(f"Nome: <span style='color: #FFD700;'>{self.user_data.get('nome', 'N/A')}</span>")
        name_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        name_label.setTextFormat(Qt.RichText)
        profile_layout.addWidget(name_label)

        nickname_label = QLabel(f"Apelido: <span style='color: #8A2BE2;'>{self.user_data.get('apelido', 'N/A')}</span>")
        nickname_label.setStyleSheet("font-size: 18px;")
        nickname_label.setTextFormat(Qt.RichText)
        profile_layout.addWidget(nickname_label)

        self.content_layout.addWidget(profile_frame)
        self.content_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Atributos do jogador (copiado de EliasStoryWindow.show_final_profile)
        attributes_frame = QFrame()
        attributes_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 45, 0.85);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.4);
            }
        """)
        attributes_layout = QVBoxLayout(attributes_frame)
        attributes_layout.setContentsMargins(25, 20, 25, 20)

        attributes_title = QLabel("Atributos de Jogo:")
        attributes_title.setStyleSheet("""
            QLabel {
                color: #FFF;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        attributes_layout.addWidget(attributes_title)
        attributes_layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        attr_translation = {
            "Justice": "Justiça",
            "Reputation": "Reputação",
            "Empathy": "Empatia",
            "Stress": "Estresse"
        }

        for attr, value in {k: self.user_data.get(k, 0) for k in attr_translation.keys()}.items():
            attr_frame = QFrame()
            attr_layout = QHBoxLayout(attr_frame)
            attr_layout.setSpacing(15)

            attr_name = QLabel(attr_translation.get(attr, attr))
            attr_name.setStyleSheet("""
                QLabel {
                    color: #A0A0A0;
                    font-size: 15px;
                    min-width: 110px;
                }
            """)
            attr_layout.addWidget(attr_name)

            value_label = QLabel(f"{value:+d}")
            value_label.setStyleSheet("""
                QLabel {
                    color: %s;
                    font-size: 15px;
                    font-weight: bold;
                    min-width: 45px;
                }
            """ % ("#4CAF50" if value >= 0 else "#F44336"))
            attr_layout.addWidget(value_label)

            progress_frame = QFrame()
            progress_frame.setFixedHeight(25)
            progress_frame.setStyleSheet("""
                QFrame {
                    background-color: #33334A;
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
            """)
            progress_layout = QHBoxLayout(progress_frame)
            progress_layout.setContentsMargins(3, 3, 3, 3)

            progress_bar = QFrame()
            if value >= 0:
                progress_bar.setStyleSheet("""
                    QFrame {
                        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                          stop:0 #8A2BE2, stop:1 #FF1493);
                        border-radius: 10px;
                    }
                """)
            else:
                progress_bar.setStyleSheet("""
                    QFrame {
                        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                          stop:0 #FF4500, stop:1 #FF8C00);
                        border-radius: 10px;
                    }
                """)
            max_value = 20 # Valor máximo assumido para os atributos para escala
            width = min(abs(value) * (250/max_value), 250) # Largura máxima da barra em pixels
            progress_bar.setFixedWidth(width)

            if value < 0:
                progress_layout.addStretch()
            progress_layout.addWidget(progress_bar)
            if value >= 0:
                progress_layout.addStretch()

            attr_layout.addWidget(progress_frame, 1)
            attributes_layout.addWidget(attr_frame)

        self.content_layout.addWidget(attributes_frame)
        self.content_layout.addStretch(1) # Empurra o conteúdo para cima

    def go_back(self):
        """Emite o sinal para retornar à tela anterior (menu principal)."""
        self.back_to_main_menu.emit()
