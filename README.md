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


---

## 🖥️ Instalação e Execução

### 1. Clone o repositório

git clone https://github.com/seu-usuario/NaPeleEnaConsciencia.git
cd NaPeleEnaConsciencia

Instale as bibliotecas necessárias: 
Biblioteca PySide6 - pip install pyside6 
Biblioteca dotenv - pip install dotenv 

---

🔒 Segurança
Verificação em dois fatores por e-mail.

Banco de dados local com controle completo do usuário.

Campos sensíveis protegidos por variáveis de ambiente.

---
👥 Créditos
Este projeto foi idealizado como ferramenta educacional para desenvolvimento da empatia, consciência ética e análise crítica de decisões. 
Desenvolvido por Ana Souza 

