# 🎬 **LOCKMYSEAT**  
> Reserva de Assentos em Cinema  

## 🧠 **Disciplina**
**Fundamentos de Computação Concorrente, Paralela e Distribuída**  

📘 **Objetivo da Atividade:**  
Desenvolver uma solução prática que utilize **arquitetura distribuída**, aplicando os conceitos de **concorrência e paralelismo** em um contexto realista.  


## 🍿 **Sobre o Projeto**

**LOCKMYSEAT** é um sistema cliente-servidor que simula a **reserva de assentos em um cinema**. O projeto demonstra o uso de **threads, sincronização, comunicação entre processos e controle de concorrência**, garantindo que múltiplos usuários possam acessar o servidor ao mesmo tempo sem causar conflitos de dados.

## 🧩 **Arquitetura do Sistema**

**Modelo:** Cliente-Servidor (via TCP Socket)

## 🚀 **Funcionalidades**

| Função | Descrição |
| 🎞️ `Listar Sessões` | Mostra filmes, horários e número de assentos disponíveis
| 💺 `Ver Assentos` | Exibe um mapa visual (🟢 livres / 🔴 ocupados)
| 🎟️ `Reservar Assento` | Solicita reserva e aguarda resposta do servidor
| ❌ `Sair` | Encerra a conexão de forma segura
