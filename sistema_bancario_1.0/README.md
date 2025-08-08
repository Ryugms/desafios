# Desafio Dio Santander - Bootcamp Backend Python

## 🏦 Banco PAYPY – Sistema Bancário em Python

Este é um projeto simples de um sistema bancário feito em Python, com um menu interativo no terminal. Ele simula operações básicas como **depósito**, **saque**, e **visualização do extrato**.

---

## 🚀 Funcionalidades

- [x] Cadastro do usuário com nome
- [x] Depósito de valores
- [x] Saque com limite diário e por valor
- [x] Extrato com histórico de transações
- [x] Validações para operações inválidas
- [x] Interface de terminal com menu interativo

---

## 🧾 Regras de negócio

- O **limite por saque** é de R$ 500,00.
- O **número máximo de saques por sessão** é de 3.
- Valores inválidos (como negativos ou zero) não são aceitos.
- O extrato exibe todas as movimentações realizadas.

---

## 📦 Como usar

1. Execute o script com Python 3:

```bash
python banco_paypy.py
```

2. Interaja com o menu:

```
$$$$$$$$$$$$$$$$  BANCO PAYPY  $$$$$$$$$$$$$$$
##########           MENU           ##########
#                                            #
#     [1] DEPOSITAR                          #
#     [2] SACAR                              #
#     [3] EXTRATO                            #
#     [0] SAIR                               #
#                                            #
##############################################
```

3. Digite a opção desejada e siga as instruções no terminal.

---

## 📄 Exemplo de uso

```bash
Digite seu nome: Giovani
Bem vindo ao Banco PAYPY Giovani!

=> 1
Informe o valor do depósito: 1500
Deposito efetuado com sucesso!

=> 2
Digite o valor do saque: 300
Saque efetuado com sucesso!

=> 3
Depósito: R$ 1500.00
Saque: R$ 300.00

Saldo atual: R$ 1200.00
```

---

## 👨‍💻 Autor

Desenvolvido por **Giovani M. S.**

---

## 📚 Licença

Este projeto é de uso livre para fins educacionais. Compartilhe, modifique e melhore!
