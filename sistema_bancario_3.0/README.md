# 💰 Sistema Bancário 3.0 - (POO)

💳 Sistema Bancário 3.0

📌 Descrição
O Sistema Bancário 3.0 é uma evolução das versões anteriores, mantendo as funcionalidades essenciais para operações bancárias simples, como depósito, saque e visualização de extrato.

Nesta versão, foram realizadas melhorias na estrutura do código, organização de funções e legibilidade, mantendo as regras já estabelecidas anteriormente:

Limite máximo de saque: R$ 500,00 por operação

Quantidade máxima de saques por dia: 3 saques

⚙️ Funcionalidades
Criar clientes e contas

Depósito de valores

Saque com verificação de limite diário e valor máximo por saque

Extrato detalhado com histórico de movimentações

🚀 Melhorias em relação às versões anteriores
Estrutura modular, facilitando futuras atualizações

Código mais legível e organizado

Inclusão de funções para manipulação de clientes e contas



Este projeto é uma evolução de um sistema bancário simples, migrando de **dicionários e funções soltas** para uma **arquitetura orientada a objetos** com uso de:
- **Classes**
- **Herança**
- **Métodos abstratos**
- **@classmethod**
- **@staticmethod**
- **@property**
- **Interface (abstract base class) para transações**

O objetivo foi melhorar **organização, legibilidade, reutilização de código e escalabilidade**.

---

## 📌 Funcionalidades
- Criar clientes (pessoa física)
- Criar contas (corrente ou poupança)
- Realizar depósitos
- Realizar saques (com limite e quantidade máxima por dia)
- Listar clientes e contas
- Histórico de transações por conta
- Formatação de CPF, telefone e endereço

---

## 🏗 Arquitetura
O sistema segue a modelagem UML:

Cliente (Pessoa Física)
│
├── Conta
│ ├── Conta Corrente
│
├── Histórico de Transações
│
└── Interface Transação
├── Saque
└── Depósito


### **Principais Classes**
- **Cliente** → Armazena informações e gerencia contas.
- **PessoaFisica** → Especialização de Cliente.
- **Conta** → Classe base para contas bancárias.
- **ContaCorrente** → Conta com limite e limite de saques.
- **Historico** → Registro das transações.
- **Transacao (Interface)** → Define contrato para operações (saque e depósito).
- **Saque / Deposito** → Implementam a interface de transação.

---

## 📂 Estrutura de Arquivos
📦 sistema-bancario 3.0
┣ 📜 sistema_bancario_3.0.py # Arquivo principal do sistema
┣ 📜 README.md # Este documento
┗ 📜 requirements.txt # Dependências (se necessário)


---

## ⚙️ Como Executar
1. **Clone o repositório**

git clone https://github.com/Ryugms/sistema-bancario.git
cd sistema_bancario_3.0

2. ** (Opcional) Crie um ambiente virtual**
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

3. ** Execute o programa **
pyhton sistema_bancario_3.0.py

🖥 Exemplo de Uso

================ MENU ================
[1] Novo Usuário
[2] Nova Conta
[3] Depositar
[4] Sacar
[5] Extrato
[6] Listar Usuários
[7] Listar Contas
[0] Sair
=======================================
=> 1
Nome: João
CPF: 12345678901
...
Usuário cadastrado com sucesso!

🛠 Tecnologias Utilizadas
Python 3.10+

Módulo abc para criação de interfaces

POO (Herança, Abstração, Encapsulamento, Polimorfismo)

📜 Licença
Este projeto é de uso livre para fins de estudo e pode ser adaptado conforme necessário.

✍ Autor: [Giovani Menezes]
📅 Versão: 3.0
