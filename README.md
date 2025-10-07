# 🎬 **LOCKMYSEAT**  
> Reserva de assentos em cinema  

## 🧠 **Disciplina**
**Fundamentos de Computação Concorrente, Paralela e Distribuída**  

📘 **Objetivo da atividade:**  
Desenvolver uma solução prática que utilize **arquitetura distribuída**, aplicando os conceitos de **concorrência e paralelismo** em um contexto realista.  

## 🍿 **Sobre o projeto**

**LOCKMYSEAT** é um sistema cliente-servidor que simula a **reserva de assentos em um cinema**. O projeto demonstra o uso de **threads, sincronização, comunicação entre processos e controle de concorrência**, garantindo que múltiplos usuários possam acessar o servidor ao mesmo tempo sem causar conflitos de dados.

## 🧩 **Arquitetura do sistema**

**Modelo:** Cliente-Servidor (via TCP Socket)

## 🚀 **Funcionalidades**

1. `Listar Sessões` | Mostra filmes, horários e número de assentos disponíveis
2. `Ver Assentos` | Exibe um mapa visual (🟢 livres / 🔴 ocupados)
3. `Reservar Assento` | Solicita reserva e aguarda resposta do servidor
4. `Sair` | Encerra a conexão de forma segura

## 🖥️ **Como executar**

### 1. Clonar o repositório

Abra o terminal e execute:

1. `bash`
2. `git clone https://github.com/<seu-usuario>/lockmyseat.git`
3. `cd lockmyseat`

### 2. Iniciar o servidor

No diretório do projeto, execute:

`python server.py`

O servidor será iniciado em localhost:5555 (porta padrão). Ele ficará escutando conexões dos clientes e exibirá no terminal quando cada cliente se conectar.

### 3. Iniciar um ou mais clientes

Em outro terminal, execute:

`python client.py`

ou especifique o host e a porta manualmente:

`python client.py localhost 5555`

O cliente abrirá um menu interativo. Pressione `Ctrl + C` no terminal do servidor para finalizar a execução.

## 🧰 **Tecnologias Utilizadas**

Python 3.x
📦 Bibliotecas:

1. `socket` → comunicação TCP
2. `threading` → paralelismo e sincronização
3. `time, datetime` → logs e delays
4. `json` → manipulação de dados das sessões

## 👩‍💻 **Autoria**

1. Débora Buriti
2. Mirella Santana
3. Myllena Navarro

ADS B (Embarque) | 4° período
