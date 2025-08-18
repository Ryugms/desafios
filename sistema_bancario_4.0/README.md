# 💰 Sistema Bancário 4.0

Um sistema bancário em **Python** que implementa operações de depósito, saque, extrato, cadastro de clientes e contas, com **decoradores de logs**, **iteradores personalizados** e **relatórios de contas**.

## 📌 Funcionalidades

- Criar clientes e contas (corrente ou poupança).
- Realizar **depósitos** e **saques** com limite diário configurável.
- Consultar **extrato** detalhado das transações.
- Gerar **relatórios de contas**, incluindo:
  - Data e hora de criação da conta.
  - Quantidade de saques realizados no dia atual.
- Listar clientes e contas.
- Iterar sobre contas com um **iterador personalizado**.
- Logs automáticos de cada transação realizada com sucesso.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- Módulos nativos: `abc`, `datetime`, `textwrap`

## 📂 Estrutura do Projeto

```
📦 sistema-bancario-4.0
 ┣ 📜 sistema_bancario.py   # Código principal do sistema
 ┣ 📜 README.md             # Documentação do projeto
```

## ▶️ Como Executar

1. Clone este repositório:

   ```bash
   [git clone https://github.com/Ryugms/desafios/tree/main/sistema_bancario_4.0.git
   ```

2. Entre na pasta do projeto:

   ```bash
   cd sistema_bancario_4.0
   ```

3. Execute o script principal:

   ```bash
   python sistema_bancario_4.0.py
   ```

## 📖 Menu Principal

```
===========================================================
|                 $ BANCO PAYPY $                         |
=========================== MENU ==========================
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Novo Usuário
        [5] Nova Conta
        [6] Listar Usuários
        [7] Listar Contas
        [8] Gerar Relatórios
        [9] Listar Contas (Iterador)
        [0] Sair
===========================================================
```

## 📊 Exemplo de Relatório Gerado

```
===== RELATÓRIO DE CONTAS =====

Cliente: João Silva
Agência: 0001 Conta: 1 Tipo: ContaCorrente
Saldo: R$ 1500.00
Data de criação: 17/08/2025 15:30:22
Saques realizados hoje: 2

=================================
```

---

👨‍💻 Desenvolvido em Python para estudos de **POO, decoradores, iteradores e logs**.

Autor: Giovani Menezes
