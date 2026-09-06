# 🔒 Multi-Client Encrypted Chat & Stress Testing

> Sistema de chat cliente-servidor multithread em **Python** com arquitetura de criptografia híbrida (**RSA-2048 + Fernet/AES-128-CBC**) e módulo integrado de **testes de estresse e carga de rede**.

---

## 📌 Visão Geral

Este projeto implementa uma aplicação de chat em tempo real via sockets TCP, focando em **segurança de dados em trânsito** e **concorrência multithread**.

A troca de mensagens utiliza um modelo de **criptografia híbrida**:
1. O servidor gera um par de chaves assimétricas **RSA-2048**.
2. Cada cliente, ao se conectar, recebe a chave pública do servidor e envia uma chave simétrica efêmera (**Fernet / AES-128**) cifrada com essa chave RSA.
3. Todas as mensagens subsequentes trocadas entre o cliente e o servidor são protegidas por criptografia simétrica autenticada com HMAC.

Além do sistema de mensagens, o repositório conta com uma suíte de **teste de estresse (stress testing)** automatizada que avalia a vazão, latência e resiliência do servidor sob diferentes volumes de conexões, pacotes e tamanhos de payload.

---

## ✨ Principais Funcionalidades

- 💬 **Comunicação Multiusuário em Tempo Real**:
  - Broadcast de mensagens para todos os participantes conectados.
  - Notificação automática de entrada e desconexão de clientes.
- 🔐 **Criptografia Híbrida de Ponta**:
  - **RSA-2048** com padding **OAEP (MGF1 + SHA-256)** para handshake seguro e troca de chave de sessão.
  - **Fernet (AES-128 em modo CBC com assinatura HMAC-SHA256)** para cifragem rápida e autenticada de mensagens e nomes de usuário.
- ⚡ **Arquitetura Multithread**:
  - Cada conexão de cliente é gerenciada de forma assíncrona por uma thread dedicada no servidor.
  - No cliente, uma thread ouvinte independente garante recebimento contínuo sem bloquear a entrada do terminal.
- 📊 **Módulo de Stress Test Parametrizado**:
  - Simula cenários de carga variando conexões simultâneas (10 a 500), quantidade de mensagens (10 a 1.000) e tamanhos de payload (100 B a 10 KB).
  - Coleta e exibe tempo total de execução e latência média por mensagem em formato tabular.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3](https://www.python.org/) (módulos nativos `socket`, `threading`, `itertools`, `time`)
- **Criptografia:** Biblioteca [`cryptography`](https://cryptography.io/) (módulos `hazmat` e `fernet`)
- **Protocolo de Transporte:** TCP / IP

---

## 📁 Estrutura de Arquivos

```text
.
├── crypto_utils.py     # Métodos de criptografia RSA (geração, serialização, OAEP) e Fernet
├── server.py           # Classes ChatServer e ClientHandler (gerenciamento de conexões e broadcast)
├── client.py           # Classe ChatClient (conexão, handshake criptográfico e thread de escuta)
├── main_server.py      # Ponto de entrada para iniciar o servidor de chat
├── main_client.py      # Ponto de entrada CLI interativo para o usuário conversar
├── stress_test.py      # Script de benchmark e teste de estresse de conexões e carga
└── README.md           # Documentação do projeto
