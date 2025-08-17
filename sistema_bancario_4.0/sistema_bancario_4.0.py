## Sistema Bancário 4.0 ##

from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# ==============================
# Constantes
# ==============================
LIMITE_SAQUES = 3
LIMITE = 500
AGENCIA = "0001"


# ==============================
# Decorador de Logs
# ==============================
def log_transacao(func):
    def wrapper(self, *args, **kwargs):
        resultado = func(self, *args, **kwargs)
        if resultado:  # Só registra o log se a transação foi bem-sucedida
            data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            tipo = func.__name__.capitalize()
            log = f"[{data_hora}] {tipo} efetuado com sucesso!"
            self._extrato.append(data_hora)  # grava no histórico
            print(f"[LOG] {log}")       # printa no console
        return resultado
    return wrapper


# ==============================
# Classe utilitária
# ==============================
class Formatador:
    @staticmethod
    def cpf(cpf):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @staticmethod
    def telefone(telefone):
        return f"(55)({telefone[:2]}){telefone[2:6]}-{telefone[6:]}"

    @staticmethod
    def data_nascimento(data_nascimento):
        return f"{data_nascimento[:2]}/{data_nascimento[2:4]}/{data_nascimento[4:]}"

    @staticmethod
    def endereco(endereco, largura=40):
        return "\n".join(textwrap.wrap(endereco, largura))


# ==============================
# Classe Pessoa e Cliente
# ==============================
class Pessoa:
    def __init__(self, nome, estado_civil, data_nascimento, cpf, telefone, endereco):
        self.nome = nome
        self.estado_civil = estado_civil
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco

    @property
    def nome_completo(self):
        return f"{self.nome}"


class Cliente(Pessoa):
    def __init__(self, nome, estado_civil, data_nascimento, cpf, telefone, endereco):
        super().__init__(nome, estado_civil, data_nascimento, cpf, telefone, endereco)
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# ==============================
# Classe Conta (abstrata)
# ==============================
class Conta(ABC):
    def __init__(self, cliente, numero):
        self._cliente = cliente
        self._agencia = AGENCIA
        self._numero = numero
        self._saldo = 0.0
        self._extrato = []
        self._numero_saques = 0

    @property
    def saldo(self):
        return self._saldo

    @property
    def cliente(self):
        return self._cliente

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @abstractmethod
    def sacar(self, valor):
        pass

    @log_transacao
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._extrato.append(f"Depósito: R$ {valor:.2f}")
            print("Depósito realizado com sucesso!")
            return True
        else:
            print("Valor inválido para depósito.")
            return False

    def exibir_extrato(self):
        print("\n####################### EXTRATO ######################")
        if self._extrato:
            for mov in self._extrato:
                print(mov)
        else:
            print("Nenhuma movimentação realizada.")
        print(f"Saldo atual: R$ {self._saldo:.2f}")
        print("######################################################\n")

    # ===== Gerador de Relatórios =====
    def gerar_transacoes(self, tipo=None):
        """Gerador de transações da conta, com filtro opcional por tipo."""
        for transacao in self._extrato:
            if not tipo or tipo.lower() in transacao.lower():
                yield transacao


# ==============================
# Contas específicas
# ==============================
class ContaCorrente(Conta):
    @log_transacao
    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        elif valor > LIMITE:
            print("Valor excede o limite de saque.")
            return False
        elif self._numero_saques >= LIMITE_SAQUES:
            print("Limite de saques diários excedido.")
            return False
        elif valor > 0:
            self._saldo -= valor
            self._extrato.append(f"Saque: R$ {valor:.2f}")
            self._numero_saques += 1
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Valor inválido.")
            return False


class ContaPoupanca(Conta):
    @log_transacao
    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        elif valor > 0:
            self._saldo -= valor
            self._extrato.append(f"Saque: R$ {valor:.2f}")
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Valor inválido.")
            return False


# ==============================
# Iterador personalizado
# ==============================
class ContaIterador:
    """Itera sobre uma lista de contas retornando informações básicas."""
    def __init__(self, contas):
        self._contas = contas
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self._contas):
            raise StopIteration
        conta = self._contas[self._i]
        self._i += 1
        return (
            f"Agência: {conta.agencia} | Conta: {conta.numero} | "
            f"Tipo: {conta.__class__.__name__} | Cliente: {conta.cliente.nome_completo} | "
            f"Saldo: R$ {conta.saldo:.2f}"
        )


# ==============================
# Classe Banco
# ==============================
class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def cadastrar_cliente(self):
        cpf = input("CPF (apenas números): ").strip()
        if any(c.cpf == cpf for c in self.clientes):
            print("Usuário já cadastrado com este CPF.")
            return

        nome = input("Nome: ").strip()
        estado_civil = input("Estado Civil: ").strip()
        data_nascimento = input("Data de Nascimento (DDMMAAAA): ").strip()
        telefone = input("Telefone (DDD + número): ").strip()
        endereco = input("Endereço: ").strip()

        cliente = Cliente(nome, estado_civil, data_nascimento, cpf, telefone, endereco)
        self.clientes.append(cliente)
        print("Usuário cadastrado com sucesso!")

    def listar_clientes(self):
        for c in self.clientes:
            print(f"{c.nome_completo} \n - Nasc.: {Formatador.data_nascimento(c.data_nascimento)} - CPF: {Formatador.cpf(c.cpf)}")
            print(f" - Tel: {Formatador.telefone(c.telefone)} Estado Civil: {c.estado_civil} \n - {Formatador.endereco(c.endereco)}\n")

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ").strip()
        cliente = next((c for c in self.clientes if c.cpf == cpf), None)

        if not cliente:
            print("Usuário não encontrado. Cadastre primeiro.")
            return

        tipo = input("Tipo da conta, [1] corrente, [2] poupanca: ").strip()
        numero = len(self.contas) + 1

        if tipo == "1":
            conta = ContaCorrente(cliente, numero)
        elif tipo == "2":
            conta = ContaPoupanca(cliente, numero)
        else:
            print("Tipo inválido.")
            return

        cliente.adicionar_conta(conta)
        self.contas.append(conta)
        print(f"Conta criada com sucesso! Agência: {AGENCIA} Conta: {numero}")

    def gerar_relatorio(self, filtro=None):
        print("\n===== RELATÓRIO DE CONTAS =====")
        for conta in self.contas:
            if not filtro or isinstance(conta, filtro):
                print(f" - {conta.__class__.__name__} | Agência: {conta.agencia} Conta: {conta.numero} | Cliente: {conta.cliente.nome_completo} | Saldo: R$ {conta.saldo:.2f}")
        print("=================================\n")

    def listar_contas(self):
        for conta in self.contas:
            print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Tipo: {conta.__class__.__name__}, Cliente: {conta.cliente.nome_completo}")

    # ---- NOVO: Listagem via iterador personalizado ----
    def listar_contas_iterador(self):
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        print("\n===== LISTA DE CONTAS (via iterador) =====")
        for info in ContaIterador(self.contas):
            print(info)
        print("=========================================\n")


# ==============================
# Programa principal
# ==============================
def main():
    banco = Banco()

    menu_texto = """
    ===========================================================
    |		      $ BANCO PAYPY $			      |
    =========================== MENU =========================
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
    => """

    while True:
        opcao = input(textwrap.dedent(menu_texto))

        if opcao == "1":
            numero = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero == numero), None)
            if conta:
                valor = float(input("Valor para depósito: "))
                conta.depositar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == "2":
            numero = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero == numero), None)
            if conta:
                valor = float(input("Valor para saque: "))
                conta.sacar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == "3":
            numero = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero == numero), None)
            if conta:
                conta.exibir_extrato()
                # exemplo de uso do gerador de relatórios:
                print("\n--- Transações filtradas (saques) ---")
                for t in conta.gerar_transacoes("saque"):
                    print(t)
            else:
                print("Conta não encontrada.")

        elif opcao == "4":
            banco.cadastrar_cliente()

        elif opcao == "5":
            banco.criar_conta()

        elif opcao == "6":
            banco.listar_clientes()

        elif opcao == "7":
            banco.listar_contas()

        elif opcao == "8":
            banco.gerar_relatorio()

        elif opcao == "9":
            banco.listar_contas_iterador()

        elif opcao == "0":
            print("Obrigado por utilizar nosso sistema!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
