import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QSpacerItem, 
                             QSizePolicy, QMessageBox, QScrollArea, QTabWidget,
                             QGraphicsDropShadowEffect)
from PySide6.QtGui import (QPixmap, QPainter, QFont, QColor, QLinearGradient, 
                         QBrush, QIcon, QPen, QFontDatabase, QImage)
from PySide6.QtCore import (Qt, QSize, Signal, QPoint, QTimer)

class BackgroundWidget(QWidget):
    """Widget de fundo com efeito de desfoque e overlay escuro"""
    def __init__(self, background_image_path, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap(background_image_path)
        self.darken_factor = 0.6  # Intensidade do escurecimento
        
        if self.original_pixmap.isNull():
            print(f"ERRO: Não foi possível carregar a imagem em: {background_image_path}")
            # Fallback: fundo gradiente
            self.original_pixmap = QPixmap(QSize(1920, 1080))
            self.original_pixmap.fill(QColor(20, 25, 45))
        
        self.setAttribute(Qt.WA_StyledBackground, False)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenha a imagem de fundo escalada
        scaled_pixmap = self.original_pixmap.scaled(
            self.size(), 
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        x = (self.width() - scaled_pixmap.width()) // 2
        y = (self.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)
        
        # Overlay escuro para melhor contraste
        overlay = QBrush(QColor(0, 0, 0, int(255 * self.darken_factor)))
        painter.setBrush(overlay)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        
        painter.end()

class GlassCard(QFrame):
    """Card com efeito de vidro (glassmorphism)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(35, 40, 60, 0.4);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        # Efeito de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

class StoryCard(GlassCard):
    """Card interativo para cada história com efeito de vidro"""
    clicked = Signal(str)
    
    def __init__(self, story_id, title, icon_path, enabled=True, parent=None):
        super().__init__(parent)
        self.story_id = story_id
        self.title = title
        self.enabled = enabled
        
        self.setCursor(Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor)
        self.setFixedSize(320, 450)
        
        # Efeito de brilho na borda
        self.border_gradient = QLinearGradient(0, 0, self.width(), 0)
        if enabled:
            self.border_gradient.setColorAt(0, QColor(255, 215, 0, 80))  # Dourado
            self.border_gradient.setColorAt(0.5, QColor(255, 20, 147, 80))  # Rosa
            self.border_gradient.setColorAt(1, QColor(138, 43, 226, 80))  # Roxo
        else:
            self.border_gradient.setColorAt(0, QColor(100, 100, 100, 80))
            self.border_gradient.setColorAt(1, QColor(70, 70, 70, 80))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Ícone da história
        self.icon_label = QLabel()
        self.load_icon(icon_path)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # Título da história
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
            }
        """)
        layout.addWidget(title_label)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("border: 1px solid rgba(255, 255, 255, 0.1);")
        layout.addWidget(divider)
        
        # Status
        status_label = QLabel("DISPONÍVEL" if enabled else "EM DESENVOLVIMENTO")
        status_label.setStyleSheet("""
            QLabel {
                color: #AAAAAA;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                letter-spacing: 2px;
            }
        """)
        layout.addWidget(status_label)
        
        layout.addStretch()

    def load_icon(self, icon_path):
        """Carrega o ícone com tratamento de fallback"""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            # Fallback: ícone padrão
            self.icon_label.setText("📖")
            self.icon_label.setStyleSheet("""
                QLabel {
                    font-size: 80px;
                    color: rgba(255, 255, 255, 0.7);
                }
            """)
        else:
            # Ícone circular com borda
            mask = QPixmap(pixmap.size())
            mask.fill(Qt.transparent)
            
            painter = QPainter(mask)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(Qt.white)
            painter.drawEllipse(mask.rect())
            painter.end()
            
            pixmap.setMask(mask.mask())
            self.icon_label.setPixmap(pixmap.scaled(180, 180, 
                                                 Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation))

    def paintEvent(self, event):
        """Personaliza a pintura para adicionar borda gradiente"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Borda gradiente
        pen = QPen(QBrush(self.border_gradient), 3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 20, 20)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.enabled:
            self.clicked.emit(self.story_id)
        elif event.button() == Qt.MouseButton.LeftButton and not self.enabled:
            # Efeito visual ao clicar em história em desenvolvimento
            self.animate_click()
            QMessageBox.information(self, "Em desenvolvimento", 
                                  "História em desenvolvimento. Em breve disponível!")
        else:
            super().mousePressEvent(event)

    def animate_click(self):
        """Animação de clique para feedback visual"""
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(50, 55, 80, 0.6);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        QTimer.singleShot(200, lambda: self.setStyleSheet("""
            QFrame {
                background-color: rgba(35, 40, 60, 0.4);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """))

class ModernButton(QPushButton):
    """Botão moderno com gradiente e efeitos"""
    def __init__(self, text, color1, color2, parent=None):
        super().__init__(text, parent)
        self.color1 = color1
        self.color2 = color2
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(50)
        
        # Efeito de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)
        
        self.update_style()
    
    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color1}, stop:1 {self.color2});
                color: white;
                border-radius: 25px;
                font: bold 16px;
                padding: 0 25px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.lighter_color(self.color1)}, stop:1 {self.lighter_color(self.color2)});
            }}
            QPushButton:pressed {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.darker_color(self.color1)}, stop:1 {self.darker_color(self.color2)});
                padding-top: 2px;
            }}
        """)
    
    def lighter_color(self, hex_color, factor=0.2):
        """Clareia a cor para o efeito hover"""
        color = QColor(hex_color)
        return color.lighter(int(100 + factor * 100)).name()
    
    def darker_color(self, hex_color, factor=0.2):
        """Escurece a cor para o efeito pressed"""
        color = QColor(hex_color)
        return color.darker(int(100 + factor * 100)).name()

class WorldOfConsciousnessScreen(QMainWindow):
    """Tela principal do Mundo de Consciências - Versão Premium"""
    go_back_to_menu = Signal()
    
    def __init__(self, db, user_apelido, parent=None):
        super().__init__(parent)
        self.db = db
        self.user_apelido = user_apelido
        self.selected_mode = None
        
        # Configuração da janela
        self.setWindowTitle("Na Pele e na Consciência - Mundo de Consciências")
        self.setMinimumSize(1600, 900)
        
        # Carrega fonte personalizada se disponível
        self.load_fonts()
        
        # Configuração do fundo
        self.background_widget = BackgroundWidget("assets/world_bg.jpg")
        self.setCentralWidget(self.background_widget)
        
        main_layout = QVBoxLayout(self.background_widget)
        main_layout.setContentsMargins(60, 30, 60, 30)
        main_layout.setSpacing(30)
        
        # Barra superior
        self.setup_top_bar(main_layout)
        
        # Seção de modos de jogo
        self.setup_mode_selection(main_layout)
        
        # Cards principais das histórias
        self.setup_main_stories(main_layout)
        
        # Abas de status das histórias
        self.setup_story_tabs(main_layout)
        
        # Referências para telas secundárias
        self.story_windows = {}
        self.personalized_profile_screen = None

    def load_fonts(self):
        """Carrega fontes personalizadas se disponíveis"""
        try:
            # Tenta carregar fontes personalizadas
            QFontDatabase.addApplicationFont("assets/fonts/Roboto-Bold.ttf")
            QFontDatabase.addApplicationFont("assets/fonts/Roboto-Regular.ttf")
        except:
            print("Não foi possível carregar fontes personalizadas. Usando fontes padrão.")

    def setup_top_bar(self, main_layout):
        """Configura a barra superior premium"""
        top_bar = GlassCard()
        top_bar.setFixedHeight(100)
        
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(30, 10, 30, 10)
        
        # Botão de voltar
        back_btn = ModernButton("Voltar ao Menu Principal", "#6A5ACD", "#9370DB")
        back_btn.setIcon(QIcon("assets/icons/back_icon.png"))
        back_btn.setIconSize(QSize(24, 24))
        back_btn.clicked.connect(self.go_back_to_menu.emit)
        top_bar_layout.addWidget(back_btn)
        
        # Título
        title_label = QLabel("MUNDO DE CONSCIÊNCIAS")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-size: 32px;
                font-weight: bold;
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
                letter-spacing: 3px;
            }
        """)
        top_bar_layout.addWidget(title_label, 1)
        
        # Espaçador para alinhamento
        top_bar_layout.addSpacerItem(QSpacerItem(250, 45, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        
        main_layout.addWidget(top_bar)

    def setup_mode_selection(self, main_layout):
        """Configura a seleção de modos de jogo premium"""
        mode_container = GlassCard()
        mode_container.setFixedHeight(120)
        
        mode_layout = QHBoxLayout(mode_container)
        mode_layout.setContentsMargins(40, 20, 40, 20)
        mode_layout.addStretch(1)
        
        # Título da seção
        section_label = QLabel("SELECIONE O MODO:")
        section_label.setStyleSheet("""
            QLabel {
                color: #AAAAAA;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 2px;
            }
        """)
        mode_layout.addWidget(section_label)
        mode_layout.addSpacing(40)
        
        # Indicador do Modo 1
        self.mode1_indicator = QLabel()
        self.mode1_indicator.setFixedSize(30, 30)
        self.mode1_indicator.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: 2px solid #FFD700;
                border-radius: 15px;
            }
        """)
        mode_layout.addWidget(self.mode1_indicator)
        
        # Botão do Modo 1
        self.mode1_btn = ModernButton("MODO TRADICIONAL", "#FF8C00", "#FFD700")
        self.mode1_btn.setFixedWidth(250)
        self.mode1_btn.clicked.connect(lambda: self.select_mode("modo1"))
        mode_layout.addWidget(self.mode1_btn)
        mode_layout.addSpacing(50)
        
        # Indicador do Modo 2
        self.mode2_indicator = QLabel()
        self.mode2_indicator.setFixedSize(30, 30)
        self.mode2_indicator.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: 2px solid #9370DB;
                border-radius: 15px;
            }
        """)
        mode_layout.addWidget(self.mode2_indicator)
        
        # Botão do Modo 2
        self.mode2_btn = ModernButton("MODO TEMPORIZADO", "#8A2BE2", "#9370DB")
        self.mode2_btn.setFixedWidth(250)
        self.mode2_btn.clicked.connect(lambda: self.select_mode("modo2"))
        mode_layout.addWidget(self.mode2_btn)
        mode_layout.addStretch(1)
        
        main_layout.addWidget(mode_container)

    def setup_main_stories(self, main_layout):
        """Configura os cards principais das histórias premium"""
        stories_container = GlassCard()
        
        stories_layout = QHBoxLayout(stories_container)
        stories_layout.setContentsMargins(40, 40, 40, 40)
        stories_layout.setSpacing(60)
        
        # Título da seção
        section_title = QLabel("EXPLORE AS HISTÓRIAS")
        section_title.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-size: 24px;
                font-weight: bold;
                text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
                letter-spacing: 2px;
            }
        """)
        main_layout.addWidget(section_title)
        
        # Card da história de Elias
        self.elias_card = StoryCard(
            "elias_story", 
            "O Julgamento de Elias", 
            "assets/stories/elias_icon.png",
            True
        )
        self.elias_card.clicked.connect(self.open_story)
        stories_layout.addWidget(self.elias_card)
        
        # Card da história da Dra. Lívia
        self.livia_card = StoryCard(
            "livia_story", 
            "A Jornada da Dra. Lívia", 
            "assets/stories/livia_icon.png",
            False
        )
        stories_layout.addWidget(self.livia_card)
        
        # Card da história sobre Desigualdade Social
        self.inequality_card = StoryCard(
            "inequality_story", 
            "Desigualdade Social", 
            "assets/stories/inequality_icon.png",
            False
        )
        stories_layout.addWidget(self.inequality_card)
        
        main_layout.addWidget(stories_container)

    def setup_story_tabs(self, main_layout):
        """Configura as abas de status das histórias premium"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: rgba(30, 35, 50, 0.5);
                border-radius: 15px;
            }
            QTabBar::tab {
                background-color: rgba(60, 65, 90, 0.7);
                color: #CCCCCC;
                padding: 15px 30px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                font-size: 16px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: rgba(80, 85, 120, 0.9);
                color: #FFD700;
                border-bottom: 3px solid #FFD700;
            }
            QTabBar::tab:hover {
                background-color: rgba(90, 95, 130, 0.8);
            }
        """)
        
        # Efeito de sombra nas abas
        tab_shadow = QGraphicsDropShadowEffect()
        tab_shadow.setBlurRadius(20)
        tab_shadow.setColor(QColor(0, 0, 0, 100))
        tab_shadow.setOffset(0, 5)
        self.tab_widget.setGraphicsEffect(tab_shadow)
        
        # Aba de histórias não iniciadas
        self.not_started_tab = QWidget()
        self.setup_story_tab(self.not_started_tab, "not_started")
        self.tab_widget.addTab(self.not_started_tab, "NÃO INICIADAS")
        
        # Aba de histórias em andamento
        self.in_progress_tab = QWidget()
        self.setup_story_tab(self.in_progress_tab, "in_progress")
        self.tab_widget.addTab(self.in_progress_tab, "EM ANDAMENTO")
        
        # Aba de histórias concluídas
        self.completed_tab = QWidget()
        self.setup_story_tab(self.completed_tab, "completed")
        self.tab_widget.addTab(self.completed_tab, "CONCLUÍDAS")
        
        main_layout.addWidget(self.tab_widget, 1)

    def setup_story_tab(self, tab, status):
        """Configura uma aba individual de status de histórias premium"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: rgba(50, 55, 80, 0.3);
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 215, 0, 0.5);
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(25)
        
        # Adiciona histórias de exemplo baseadas no status
        stories = self.get_stories_by_status(status)
        
        if not stories:
            no_stories_label = QLabel(f"Nenhuma história {status.replace('_', ' ').lower()}")
            no_stories_label.setStyleSheet("""
                QLabel {
                    color: #666688;
                    font-size: 20px;
                    font-style: italic;
                    padding: 50px 0;
                }
            """)
            no_stories_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.addWidget(no_stories_label)
        else:
            for story in stories:
                story_widget = self.create_story_status_widget(story)
                container_layout.addWidget(story_widget)
        
        container_layout.addStretch()
        scroll_area.setWidget(container)
        layout.addWidget(scroll_area)

    def get_stories_by_status(self, status):
        """Retorna histórias baseadas no status (mock para demonstração)"""
        # Na implementação real, isso viria do banco de dados
        if status == "not_started":
            return [
                {"id": "livia_story", "title": "A Jornada da Dra. Lívia", "status": status},
                {"id": "inequality_story", "title": "Desigualdade Social", "status": status}
            ]
        elif status == "in_progress":
            return [
                {"id": "elias_story", "title": "O Julgamento de Elias", "status": status, 
                 "progress": "Capítulo 2", "completion": "40%"}
            ]
        elif status == "completed":
            return []
        return []

    def create_story_status_widget(self, story):
        """Cria um widget premium para exibir o status de uma história"""
        widget = GlassCard()
        widget.setFixedHeight(120)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Ícone da história
        icon_label = QLabel()
        icon_pixmap = QPixmap(f"assets/stories/{story['id']}_icon.png")
        if icon_pixmap.isNull():
            icon_label.setText("📖")
            icon_label.setStyleSheet("font-size: 40px; color: rgba(255, 255, 255, 0.7);")
        else:
            icon_label.setPixmap(icon_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, 
                                                 Qt.TransformationMode.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        layout.addSpacing(20)
        
        # Informações da história
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        # Título e progresso
        title_layout = QHBoxLayout()
        
        title_label = QLabel(story["title"])
        title_label.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        if "completion" in story:
            progress_label = QLabel(story["completion"])
            progress_label.setStyleSheet("""
                QLabel {
                    color: #AAAAAA;
                    font-size: 14px;
                    font-weight: bold;
                    background-color: rgba(70, 70, 100, 0.5);
                    padding: 3px 10px;
                    border-radius: 10px;
                }
            """)
            title_layout.addWidget(progress_label)
        
        info_layout.addLayout(title_layout)
        
        # Barra de progresso customizada
        if "progress" in story:
            progress_bar = QFrame()
            progress_bar.setFixedHeight(8)
            progress_bar.setStyleSheet("""
                QFrame {
                    background-color: rgba(70, 70, 100, 0.5);
                    border-radius: 4px;
                }
            """)
            
            # Barra de progresso interna
            inner_progress = QFrame(progress_bar)
            progress_width = 200 if story["id"] == "elias_story" else 0
            inner_progress.setGeometry(0, 0, progress_width, 8)
            inner_progress.setStyleSheet("""
                QFrame {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #FF8C00, stop:1 #FFD700);
                    border-radius: 4px;
                }
            """)
            
            info_layout.addWidget(progress_bar)
            
            # Texto de progresso
            progress_text = QLabel(f"Progresso: {story['progress']}")
            progress_text.setStyleSheet("""
                QLabel {
                    color: #AAAAAA;
                    font-size: 14px;
                }
            """)
            info_layout.addWidget(progress_text)
        
        layout.addLayout(info_layout, 1)
        
        # Botão de ação
        action_btn = ModernButton(
            "Continuar" if story["status"] == "in_progress" else "Iniciar",
            "#6A5ACD", "#9370DB"
        )
        action_btn.setFixedWidth(120)
        action_btn.setEnabled(story["id"] == "elias_story")  # Só Elias está implementado
        action_btn.clicked.connect(lambda: self.open_story(story["id"]))
        layout.addWidget(action_btn)
        
        return widget

    def select_mode(self, mode):
        """Seleciona o modo de jogo (1 ou 2) com animação"""
        self.selected_mode = mode
        
        # Animação de seleção
        if mode == "modo1":
            self.mode1_indicator.setStyleSheet("""
                QLabel {
                    background-color: #FFD700;
                    border: 2px solid #FFD700;
                    border-radius: 15px;
                }
            """)
            self.mode2_indicator.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    border: 2px solid #9370DB;
                    border-radius: 15px;
                }
            """)
            self.mode1_btn.setStyleSheet(self.mode1_btn.styleSheet() + """
                QPushButton {
                    border: 2px solid #FFD700;
                }
            """)
            self.mode2_btn.setStyleSheet(self.mode2_btn.styleSheet().replace("border: 2px solid #9370DB;", ""))
        else:
            self.mode1_indicator.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    border: 2px solid #FFD700;
                    border-radius: 15px;
                }
            """)
            self.mode2_indicator.setStyleSheet("""
                QLabel {
                    background-color: #9370DB;
                    border: 2px solid #9370DB;
                    border-radius: 15px;
                }
            """)
            self.mode2_btn.setStyleSheet(self.mode2_btn.styleSheet() + """
                QPushButton {
                    border: 2px solid #9370DB;
                }
            """)
            self.mode1_btn.setStyleSheet(self.mode1_btn.styleSheet().replace("border: 2px solid #FFD700;", ""))
        
        print(f"Modo selecionado: {mode}")

    def open_story(self, story_id):
        """Abre a história selecionada com verificação de modo"""
        if story_id == "elias_story":
            if not self.selected_mode:
                QMessageBox.warning(self, "Modo Não Selecionado", 
                                   "Por favor, selecione um modo de jogo antes de iniciar a história.")
                return
            
            # Abre a história de Elias no modo selecionado
            self.open_elias_story()
        else:
            # Efeito visual para histórias em desenvolvimento
            for card in [self.livia_card, self.inequality_card]:
                if card.story_id == story_id:
                    card.animate_click()
            
            QMessageBox.information(self, "Em desenvolvimento", 
                                  "História em desenvolvimento. Em breve disponível!")

    def open_elias_story(self):
        """Abre a história de Elias com efeito visual"""
        # Efeito de clique no card
        self.elias_card.animate_click()
        
        # Simula a abertura da história
        print(f"Abrindo história de Elias no modo {self.selected_mode}")
        
        # Janela de demonstração
        msg = QMessageBox()
        msg.setWindowTitle("História de Elias")
        msg.setText(f"História de Elias será aberta no Modo {self.selected_mode}")
        msg.setIcon(QMessageBox.Icon.Information)
        
        # Personaliza a mensagem
        msg.setStyleSheet("""
            QMessageBox {
                background-color: rgba(40, 45, 60, 0.9);
                color: white;
            }
            QLabel {
                color: #FFD700;
                font-size: 18px;
            }
            QPushButton {
                background-color: #6A5ACD;
                color: white;
                border-radius: 10px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #9370DB;
            }
        """)
        
        msg.exec_()

    def refresh_story_status(self):
        """Atualiza o status das histórias (será chamado quando retornar de uma história)"""
        # TODO: Implementar atualização do banco de dados
        pass

# Classe de mock para o banco de dados para teste
class MockDatabase:
    def __init__(self):
        self.users = {
            "TestUser": {"name": "Aventureiro", "apelido": "TestUser", 
                        "Justice": 10, "Reputation": 5, "Empathy": 15, "Stress": 2},
            "AnotherUser": {"name": "Explorador", "apelido": "AnotherUser", 
                          "Justice": 5, "Reputation": 10, "Empathy": 8, "Stress": 10}
        }
        self.story_progress = {
            "TestUser": {
                "elias_story": {"story_state": "in_progress", "last_chapter": "chapter_2"},
                "elias_story_timed": None,
                "livia_story": None,
                "inequality_story": None,
            },
            "AnotherUser": {
                "elias_story": {"story_state": "completed", "last_chapter": "end"},
                "elias_story_timed": {"story_state": "in_progress", "last_chapter": "intro"},
                "livia_story": None,
                "inequality_story": None,
            }
        }

    def get_user_profile(self, apelido):
        return self.users.get(apelido, {})

    def get_story_progress(self, user_apelido, story_id):
        return self.story_progress.get(user_apelido, {}).get(story_id)

    def save_story_progress(self, user_apelido, story_id, story_state, last_chapter):
        if user_apelido not in self.story_progress:
            self.story_progress[user_apelido] = {}
        self.story_progress[user_apelido][story_id] = {
            "story_state": story_state, 
            "last_chapter": last_chapter
        }

# Código para testar a aplicação
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QPalette, QColor
    
    app = QApplication(sys.argv)
    
    # Configura o estilo geral da aplicação
    app.setStyle("Fusion")
    
    # Paleta de cores escura
    dark_palette = QPalette()
    
    # Configuração da paleta usando ColorRole
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(25, 30, 45))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 40, 60))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 50, 70))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(60, 65, 90))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 215, 0))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(138, 43, 226))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(dark_palette)
    
    # Criar uma instância mock do banco de dados
    mock_db = MockDatabase()
    
    # Criar e mostrar a tela principal
    main_window = WorldOfConsciousnessScreen(mock_db, "TestUser")
    main_window.showMaximized()
    
    sys.exit(app.exec())
