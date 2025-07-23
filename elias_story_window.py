import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                              QPushButton, QFrame, QScrollArea, QButtonGroup, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QPalette

class MundoConscienciaElias(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("O Julgamento de Elias")
        self.setMinimumSize(800, 600)
        
        # Configurar a paleta de cores para o tema escuro
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(34, 34, 34))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(50, 50, 50))
        palette.setColor(QPalette.AlternateBase, QColor(34, 34, 34))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(68, 68, 68))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(0, 122, 204))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.setPalette(palette)
        
        # Variáveis de estado do jogo
        self.current_choice_path = []
        self.story_state = "intro"
        self.player_attributes = {
            "Justice": 0,
            "Reputation": 0,
            "Empathy": 0,
            "Stress": 0
        }
        
        # Configurar a estrutura da história
        self.story = self.setup_story_structure()
        
        # Widget central e layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Área de rolagem
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        
        # Botões de ação (fora da área de rolagem)
        self.action_buttons_layout = QVBoxLayout()
        self.action_buttons_layout.setSpacing(10)
        self.main_layout.addLayout(self.action_buttons_layout)
        
        # Iniciar o jogo
        self.show_story_screen()
    
    def setup_story_structure(self):
        """Estrutura hierárquica da história baseada no PDF"""
        return {
            "intro": {
                "title": "⚖️ O JULGAMENTO DE ELIAS ⚖️",
                "text": """Você é juiz há 12 anos. É conhecido por sua imparcialidade, mas também por sua frieza técnica. Hoje, você encara um dos julgamentos mais controversos da sua carreira: Elias, um jovem negro e professor de filosofia, é preso acusado de envolvimento em um assalto violento que deixou uma vítima em coma. Não há provas físicas contra ele — nenhuma digital, nenhuma arma, nenhum DNA. Apenas o depoimento de uma testemunha, que afirma tê-lo visto no local do crime. A pressão da mídia e da população é grande. Como juiz, você precisa decidir o destino de Elias. A sociedade quer justiça. Mas será que justiça é o mesmo que punição?""",
                "choices": [
                    ("📜 Seguir com o julgamento mesmo sem provas, confiando no processo.", "1"),
                    ("⏳ Adiar o julgamento até surgirem provas mais concretas.", "2"),
                    ("❌ Arquivar o caso por falta de provas e libertar Elias.", "3")
                ],
                # Indica qual container de escolhas estas escolhas levam
                "next_container_key": "choices_lvl1"
            },
            "choices_lvl1": {  # Container das escolhas resultantes da intro
                "1": {
                    "title": "👁️‍🗨️ Seguir com o julgamento",
                    "text": """O tribunal se enche. O público vibra como se estivesse num espetáculo. Seu rosto estampa jornais como símbolo de ação firme contra o crime. Porém, durante a noite, você recebe um e-mail anônimo: "E se fosse você no banco dos réus?" A pressão se transforma em inquietação interna. Agora você como juiz recebe mais 3 escolhas de decisões que pode tomar, o que você escolhe?""",
                    "choices": [
                        ("🗣️ Ouvir apenas testemunhas da acusação.", "1.1"),
                        ("🤝 Solicitar novas testemunhas imparciais.", "1.2"),
                        ("🚫 Impedir novas evidências após a abertura do julgamento.", "1.3")
                    ],
                    "next_container_key": "choices_lvl2_1"
                },
                "2": {
                    "title": "⏸️ Adiar o julgamento",
                    "text": """O povo protesta: "Covarde!" Mas uma defensora pública sussurra: "Você está protegendo a justiça." Nos bastidores, você inicia uma investigação paralela. E, mais três decisões aparecem:""",
                    "choices": [
                        ("🔎 Enviar investigadores para reabrirem o caso.", "2.1"),
                        ("🎙️ Realizar uma audiência pública sobre o caso.", "2.2"),
                        ("📚 Revisar o histórico de Elias em busca de possíveis motivações.", "2.3")
                    ],
                    "next_container_key": "choices_lvl2_2"
                },
                "3": {
                    "title": "📂 Arquivar o caso",
                    "text": """Você decide arquivar o caso por falta de provas suficientes. """,
                    "choices": [
                        ("📢 Fazer um pronunciamento explicando a decisão.", "3.1"),
                        ("🤫 Manter silêncio para evitar retaliações.", "3.2"),
                        ("🤝 Conversar com a família da vítima para explicar a falta de provas.", "3.3")
                    ],
                    "next_container_key": "choices_lvl2_3"
                }
            },
            "choices_lvl2_1": {  # Container para as escolhas 1.1, 1.2, 1.3
                "1.1": {
                    "title": "🔊 Ouvir apenas testemunhas da acusação",
                    "text": """Ao optar por ouvir somente as testemunhas da acusação, o tribunal recebe depoimentos contundentes contra Elias. A defesa reclama de parcialidade e pede reconsideração, mas sua decisão mantém o foco unilateral. A população fica dividida: alguns clamam por justiça rápida, enquanto outros acusam o sistema de ser injusto e precipitado. Elias parece cada vez mais desesperado diante da falta de uma defesa justa. Como juiz, você tem mais um último desafio: Tomar a decisão final acerca do julgamento de Elias, e agora, o que você faz?""",
                    "choices": [
                        ("⚖️ Manter a decisão e condenar Elias com base nos depoimentos apresentados.", "1.1.1"),
                        ("🚪 Permitir que a defesa apresente suas testemunhas para garantir um julgamento mais justo.", "1.1.2"),
                        ("🔄 Reabrir o inquérito para buscar novas provas que possam confirmar ou refutar os depoimentos.", "1.1.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "1.2": {
                    "title": "🤝 Solicitar novas testemunhas imparciais",
                    "text": """Você decide suspender temporariamente o julgamento e exige a convocação de testemunhas que não estejam ligadas nem à acusação nem à defesa. Isso gera tensão no tribunal. A mídia elogia sua tentativa de neutralidade, mas os advogados da acusação alegam que isso enfraquece a posição deles. Após alguns dias, três novas testemunhas são localizadas: um segurança do local do crime, um vizinho que escutou gritos naquela noite e um entregador que passava na rua. Essas novas testemunhas trazem versões que contradizem partes da acusação, mas também deixam dúvidas no ar. O julgamento se torna ainda mais delicado. Agora, surge uma nova responsabilidade para você: Decidir quais outros caminhos esse julgamento deve tomar. O que você escolhe?""",
                    "choices": [
                        ("📝 Registrar os novos depoimentos e levar o julgamento direto à decisão final.", "1.2.1"),
                        ("🔬 Solicitar perícia técnica complementar para verificar detalhes apontados nas novas falas.", "1.2.2"),
                        ("🗳️ Propor um júri popular para que a decisão final reflita a visão coletiva da sociedade.", "1.2.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "1.3": {
                    "title": "🚫 Impedir novas evidências após a abertura do julgamento",
                    "text": """Você decide que o julgamento seguirá apenas com as provas apresentadas inicialmente. A defesa protesta energicamente, afirmando que novas evidências poderiam provar a inocência de Elias. A opinião pública explode - alguns elogiam sua firmeza e defesa da ordem processual; outros o acusam de estar ignorando o direito à verdade. Um jornalista investigativo revela que houve uma denúncia anônima com possíveis provas novas, mas você recusa aceitá-las oficialmente, alegando que o julgamento já está em curso e deve ser finalizado. O clima é tenso. Elias parece cada vez mais fragilizado.""",
                    "choices": [
                        ("🔒 Condenar Elias com as provas existentes, mantendo a firmeza na decisão.", "1.3.1"),
                        ("⚖️ Considerar a possibilidade de reavaliar, mas manter a decisão inicial para evitar atrasos.", "1.3.2"),
                        ("✨ Suspender o julgamento para buscar novas evidências, mesmo contra a decisão anterior.", "1.3.3")
                    ],
                    "next_container_key": "final_outcomes"
                }
            },
            "choices_lvl2_2": {  # Container para as escolhas 2.1, 2.2, 2.3
                "2.1": {
                    "title": "🔎 Enviar investigadores para reabrirem o caso",
                    "text": """Você determina que o caso seja reaberto para investigação. Dois detetives independentes são convocados. Dias depois, descobrem inconsistências no depoimento da principal testemunha da acusação e também encontram imagens de uma câmera de segurança mal analisada anteriormente, que pode mudar o rumo do processo. A mídia começa a cobrir o caso com mais atenção, e a opinião pública começa a se dividir entre "Elias pode ser inocente" e "Estão querendo livrar um criminoso". O tempo para julgamento é estendido, gerando pressão política e institucional sobre você.""",
                    "choices": [
                        ("🚨 Pressionar para a prisão do verdadeiro culpado e reabilitar Elias publicamente.", "2.1.1"),
                        ("🤫 Manter a discrição, concluindo o caso sem alardes para evitar mais perturbações.", "2.1.2"),
                        ("🏛️ Usar o caso como exemplo para promover reformas no sistema judiciário.", "2.1.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "2.2": {
                    "title": "🎙️ Realizar uma audiência pública sobre o caso",
                    "text": """Você decide abrir uma audiência pública, permitindo que o caso de Elias seja debatido com transparência. Familiares da vítima e do acusado, representantes da sociedade civil, juristas e jornalistas participam. A audiência se torna um evento de grande repercussão. Durante a sessão, surgem dúvidas importantes sobre a coerência da investigação original. A sociedade pressiona por justiça, mas com equilíbrio. A opinião pública se divide: alguns te veem como corajoso e transparente; outros acham que a justiça está se tornando um espetáculo.""",
                    "choices": [
                        ("❤️ Considerar a opinião pública e julgar Elias com base na comoção popular.", "2.2.1"),
                        ("📈 Ignorar a pressão e focar apenas nas evidências técnicas para a decisão.", "2.2.2"),
                        ("🕵️ Suspender a audiência para realizar novas investigações sobre os depoimentos.", "2.2.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "2.3": {
                    "title": "📚 Revisar o histórico de Elias em busca de possíveis motivações",
                    "text": """Você decide solicitar uma investigação completa sobre o passado de Elias: antecedentes criminais, histórico escolar, profissional e relações sociais. Descobre que ele teve um desentendimento com a vítima há alguns anos, mas também que nunca teve envolvimento com atividades ilegais. Relatórios sociais mostram que ele era visto como alguém calmo e trabalhador, embora tenha sofrido episódios de discriminação racial e perseguição policial injustificada em seu bairro. A imprensa começa a questionar se a justiça está usando o passado dele para justificar uma acusação sem provas.""",
                    "choices": [
                        ("👊 Confrontar as autoridades locais sobre a possível perseguição política contra Elias.", "2.3.1"),
                        ("🕵️‍♀️ Manter a discrição e continuar investigando internamente para evitar escândalos.", "2.3.2"),
                        ("📰 Divulgar as novas informações para a imprensa para pressionar por uma investigação externa.", "2.3.3")
                    ],
                    "next_container_key": "final_outcomes"
                }
            },
            "choices_lvl2_3": {  # Container para as escolhas 3.1, 3.2, 3.3
                "3.1": {
                    "title": "📢 Fazer um pronunciamento explicando a decisão",
                    "text": """Você decide se posicionar publicamente. Em rede nacional, comunica com firmeza que o caso foi arquivado por falta de provas e que a justiça não pode se basear em suposições. No pronunciamento, você destaca a importância da presunção de inocência e do respeito aos direitos humanos. O país se divide: parte da população apoia sua coragem; outra parte o acusa de estar "protegendo criminosos" e enfraquecendo a justiça. A imprensa pressiona, a promotoria recorre, e protestos começam a surgir nas redes e nas ruas.""",
                    "choices": [
                        ("🔐 Solicitar proteção para Elias e sua família", "3.1.1"),
                        ("🕵 Criar uma força-tarefa independente para investigar o caso por fora", "3.1.2"),
                        ("🧾 Reabrir o caso discretamente após novas denúncias anônimas", "3.1.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "3.2": {
                    "title": "🤫 Manter silêncio para evitar retaliações",
                    "text": """Você decide não se pronunciar publicamente após arquivar o caso de Elias. A mídia começa a especular os motivos do silêncio. Grupos ativistas o criticam por não dar satisfação à sociedade, enquanto outros o elogiam por evitar politização. Elias, mesmo livre, enfrenta hostilidade em seu bairro e tem dificuldade para retomar a vida. O clima é de tensão. Seu silêncio vira símbolo de prudência para alguns — e de omissão para outros.""",
                    "choices": [
                        ("📞 Entrar em contato diretamente com a família de Elias", "3.2.1"),
                        ("📄 Redigir um relatório confidencial explicando sua decisão, a ser usado apenas se necessário", "3.2.2"),
                        ("🗂 Encaminhar discretamente o caso para um grupo de direitos humanos investigar por fora", "3.2.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "3.3": {
                    "title": "🤝 Conversar com a família da vítima para explicar a falta de provas",
                    "text": """Você marca uma reunião privada com os pais da vítima. Eles estão emocionalmente abalados e com sede de justiça. Ao explicar que o caso foi arquivado por falta de provas concretas, a família reage com dor, revolta e incompreensão. Acusam o sistema de ser falho e juram buscar justiça por conta própria. A notícia da conversa vaza para a mídia. O clima se torna ainda mais delicado: agora, além da pressão social, há risco de retaliação contra Elias por parte de simpatizantes da vítima.""",
                    "choices": [
                        ("⚠️ Oferecer proteção legal e psicológica à família da vítima", "3.3.1"),
                        ("󰳌 Encaminhar a família para abertura de um processo cível paralelo", "3.3.2"),
                        ("🧯 Intermediar um encontro entre a família da vítima e Elias (caso ele aceite)", "3.3.3")
                    ],
                    "next_container_key": "final_outcomes"
                }
            },
            "final_outcomes": {  # O container que agrupa todos os desfechos finais
                "1.1.1": {
                    "title": "❌ Condenação Injusta ❌",
                    "text": """Elias é condenado à prisão perpétua. Anos depois, novas evidências surgem provando sua inocência, mas ele já está cumprindo pena. A sociedade questiona o sistema judicial, e sua reputação como juiz fica gravemente manchada. Você passa a sofrer ataques públicos e internos por ter ignorado a possibilidade de injustiça.""",
                    "attributes": {"Justice": -8, "Reputation": -10, "Empathy": -5, "Stress": 12}
                },
                "1.1.2": {
                    "title": "✅ Absolvição com Integridade ✅",
                    "text": """A defesa traz testemunhas que apontam falhas nas acusações, gerando dúvidas razoáveis no júri. Elias é absolvido, e você é reconhecido por garantir o direito ao contraditório, preservando os valores da justiça. No entanto, você enfrenta críticas por atrasar o processo.""",
                    "attributes": {"Justice": 7, "Reputation": 8, "Empathy": 6, "Stress": 4}
                },
                "1.1.3": {
                    "title": "🔥 Descoberta da Corrupção 🔥",
                    "text": """A investigação revela uma conspiração dentro da polícia, forjando provas contra Elias. O caso se torna um escândalo nacional, e você é visto como um símbolo da luta contra a corrupção. Elias é libertado, e sua carreira judicial se fortalece, mas você enfrenta ameaças e pressões constantes.""",
                    "attributes": {"Justice": 10, "Reputation": 12, "Empathy": 8, "Stress": 10}
                },
                "1.2.1": {
                    "title": "✨ Justiça Prevalecida ✨",
                    "text": """Você considera os relatos das testemunhas imparciais e decide que há dúvida razoável. Elias é absolvido. No entanto, meses depois, outra pessoa confessa o crime com detalhes. Você é elogiado por ter evitado uma injustiça, mas também criticado por não ter ido mais a fundo. A sociedade se divide: metade reconhece sua coragem, metade chama de "juiz frouxo".""",
                    "attributes": {"Justice": 6, "Reputation": 4, "Empathy": 7, "Stress": 5}
                },
                "1.2.2": {
                    "title": "🏆 O Juiz Honesto 🏆",
                    "text": """A perícia revela que Elias não estava na cena do crime, e que houve manipulação de dados no relatório original da polícia. Você encaminha o caso ao Ministério Público e uma rede de corrupção policial é descoberta. Elias é libertado, e você se torna símbolo da justiça meticulosa. Mas sofre retaliações e ameaças.""",
                    "attributes": {"Justice": 10, "Reputation": 9, "Empathy": 8, "Stress": 10}
                },
                "1.2.3": {
                    "title": "📉 Decisão Popular e Injusta 📉",
                    "text": """O júri ouve todas as versões e decide pela condenação de Elias. Mais tarde, novas provas revelam que o júri foi influenciado por um vazamento de informações falsas nas redes sociais. Elias é inocente. Você se vê arrependido por ter delegado a decisão sem garantir segurança plena do processo. Sua imagem sofre, e você passa a repensar o papel do juiz na mediação da verdade.""",
                    "attributes": {"Justice": -8, "Reputation": -7, "Empathy": -7, "Stress": 8}  # Ajustado para o range, dado que não há valores específicos para este no PDF.
                },
                "1.3.1": {
                    "title": "⚖️ Firmeza Questionável ⚖️",
                    "text": """Elias é condenado. Sem chance de defesa atualizada, ele é levado para a prisão. Meses depois, a denúncia anônima leva à prisão do verdadeiro culpado um parente da vítima que confessou em troca de delação premiada. A sua imagem como juiz entra em colapso. Movimentos sociais protestam, e sua carreira entra em declínio.""",
                    "attributes": {"Justice": -9, "Reputation": -10, "Empathy": -5, "Stress": 12}
                },
                "1.3.2": {
                    "title": "⚠️ A Incerteza da Decisão ⚠️",
                    "text": """Você conclui o julgamento com base nas provas antigas, mas permite que os autos fiquem abertos para recurso. Elias é condenado, mas sua defesa entra com novo processo dias depois. A apelação revela a inocência dele, e ele é libertado. Você é criticado por não ter agido antes, mas elogiado por ter deixado espaço para a revisão.""",
                    "attributes": {"Justice": 2, "Reputation": -3, "Empathy": 4, "Stress": 8}
                },
                "1.3.3": {
                    "title": "🌟 A Coragem da Verdade 🌟",
                    "text": """Você fecha completamente a porta para qualquer novo elemento. Elias é condenado. A denúncia anônima se torna pública pelas redes sociais e imprensa. Um escândalo explode. Você sofre um processo por violação dos direitos constitucionais do réu. Seu nome é usado em campanhas contra injustiças judiciais. Mesmo assim, você defende sua decisão até o fim.""",
                    "attributes": {"Justice": -12, "Reputation": -15, "Empathy": -8, "Stress": 15}
                },
                "2.1.1": {
                    "title": "🦸‍♂️ Ícone da Justiça 🦸‍♂️",
                    "text": """A perícia comprova que Elias não estava na cena do crime, e a gravação mostra outro homem, posteriormente identificado como o verdadeiro autor. A acusação desmorona. Elias é libertado e você é homenageado por sua decisão de aprofundar a verdade, mesmo sob pressão. O processo vira exemplo em faculdades de Direito.""",
                    "attributes": {"Justice": 10, "Reputation": 8, "Empathy": 6, "Stress": 4}
                },
                "2.1.2": {
                    "title": "🤫 Justiça Silenciosa 🤫",
                    "text": """A testemunha entra em contradição e, pressionada, admite que foi coagida pela polícia para mentir. Uma investigação maior é aberta, revelando manipulação de provas. Você suspende o julgamento e solicita revisão total do processo. Elias é libertado, mas a crise institucional gera ataques à sua conduta. Mesmo assim, defensores dos direitos humanos o apoiam fortemente.""",
                    "attributes": {"Justice": 9, "Reputation": 3, "Empathy": 7, "Stress": 9}
                },
                "2.1.3": {
                    "title": "✊ Agente de Mudança ✊",
                    "text": """Você solicita a suspensão do julgamento e proteção especial ao réu. Isso causa comoção setores da sociedade veem sua decisão como prudente, outros como provocativa. Uma semana depois, o verdadeiro culpado confessa o crime para aliviar sua consciência. Elias é libertado, mas sua imagem permanece manchada por ter sido preso e acusado injustamente por tanto tempo.""",
                    "attributes": {"Justice": 7, "Reputation": -2, "Empathy": 9, "Stress": 6}
                },
                "2.2.1": {
                    "title": "🎭 Justiça Emocional 🎭",
                    "text": """Elias faz um discurso emocionado. Ele expõe falhas do processo, fala de sua vida, de como perdeu o emprego, o respeito da comunidade e a paz. O público se comove. Uma nova testemunha que estava calada por medo decide falar, revelando que Elias não estava na cena do crime. A investigação reabre, ele é inocentado. Sua fala viraliza como símbolo contra erros judiciais.""",
                    "attributes": {"Justice": 8, "Reputation": 9, "Empathy": 10, "Stress": 6}
                },
                "2.2.2": {
                    "title": "🛡️ Integridade Inabalável 🛡️",
                    "text": """O comitê formado por juristas e especialistas encontra diversas irregularidades no processo, incluindo provas forjadas. Você é parabenizado por buscar isenção. A promotoria é investigada, Elias é libertado e recebe uma indenização do Estado. Você é visto como exemplo de ética judicial.""",
                    "attributes": {"Justice": 10, "Reputation": 7, "Empathy": 8, "Stress": 5}
                },
                "2.2.3": {
                    "title": "👑 Herói da Verdade 👑",
                    "text": """Ao encerrar a audiência, parte da população se frustra por sentir que a discussão foi interrompida. No julgamento, as provas continuam frágeis, mas você sente-se pressionado a seguir com o rito. Elias é condenado. Meses depois, uma denúncia anônima aponta outro suspeito, mas o caso já está encerrado. A credibilidade do processo é duramente questionada.""",
                    "attributes": {"Justice": -4, "Reputation": -5, "Empathy": -2, "Stress": 10}
                },
                "2.3.1": {
                    "title": "🔥 Confronto Corajoso 🔥",
                    "text": """O psicólogo avalia Elias como emocionalmente estável, com sinais de trauma recente pela prisão injusta. A avaliação desmonta a tese da promotoria sobre “comportamento agressivo oculto”. A defesa solicita a anulação do processo e você a acata. Elias é libertado, e sua imagem começa a ser restaurada com o apoio de psicólogos, juristas e movimentos sociais.""",
                    "attributes": {"Justice": 9, "Reputation": 6, "Empathy": 9, "Stress": 5}
                },
                "2.3.2": {
                    "title": "🕵️‍♂️ Investigação Discreta 🕵️‍♂️",
                    "text": """O histórico é usado no tribunal, mas parte da sociedade considera essa atitude preconceituosa. Não há provas materiais, mas o histórico negativo do conflito com a vítima influencia o júri, que o considera culpado. Elias é condenado, e mais tarde descobre-se que o verdadeiro autor do crime fugiu do país. A sua reputação como juiz é seriamente abalada.""",
                    "attributes": {"Justice": -5, "Reputation": -7, "Empathy": -4, "Stress": 10}
                },
                "2.3.3": {
                    "title": "📢 O Legado do Juiz 📢",
                    "text": """Você descobre que a vítima tinha envolvimento com um grupo de extorsão na região e que Elias havia sido uma das pessoas que se recusaram a pagar esse grupo. Essa descoberta muda completamente a narrativa: Elias passa a ser visto como possível alvo de uma armação. Uma nova investigação é aberta, o caso é suspenso, e Elias é libertado com apoio popular.""",
                    "attributes": {"Justice": 10, "Reputation": 9, "Empathy": 7, "Stress": 3}
                },
                "3.1.1": {
                    "title": "🤝 Compaixão e Lei 🤝",
                    "text": """Elias e seus familiares passam a receber ameaças. Com sua intervenção, a segurança deles é reforçada, evitando uma tragédia. Isso é bem visto por grupos de direitos humanos, mas criticado por setores conservadores. Um tempo depois, uma testemunha revela que a denúncia contra Elias foi fabricada. O verdadeiro culpado é preso, e sua postura preventiva é exaltada.""",
                    "attributes": {"Justice": 8, "Reputation": 7, "Empathy": 9, "Stress": 6}
                },
                "3.1.2": {
                    "title": "📚 O Educador da Justiça 📚",
                    "text": """A força-tarefa é bem recebida pela sociedade. Sem vínculo direto com o Judiciário, ela consegue novas evidências — inclusive um vídeo comprometedor de outro suspeito. Elias é oficialmente inocentado. Sua decisão de arquivar o processo é vista agora como prudente, e sua reputação cresce como a de um juiz ético e estratégico.""",
                    "attributes": {"Justice": 10, "Reputation": 10, "Empathy": 7, "Stress": 4}
                },
                "3.1.3": {
                    "title": "⚖️ Foco na Eficiência ⚖️",
                    "text": """Você age por fora do protocolo. As novas denúncias não são confirmadas, e seu ato é descoberto pela promotoria. Você é acusado de abuso de autoridade por tentar agir secretamente após arquivar o caso formalmente. Apesar da boa intenção, a mancha no seu histórico pesa. Elias continua em liberdade, mas você é afastado temporariamente do cargo.""",
                    "attributes": {"Justice": 4, "Reputation": -6, "Empathy": 6, "Stress": 9}
                },
                "3.2.1": {
                    "title": "🌪️ Silêncio e Desconfiança 🌪️",
                    "text": """Você conversa com a família de Elias. Eles estão assustados e desamparados. Sua postura humana e solidária os reconforta. Eles ganham confiança e coragem para falar publicamente. Isso muda a narrativa: Elias dá entrevista, conta sua versão e a sociedade começa a enxergar o erro. Sua empatia, ainda que silenciosa, causa grande impacto.""",
                    "attributes": {"Justice": 7, "Reputation": 6, "Empathy": 10, "Stress": 4}
                },
                "3.2.2": {
                    "title": "🤝 Apoio nos Bastidores 🤝",
                    "text": """Meses depois, você é questionado por um conselho superior. O relatório detalhado protege você de punições e mostra que a decisão de arquivar foi técnica, não política. O caso volta aos holofotes, mas você se mantém firme. Elias continua livre, e a investigação é reaberta por outra vara judicial. Sua reputação como um juiz estrategista cresce nos bastidores.""",
                    "attributes": {"Justice": 9, "Reputation": 8, "Empathy": 6, "Stress": 3}
                },
                "3.2.3": {
                    "title": "📉 Recuperação Tardía 📉",
                    "text": """O grupo assume o caso e descobre provas que haviam sido ignoradas. A nova investigação isenta Elias e expõe falhas policiais. Seu nome não aparece diretamente, mas jornalistas descobrem sua influência silenciosa. O público o enxerga como um juiz que age com sabedoria e sensibilidade. Elias passa a colaborar com o grupo, tornando-se ativista.""",
                    "attributes": {"Justice": 10, "Reputation": 9, "Empathy": 8, "Stress": 2}
                },
                "3.3.1": {
                    "title": "🌟 A Humanidade da Justiça 🌟",
                    "text": """O apoio institucional oferecido ajuda a família a lidar com o luto e canalizar a dor de forma construtiva. Eles participam de audiências públicas, criam um grupo de apoio a vítimas e passam a lutar por melhorias no sistema investigativo. Elias permanece livre e em segurança. Sua atuação é vista como firme, porém sensível.""",
                    "attributes": {"Justice": 9, "Reputation": 7, "Empathy": 10, "Stress": 5}
                },
                "3.3.2": {
                    "title": "🔎 O Caminho Contínuo da Justiça 🔎",
                    "text": """A família acata a sugestão e move um processo cível, acusando o Estado de omissão. Isso levanta debates importantes sobre falhas processuais. Você é chamado para prestar depoimento, mas seu equilíbrio e argumentação são elogiados. A decisão judicial é mantida, mas o caso vira referência para reformas jurídicas.""",
                    "attributes": {"Justice": 10, "Reputation": 8, "Empathy": 7, "Stress": 6}
                },
                "3.3.3": {
                    "title": "🔒 Discrição e Confiança 🔒",
                    "text": """Apesar da tensão inicial, o encontro ocorre com apoio de mediadores. Elias expressa empatia e dor pelas acusações que sofreu, enquanto os pais da vítima, mesmo inconformados, enxergam um ser humano diante deles, não um monstro. A conversa não resolve tudo, mas abre espaço para uma nova narrativa. A imprensa cobre o evento e elogia sua coragem.""",
                    "attributes": {"Justice": 8, "Reputation": 10, "Empathy": 10, "Stress": 7}

                }
            }

        }
    
    def clear_scroll_area(self):
        """Limpa todo o conteúdo da área de rolagem"""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def show_story_screen(self):
        """Mostra a tela da história atual baseada no estado"""
        self.clear_scroll_area()
        
        if self.story_state == "final_outcomes":
            self.show_final_outcome()
        else:
            self.show_choices_screen()
    
    def show_choices_screen(self):
        """Mostra a tela de escolhas e texto para os estados intermediários ou intro"""
        current_data = self.get_current_story_segment()
        
        if not current_data:
            QMessageBox.critical(self, "Erro de Jogo", "Segmento da história não encontrado. Reiniciando.")
            self.restart_game()
            return
        
        # Título
        title_label = QLabel(current_data["title"])
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #FFD700; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(title_label)
        
        # Texto da história
        text_label = QLabel(current_data["text"])
        text_label.setFont(QFont("Arial", 12))
        text_label.setStyleSheet("color: #D0D0D0; margin: 15px 0;")
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignJustify)
        self.scroll_layout.addWidget(text_label)
        
        # Grupo de botões para as escolhas
        self.choice_group = QButtonGroup()
        self.choice_group.setExclusive(True)
        
        # Criar botões para cada escolha
        for choice_text, choice_id in current_data["choices"]:
            choice_btn = QPushButton(choice_text)
            choice_btn.setFont(QFont("Arial", 11))
            choice_btn.setStyleSheet("""
                QPushButton {
                    background-color: #444444;
                    color: white;
                    padding: 12px;
                    border: none;
                    text-align: left;
                    margin: 8px 0;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #555555;
                }
                QPushButton:pressed {
                    background-color: #333333;
                }
                QPushButton:checked {
                    background-color: #007ACC;
                    color: white;
                }
            """)
            choice_btn.setCheckable(True)
            choice_btn.setCursor(Qt.PointingHandCursor)
            self.choice_group.addButton(choice_btn)
            self.choice_group.setId(choice_btn, choice_id)  # Agora usando ID numérico
            self.scroll_layout.addWidget(choice_btn)
        
        # Limpar botões de ação anteriores
        while self.action_buttons_layout.count():
            child = self.action_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Botão de Prosseguir
        continue_btn = QPushButton("🚀 Prosseguir")
        continue_btn.setFont(QFont("Arial", 12, QFont.Bold))
        continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0099EE;
            }
            QPushButton:pressed {
                background-color: #0055AA;
            }
        """)
        continue_btn.clicked.connect(self.process_choice)
        self.action_buttons_layout.addWidget(continue_btn)
        
        # Botão de Voltar (se não for a introdução)
        if len(self.current_choice_path) > 0:
            back_btn = QPushButton("↩️ Voltar")
            back_btn.setFont(QFont("Arial", 11))
            back_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF5733;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #FF7A55;
                }
                QPushButton:pressed {
                    background-color: #CC4028;
                }
            """)
            back_btn.clicked.connect(self.go_back)
            self.action_buttons_layout.addWidget(back_btn)
        
        # Botão de Reiniciar
        restart_btn = QPushButton("🔄 Reiniciar")
        restart_btn.setFont(QFont("Arial", 11))
        restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
        """)
        restart_btn.clicked.connect(self.restart_game)
        self.action_buttons_layout.addWidget(restart_btn)
    
    def process_choice(self):
        """Processa a escolha atual e avança para a próxima parte da história"""
        selected_button = self.choice_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione uma opção antes de prosseguir.")
            return
        
        selected_choice = self.choice_group.id(selected_button)
        current_segment_data = self.get_current_story_segment()
        
        if not current_segment_data:
            QMessageBox.critical(self, "Erro de Jogo", "Segmento da história atual não encontrado. Reiniciando.")
            self.restart_game()
            return
        
        # Adiciona a escolha ao caminho
        self.current_choice_path.append(selected_choice)
        
        # Determina o próximo estado
        if "next_container_key" in current_segment_data:
            self.story_state = current_segment_data["next_container_key"]
        elif "attributes" in current_segment_data:
            self.story_state = "final_outcomes"
        else:
            QMessageBox.critical(self, "Erro de Jogo", "Segmento de história mal definido. Reiniciando.")
            self.current_choice_path.pop()
            self.restart_game()
            return
        
        self.show_story_screen()
    
    
    
    def show_final_outcome(self):
        """Mostra o desfecho final da história"""
        self.clear_scroll_area()
        
        final_key = self.current_choice_path[-1] if self.current_choice_path else None
        if not final_key or final_key not in self.story.get("final_outcomes", {}):
            QMessageBox.critical(self, "Erro de Desfecho", "Desfecho final não encontrado. Reiniciando.")
            self.restart_game()
            return
        
        outcome = self.story["final_outcomes"][final_key]
        
        # Aplicar atributos
        for attr, value in outcome.get("attributes", {}).items():
            if attr in self.player_attributes:
                self.player_attributes[attr] += value
        
        # Título do resultado
        title_label = QLabel(outcome["title"])
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #FFD700; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(title_label)
        
        # Texto do resultado
        text_frame = QFrame()
        text_frame.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 15px;")
        text_layout = QVBoxLayout(text_frame)
        
        text_label = QLabel(outcome["text"])
        text_label.setFont(QFont("Arial", 12))
        text_label.setStyleSheet("color: #D0D0D0;")
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignJustify)
        text_layout.addWidget(text_label)
        
        self.scroll_layout.addWidget(text_frame)
        
        # Seção de informações sobre prisões injustas
        prison_title = QLabel("Prisões Injustas no Brasil")
        prison_title.setFont(QFont("Arial", 16, QFont.Bold))
        prison_title.setStyleSheet("color: #FF6347; margin-top: 30px; margin-bottom: 15px;")
        prison_title.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(prison_title)
        
        prison_frame = QFrame()
        prison_frame.setStyleSheet("background-color: #2a2a2a; border-radius: 5px; padding: 20px;")
        prison_layout = QVBoxLayout(prison_frame)
        
        prison_text = """Prisões Injustas no Brasil: o peso de uma decisão
No Brasil, centenas de pessoas são privadas de liberdade de forma indevida todos os anos. Uma das principais causas dessas prisões é a fragilidade das provas, como reconhecimentos fotográficos imprecisos ou testemunhos sem respaldo técnico. Entre 2012 e 2020, foram registradas ao menos 90 prisões injustas por reconhecimento fotográfico — sendo 73 apenas no estado do Rio de Janeiro, com predominância de vítimas negras e jovens.

A desigualdade racial e social, somada à pressa em resolver crimes, cria um terreno fértil para erros judiciais que custam a vida de inocentes. Em 2009, o então presidente do STF, ministro Gilmar Mendes, alertou que cerca de 20% das pessoas presas no país estavam em situação ilegal, seja por erros processuais ou ausência de provas sólidas.

Diante dessa realidade, iniciativas como o Innocence Project Brasil lutam para reverter condenações injustas e promover debates sobre as falhas estruturais do sistema."""
        
        prison_label = QLabel(prison_text)
        prison_label.setFont(QFont("Arial", 11))
        prison_label.setStyleSheet("color: #D0D0D0;")
        prison_label.setWordWrap(True)
        prison_label.setAlignment(Qt.AlignJustify)
        prison_layout.addWidget(prison_label)
        
        self.scroll_layout.addWidget(prison_frame)
        self.scroll_layout.addStretch()
        
        # Limpar botões de ação anteriores
        while self.action_buttons_layout.count():
            child = self.action_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Botão para continuar para reflexão
        continue_btn = QPushButton("Continuar para Reflexão →")
        continue_btn.setFont(QFont("Arial", 12, QFont.Bold))
        continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0099EE;
            }
            QPushButton:pressed {
                background-color: #0055AA;
            }
        """)
        continue_btn.clicked.connect(lambda: self.show_reflection_screen(outcome))
        self.action_buttons_layout.addWidget(continue_btn)
    
    def show_reflection_screen(self, outcome):
        """Mostra a tela de reflexão sobre a decisão"""
        self.clear_scroll_area()
        
        # Título da reflexão
        title_label = QLabel("Reflexão sobre sua Decisão")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #FFD700; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(title_label)
        
        # Texto de reflexão
        reflection_frame = QFrame()
        reflection_frame.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 20px;")
        reflection_layout = QVBoxLayout(reflection_frame)
        
        reflection_text = """E agora… repense sua decisão no caso de Elias
Você acaba de viver a história de Elias, um jovem negro acusado de um crime grave com base no relato de uma única testemunha que afirma tê-lo visto no local do crime. Durante o julgamento, você – no papel de juiz – teve que decidir se havia elementos suficientes para condená-lo ou se a dúvida deveria pesar a favor da liberdade.

O caso de Elias não é ficção isolada. Ele representa os muitos brasileiros que enfrentam a Justiça sem provas concretas, apenas com o peso do preconceito e da palavra de terceiros.

Agora que conhece os dados, os contextos e as consequências reais de decisões precipitadas, reflita:

🔍 Será que você julgou com base em evidências sólidas ou em suposições?
⚖️ Quantos Elias estão hoje atrás das grades por decisões semelhantes à que você tomou?
🧠 Se fosse com alguém que você ama… qual justiça você esperaria?

Na Pele e na Consciência não entrega respostas prontas. Ele te entrega a pergunta:
👉 Você faria diferente agora que sabe a verdade?"""
        
        reflection_label = QLabel(reflection_text)
        reflection_label.setFont(QFont("Arial", 12))
        reflection_label.setStyleSheet("color: #D0D0D0;")
        reflection_label.setWordWrap(True)
        reflection_label.setAlignment(Qt.AlignJustify)
        reflection_layout.addWidget(reflection_label)
        
        self.scroll_layout.addWidget(reflection_frame)
        self.scroll_layout.addStretch()
        
        # Limpar botões de ação anteriores
        while self.action_buttons_layout.count():
            child = self.action_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Botão para ver perfil e atributos
        profile_btn = QPushButton("Ver Meu Perfil e Atributos →")
        profile_btn.setFont(QFont("Arial", 12, QFont.Bold))
        profile_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0099EE;
            }
            QPushButton:pressed {
                background-color: #0055AA;
            }
        """)
        profile_btn.clicked.connect(lambda: self.show_final_profile(outcome))
        self.action_buttons_layout.addWidget(profile_btn)
    
    def show_final_profile(self, outcome):
        """Mostra os atributos finais e o perfil do jogador"""
        self.clear_scroll_area()
        
        # Determinar o perfil do jogador
        profile_name, profile_description = self.determine_player_profile()
        
        # Título do perfil
        title_label = QLabel("Seu Desempenho no Julgamento")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #FFD700; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(title_label)
        
        # Seção de atributos
        attributes_title = QLabel("Atributos Finais:")
        attributes_title.setFont(QFont("Arial", 14, QFont.Bold))
        attributes_title.setStyleSheet("color: white; margin-bottom: 15px;")
        self.scroll_layout.addWidget(attributes_title)
        
        # Tradução dos nomes dos atributos
        attr_translation = {
            "Justice": "Justiça",
            "Reputation": "Reputação",
            "Empathy": "Empatia",
            "Stress": "Estresse"
        }
        
        # Container para os atributos
        attributes_frame = QFrame()
        attributes_frame.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 20px;")
        attributes_layout = QVBoxLayout(attributes_frame)
        
        # Adicionar cada atributo
        for attr, value in self.player_attributes.items():
            attr_frame = QFrame()
            attr_frame.setStyleSheet("background-color: #444444; border-radius: 5px; padding: 15px;")
            attr_layout = QVBoxLayout(attr_frame)
            
            # Nome do atributo
            attr_name = QLabel(attr_translation.get(attr, attr))
            attr_name.setFont(QFont("Arial", 12, QFont.Bold))
            attr_name.setStyleSheet("color: white;")
            attr_layout.addWidget(attr_name)
            
            # Valor do atributo
            attr_value = QLabel(f"{value:+d}")
            attr_value.setFont(QFont("Arial", 14, QFont.Bold))
            attr_value.setStyleSheet("color: #FFD700;" if value >= 0 else "color: #FF6347;")
            attr_value.setAlignment(Qt.AlignCenter)
            attr_layout.addWidget(attr_value)
            
            # Barra de progresso (simulada)
            progress_frame = QFrame()
            progress_frame.setStyleSheet("background-color: #555555; border-radius: 3px;")
            progress_frame.setFixedHeight(25)
            progress_layout = QHBoxLayout(progress_frame)
            progress_layout.setContentsMargins(0, 0, 0, 0)
            
            progress_bar = QFrame()
            progress_bar.setStyleSheet("background-color: #4CAF50;" if value >= 0 else "background-color: #F44336;")
            width = min(abs(value) * 10, 220)
            progress_bar.setFixedWidth(width)
            progress_layout.addWidget(progress_bar)
            
            if value < 0:
                progress_layout.addStretch()
            
            attr_layout.addWidget(progress_frame)
            
            attributes_layout.addWidget(attr_frame)
        
        self.scroll_layout.addWidget(attributes_frame)
        
        # Seção de perfil personalizado
        profile_frame = QFrame()
        profile_frame.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 25px;")
        profile_layout = QVBoxLayout(profile_frame)
        
        profile_title = QLabel(f"Seu Perfil: {profile_name}")
        profile_title.setFont(QFont("Arial", 16, QFont.Bold))
        profile_title.setStyleSheet("color: #FFD700; margin-bottom: 15px;")
        profile_title.setAlignment(Qt.AlignCenter)
        profile_layout.addWidget(profile_title)
        
        profile_desc = QLabel(profile_description)
        profile_desc.setFont(QFont("Arial", 12))
        profile_desc.setStyleSheet("color: #E0E0E0;")
        profile_desc.setWordWrap(True)
        profile_desc.setAlignment(Qt.AlignJustify)
        profile_layout.addWidget(profile_desc)
        
        self.scroll_layout.addWidget(profile_frame)
        self.scroll_layout.addStretch()
        
        # Limpar botões de ação anteriores
        while self.action_buttons_layout.count():
            child = self.action_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Botões de ação
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(15)
        
        # Botão de Reiniciar
        restart_btn = QPushButton("🔄 Reiniciar Jogo")
        restart_btn.setFont(QFont("Arial", 11))
        restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
        """)
        restart_btn.clicked.connect(self.restart_game)
        buttons_layout.addWidget(restart_btn)
        
        # Botão de Sair
        exit_btn = QPushButton("🚪 Sair")
        exit_btn.setFont(QFont("Arial", 11))
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
        """)
        exit_btn.clicked.connect(self.close)
        buttons_layout.addWidget(exit_btn)
        
        self.action_buttons_layout.addWidget(buttons_frame)
    
    def determine_player_profile(self):
        """Determina o perfil do jogador com base nos atributos finais"""
        justice = self.player_attributes["Justice"]
        reputation = self.player_attributes["Reputation"]
        empathy = self.player_attributes["Empathy"]
        stress = self.player_attributes["Stress"]
        
        if empathy >= 7 and justice >= 5 and stress <= 8:
            return "Aliado Silencioso", "Você agiu com compaixão e buscou a justiça pelos meios menos ostensivos, construindo uma reputação de solidez e confiabilidade nos bastidores. Suas ações, embora discretas, tiveram um impacto significativo na vida de Elias e na reforma do sistema."
        elif justice >= 8 and (reputation >= 7 or empathy >= 7) and stress <= 10:
            return "Agente de Mudança", "Você se tornou um catalisador para transformações profundas no sistema judiciário, não hesitando em confrontar a corrupção e promover a transparência. Suas escolhas, embora desafiadoras, resultaram em um impacto duradouro e positivo, mas com um custo pessoal de estresse."
        else:
            return "Observador Neutro", "Suas decisões foram predominantemente técnicas e focadas na aplicação da lei, por vezes ignorando as nuances humanas ou a pressão externa. Sua postura, embora imparcial, pode ter levado a desfechos questionáveis ou a uma percepção de frieza, resultando em estresse variável."
    
    def get_current_story_segment(self):
        """Retorna o segmento atual da história baseado no estado atual"""
        if self.story_state == "intro":
            return self.story["intro"]
        
        if self.story_state in self.story and self.current_choice_path:
            current_container = self.story[self.story_state]
            chosen_key = self.current_choice_path[-1]
            
            if chosen_key in current_container:
                return current_container[chosen_key]
        
        return None
    
    def go_back(self):
        """Volta para a tela anterior"""
        if not self.current_choice_path:
            QMessageBox.information(self, "Informação", "Você já está na introdução do jogo.")
            return
        
        self.current_choice_path.pop()
        self.player_attributes = {
            "Justice": 0,
            "Reputation": 0,
            "Empathy": 0,
            "Stress": 0
        }
        
        if not self.current_choice_path:
            self.story_state = "intro"
        else:
            # Recalcula o story_state percorrendo o caminho
            temp_story_state = "intro"
            temp_current_segment = self.story["intro"]
            
            for choice_key in self.current_choice_path:
                if temp_story_state == "intro":
                    temp_story_state = temp_current_segment["next_container_key"]
                
                current_container = self.story.get(temp_story_state)
                if not current_container or choice_key not in current_container:
                    QMessageBox.critical(self, "Erro de Jogo", "Não foi possível retroceder. Reiniciando.")
                    self.restart_game()
                    return
                
                temp_current_segment = current_container[choice_key]
                
                if "next_container_key" in temp_current_segment:
                    temp_story_state = temp_current_segment["next_container_key"]
            
            self.story_state = temp_story_state
        
        self.show_story_screen()
    
    def restart_game(self):
        """Reinicia o jogo para o estado inicial"""
        self.current_choice_path = []
        self.story_state = "intro"
        self.player_attributes = {
            "Justice": 0,
            "Reputation": 0,
            "Empathy": 0,
            "Stress": 0
        }
        self.show_story_screen()
    # ... (adicionar os outros métodos restantes)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = MundoConscienciaElias()
    window.show()
    sys.exit(app.exec())