## Sistema Bancario 4.0 ##

from abc import ABC, abstractmethod
from datetime import datetime, date
import textwrap

# ==============================
# Constantes
# ==============================
LIMITE_SAQUES = 10
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
            self._extrato.append(log)  # grava no histórico
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
        self._data_ultimo_saque = date.today()
        self._criada_em = datetime.now()   # data/hora de criação da conta

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

    @property
    def criada_em(self):
        return self._criada_em

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

    # Extrato corrigido
    def exibir_extrato(self) -> None:
        print("\n############################ EXTRATO ###########################")
        print(f"Agência {self.agencia}  Conta {self.numero}  Cliente: {self.cliente.nome}")
        if not self._extrato:
            print("Não foram realizadas movimentações.")
        else:
            for mov in self._extrato:
                print(mov)
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print("################################################################\n")

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
    def __init__(
        self,
        cliente: Cliente,
        numero: int,
        limite: float = LIMITE,
        limite_saques: int = LIMITE_SAQUES,
    ) -> None:
        super().__init__(cliente, numero)
        self.limite = float(limite)
        self.limite_saques = int(limite_saques)

    @log_transacao
    def sacar(self, valor):
        hoje = date.today()
        if self._data_ultimo_saque != hoje:
            self._numero_saques = 0
            self._data_ultimo_saque = hoje

        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        elif valor > self.limite:
            print("Valor excede o limite de saque.")
            return False
        elif self._numero_saques >= self.limite_saques:
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
        hoje = date.today()
        if self._data_ultimo_saque != hoje:
            self._numero_saques = 0
            self._data_ultimo_saque = hoje

        if valor > self._saldo:
            print("Saldo insuficiente.")
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
            f"Cliente: {conta.cliente.nome_completo} |\n Agência: {conta.agencia} |"
            f" Conta: {conta.numero} | Tipo: {conta.__class__.__name__} | Saldo: R$ {conta.saldo:.2f}"
        )


# ==============================
# Classe Banco
# ==============================
class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    # Opção 4
    def cadastrar_cliente(self):
        cpf = input("CPF (apenas números): ").strip()
        if any(c.cpf == cpf for c in self.clientes):
            print("Usuário já cadastrado com este CPF.")
            return

        nome = input("Nome Completo: ").strip()
        estado_civil = input("Estado Civil: ").strip()
        data_nascimento = input("Data de Nascimento (DDMMAAAA): ").strip()
        telefone = input("Telefone (DDD + número): ").strip()
        endereco = input("Endereço: ").strip()

        cliente = Cliente(nome, estado_civil, data_nascimento, cpf, telefone, endereco)
        self.clientes.append(cliente)
        print("Usuário cadastrado com sucesso!")

    # Opção 6
    def listar_clientes(self):
        for c in self.clientes:
            print(f"\n   {c.nome_completo} \n - Nasc.: {Formatador.data_nascimento(c.data_nascimento)} - CPF: {Formatador.cpf(c.cpf)}")
            print(f" - Tel: {Formatador.telefone(c.telefone)} Estado Civil: {c.estado_civil} \n - {Formatador.endereco(c.endereco)}\n")

    # Opção 5
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

    # Opção 8
    def gerar_relatorio(self, filtro=None):
        print("\n===== RELATÓRIO DE CONTAS =====")
        for conta in self.contas:
            if not filtro or isinstance(conta, filtro):
                print(f"\nCliente: {conta.cliente.nome_completo}")
                print(f"Agência: {conta.agencia} Conta: {conta.numero} Tipo: {conta.__class__.__name__}")
                print(f"Saldo: R$ {conta.saldo:.2f}")
                print(f"Data de criação: {conta.criada_em.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"Saques realizados hoje: {conta._numero_saques}")
        print("=================================\n")

    # Opção 9
    def listar_contas(self):
        for conta in self.contas:
            print(f" Cliente: {conta.cliente.nome_completo}, Agência: {conta.agencia}, Conta: {conta.numero}, Tipo: {conta.__class__.__name__}")

    # ----  Listagem via iterador personalizado ----
    def listar_contas_iterador(self):
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        print("\n===== LISTA DE CONTAS (via iterador) =====")
        for info in ContaIterador(self.contas):
            print(info)
        print("=========================================\n")

def ler_numero(mensagem, tipo=int):
    while True:
        valor = input(mensagem).strip()
        if not valor:  # se vazio ou só espaço
            print("Opção inválida. Digite novamente.")
            continue
        try:
            return tipo(valor)  # tenta converter para int ou float
        except ValueError:
            print("Entrada inválida. Digite um número válido.")


def main():
    banco = Banco()

    menu_texto = """
    ===========================================================
    |		      $ BANCO PAYPY $			  |
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
    => """

    while True:
        opcao = input(textwrap.dedent(menu_texto)).strip()

        if opcao == "1":
            numero = ler_numero("Informe o número da conta: ", int)
            conta = next((c for c in banco.contas if c.numero == numero), None)
            if conta:
                valor = ler_numero("Valor para depósito: ", float)
                conta.depositar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == "2":
            numero = ler_numero("Informe o número da conta: ", int)
            conta = next((c for c in banco.contas if c.numero == numero), None)
            if conta:
                valor = ler_numero("Valor para saque: ", float)
                conta.sacar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == "3":
            numero = ler_numero("Informe o número da conta: ", int)
            conta = next((c for c in banco.contas if c.numero == numero), None)
            if conta:
                conta.exibir_extrato()
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
