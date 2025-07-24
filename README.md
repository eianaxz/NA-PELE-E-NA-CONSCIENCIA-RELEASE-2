# NA-PELE-E-NA-CONSCIENCIA-RELEASE-2

# 🧠 Na Pele e na Consciência – Release 2.0

**Versão 2.0** do simulador interativo de dilemas éticos e sociais, com foco em empatia, consciência crítica e tomada de decisões responsáveis. 
Esta versão traz uma interface modernizada, novos modos de jogo e um sistema mais robusto e acessível.



# ✨ Novidades da Release 2.0

- 🔄 **Interface gráfica reformulada** com **PySide6**, trazendo um design minimalista, moderno e mais fluido.
- ⏳ **Modo de Decisão com Tempo**: o usuário tem 15 segundos para escolher, simulando decisões sob pressão cognitiva.
- 📊 **Sistema de Progresso**:
  - Histórias **não iniciadas**
  - Histórias **em andamento**
  - Histórias **concluídas**
- 🌐 **Aba de Comunidade (simulada)**: visualização de perfis éticos de outros usuários (em desenvolvimento).
- 🧾 **Aba Sobre atualizada**: nova descrição da versão, objetivos e mudanças.
- 📈 Otimizações no sistema de autenticação e feedback visual das escolhas.

---

## 📌 Funcionalidades Principais

### 👤 Cadastro e Login com 2FA
- CRUD completo de usuários.
- Verificação por e-mail com código de autenticação via `smtplib`.

### 📚 Módulo de Consciência
- Histórias interativas com ramificações.
- Escolhas éticas com impacto direto no enredo e no perfil final do jogador.
- Perfil personalizado com atributos visuais e descritivos (ex: empatia, impulsividade, responsabilidade).

### ⏱️ Modo Pressão Decisória (Modo 2)
- Temporizador de 15 segundos para cada decisão.
- Reinício da história em caso de tempo esgotado.
- Baseado em estudos de psicologia moral e impulsividade (ex: BBC, 2022).

### 💾 Sistema de Progresso
- Registro do status de cada história.
- Retomada de histórias em andamento.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

| Tecnologia     | Função                                  |
|----------------|------------------------------------------|
| **Python 3.13** | Lógica principal e integração geral     |
| **PySide6**     | Interface gráfica (versão Qt para Python) |
| **SQLite3**     | Banco de dados local para progresso     |
| **smtplib**     | Envio de e-mails com código de verificação |
| **dotenv**      | Gerenciamento seguro de variáveis (e-mail/senha) |


---
## ⚠️ Aviso sobre Funcionalidades em Desenvolvimento
Apesar dos esforços intensos para implementar todas as funcionalidades propostas nesta segunda release, algumas partes do sistema ainda não foram finalizadas ou integradas completamente, como:

Integração completa do CRUD de usuários e histórias.

Funcionamento pleno do Modo de Decisão com Tempo (Modo 2) para todas as histórias.

Ativação total da Aba Comunidade com exibição de perfis reais.

Essa limitação ocorreu devido a problemas técnicos enfrentados durante o processo de desenvolvimento, como falhas no editor de código (VSCode) e perda total da maiorias dos arquivos do sistema, que dificultaram a execução e depuração do sistema. 

Mesmo assim, grande parte da estrutura do sistema foi desenvolvida com responsabilidade e comprometimento, e as funcionalidades principais como cadastro e login com autenticação, interface gráfica modernizada, navegação pelo módulo de consciência e sistema de progresso estão devidamente implementadas e funcionando.

🛠️ O projeto continua em desenvolvimento, e o objetivo é que todas as funcionalidades sejam entregues e refinadas em versões futuras, mantendo a proposta pedagógica e ética que originou o sistema.

---

## 🖥️ Instalação e Execução

 Certifique-se de ter o Python 3.10+ instalado Baixe em: https://www.python.org/downloads/

Instale as bibliotecas externas necessárias: pip install python-dotenv e pip install pyside6

📥 Como clonar o repositório em qualquer sistema operacional Passos para clonar o projeto no seu computador: Abra o terminal ou prompt de comando

Windows: use o Prompt de Comando (CMD), PowerShell ou o terminal do VS Code.

Linux/macOS: use o Terminal padrão.

Navegue até a pasta onde deseja salvar o projeto Use o comando cd para entrar na pasta desejada. Exemplos:

Windows: cd C:\Users\SeuNomeDeUsuário\Documentos

Linux/macOS: cd /home/seuusuario/Documentos Substitua SeuNomeDeUsuário ou seuusuario pelo seu nome real no sistema.

Clone o repositório usando o comando:

git clone https://github.com/eianaxz/NA-PELE-E-NA-CONSCIENCIA-RELEASE-2.git Este comando criará uma nova pasta chamada NA-PELE-E-NA-CONSCI-NCIA---PROJETO dentro da pasta onde você está, contendo todos os arquivos do projeto.

Entre na pasta do projeto clonado cd NA-PELE-E-NA-CONSCI-NCIA---RELEASE 2

Para iniciar o projeto, execute o arquivo principal no terminal com: python cadastro.py

---

🔒 Segurança
Verificação em dois fatores por e-mail.

Banco de dados local com controle completo do usuário.

Campos sensíveis protegidos por variáveis de ambiente.

---
👥 Créditos
Este projeto foi idealizado como ferramenta educacional para desenvolvimento da empatia, consciência ética e análise crítica de decisões. 
Desenvolvido por Ana Souza 

