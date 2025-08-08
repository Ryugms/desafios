# 💰 Banco PayPy — Sistema Bancário v2.0

Um sistema bancário simples em **Python**, totalmente baseado em **funções** e com suporte a **múltiplos usuários e contas**.  
Permite operações de **depósito**, **saque**, **extrato**, cadastro de usuários e contas, além de listagem das informações.

---

## 📜 Funcionalidades

- **Cadastro de usuários** com:
  - Nome e Sobrenome
  - Data de nascimento
  - CPF (somente números, armazenado sem pontuação e formatado ao exibir)
  - Telefone no formato `(55)(DDD)XXXX-XXXX`
  - Endereço no formato `"logradouro, nº - bairro - cidade - estado"`

- **Cadastro de contas**:
  - Agência fixa `0001`
  - Tipos: **Corrente** ou **Poupança**
  - Numeração sequencial a partir de `1`
  - Um CPF por usuário (mas um usuário pode ter várias contas)
  - Uma conta só pode existir se vinculada a um usuário

- **Operações bancárias**:
  - Depósito
  - Saque (limite R$500 por saque e até 3 saques por dia)
  - Extrato com data e histórico de movimentações

- **Listagem**:
  - Usuários cadastrados
  - Contas cadastradas

---

## 🛠 Estrutura do Código

O código está organizado em funções:

- `cadastrar_usuario()`
- `listar_usuarios()`
- `criar_conta()`
- `listar_contas()`
- `depositar(saldo, valor, extrato, /)` — **positional only**
- `sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques)` — **keyword only**
- `exibir_extrato(saldo, /, *, extrato)` — **positional + keyword only**

Além de funções auxiliares:
- `formatar_cpf(cpf)`
- `formatar_telefone(telefone)`

---

## ▶️ Como Executar

1. **Clone o repositório** ou copie o arquivo `banco_paypy.py`.
2. Certifique-se de ter o **Python 3.8+** instalado.
3. No terminal, execute:
   ```bash
   python banco_paypy.py
   ```
4. Use o menu interativo para realizar operações.

---

## 📋 Menu do Sistema

```
===========================================================
|                  $ BANCO PAYPY $                        |
|                                                         |
=========================== MENU =========================
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Novo Usuário
        [5] Nova Conta
        [6] Listar Usuários
        [7] Listar Contas
        [0] Sair
===========================================================
```

---

## 📌 Regras de Operação

- **Depósito**: valor deve ser positivo.
- **Saque**:
  - Máximo R$500 por saque.
  - Máximo de 3 saques por dia.
  - Valor não pode ser negativo ou zerado.
  - Deve haver saldo suficiente.
- **Extrato**:
  - Mostra data da consulta.
  - Mostra movimentações e saldo atual.

---

## 📅 Histórico de Versões

- **v1.0**: Script inicial simples, sem modularização.
- **v2.0**:  
  - Modularização com funções.
  - Suporte a múltiplos usuários e contas.
  - CPF e telefone formatados.
  - Limites de saque implementados.
  - Extrato com data.
  - Listagem de usuários e contas.

---

## 📜 Licença
Projeto desenvolvido para fins educacionais. Uso livre.
