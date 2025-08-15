## sistema_bancario_3.0 ##
# Versão em POO (programação Orientada a Objeto)#

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, date
import textwrap

# ==============================
# Constantes do sistema
# ==============================

AGENCIA_PADRAO = "0001"
LIMITE_SAQUE_VALOR = 500.0
LIMITE_SAQUES_DIA = 3

# ==============================
# Utilidades de formatação
# ==============================

class Formatador:
    @staticmethod
    def cpf(cpf: str) -> str:
        cpf = "".join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return cpf  # retorna como veio se não tiver 11 dígitos
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @staticmethod
    def telefone(telefone: str) -> str:
        t = "".join(filter(str.isdigit, telefone))
        if len(t) < 10:
            return telefone
        # (55) (DD) NNNN-NNNN ou NNNNN-NNNN
        parte_meio = f"{t[2:6]}-{t[6:10]}" if len(t) == 12 else f"{t[-9:-4]}-{t[-4:]}"
        return f"(55)({t[:2]}){parte_meio}"

    @staticmethod
    def endereco(endereco: str, largura: int = 40) -> str:
        return "\n".join(textwrap.wrap(endereco, largura))


# ================================
# Interface de Transação (POO)
# ================================

class Transacao(ABC):
    def __init__(self, valor: float):
        self.valor = float(valor)

    @abstractmethod
    def registrar(self, conta: "Conta") -> bool:
        """Executa a transação na conta e retorna True/False para sucesso."""
        raise NotImplementedError


class Deposito(Transacao):
    def registrar(self, conta: "Conta") -> bool:
        ok = conta.depositar(self.valor)
        return ok


class Saque(Transacao):
    def registrar(self, conta: "Conta") -> bool:
        ok = conta.sacar(self.valor)
        return ok


# ================================
# Histórico de transações
# ================================

class Historico:
    def __init__(self) -> None:
        # cada item: {"tipo": "Deposito"/"Saque", "valor": float, "data": datetime}
        self.transacoes: list[dict] = []

    def adicionar_transacao(self, transacao: Transacao) -> None:
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": float(transacao.valor),
                "data": datetime.now(),
            }
        )

    def saques_no_dia(self, dia: date | None = None) -> int:
        dia = dia or date.today()
        return sum(1 for t in self.transacoes
                   if t["tipo"] == "Saque" and t["data"].date() == dia)

    def listar(self) -> list[dict]:
        return list(self.transacoes)


# ================================
# Pessoas / Clientes
# ================================

class PessoaFisica:
    def __init__(self, cpf: str, nome: str, data_nascimento: str) -> None:
        self.cpf = "".join(filter(str.isdigit, cpf))
        self.nome = nome
        self.data_nascimento = data_nascimento  # manter string para simplicidade


class Cliente(PessoaFisica):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str) -> None:
        super().__init__(cpf, nome, data_nascimento)
        self.endereco = endereco
        self._contas: list[Conta] = []

    @property
    def contas(self) -> list["Conta"]:
        return list(self._contas)

    def adicionar_conta(self, conta: "Conta") -> None:
        self._contas.append(conta)

    def realizar_transacao(self, conta: "Conta", transacao: Transacao) -> None:
        if conta not in self._contas:
            print("Conta não pertence a este cliente.")
            return
        if transacao.registrar(conta):
            conta.historico.adicionar_transacao(transacao)


# ================================
# Contas
# ================================

class Conta(ABC):
    def __init__(self, numero: int, cliente: Cliente, agencia: str = AGENCIA_PADRAO) -> None:
        self._saldo: float = 0.0
        self._numero: int = numero
        self._agencia: str = agencia
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

    # ---- propriedades (leitura controlada) ----
    
    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    # ---- operações básicas ----
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Valor inválido para depósito.")
            return False
        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado.")
        return True

    @abstractmethod
    def sacar(self, valor: float) -> bool:
        """Cada tipo de conta aplica suas próprias regras de saque."""
        raise NotImplementedError

    # ---- extrato ----
    def exibir_extrato(self) -> None:
        print("\n############################ EXTRATO ###########################")
        
        print(f"Agência {self.agencia}  Conta {self.numero}  Cliente: {self.cliente.nome}")
        if not self.historico.listar():
            print("Nenhuma movimentação realizada.")
        else:
            for t in self.historico.listar():
                quando = t["data"].strftime("%d/%m/%Y %H:%M:%S")
                print(f"{quando} - {t['tipo']}: R$ {t['valor']:.2f}")
        print(f"Saldo atual: R$ {self.saldo:.2f}")

        print("################################################################\n")

    # ---- fábrica de contas ----
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> "Conta":
        """Fábrica; cada subclasse retorna sua própria instância."""
        return cls(numero=numero, cliente=cliente)


class ContaCorrente(Conta):
    # regras específicas (podem ser ajustadas por instância se quiser)
    def __init__(
        self,
        numero: int,
        cliente: Cliente,
        agencia: str = AGENCIA_PADRAO,
        limite: float = LIMITE_SAQUE_VALOR,
        limite_saques: int = LIMITE_SAQUES_DIA,
    ) -> None:
        super().__init__(numero, cliente, agencia)
        self.limite = float(limite)
        self.limite_saques = int(limite_saques)

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Valor inválido para saque.")
            return False
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False
        if valor > self.limite:
            print(f"Valor excede o limite de saque (R$ {self.limite:.2f}).")
            return False
        saques_hoje = self.historico.saques_no_dia()
        if saques_hoje >= self.limite_saques:
            print("Limite de saques diários excedido.")
            return False

        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado.")
        return True

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> "ContaCorrente":
        return cls(numero=numero, cliente=cliente)


# ==============================
# Banco (orquestra o fluxo)
# ==============================
class Banco:
    def __init__(self) -> None:
        self._clientes: list[Cliente] = []
        self._contas: list[Conta] = []

    # ---------- clientes ----------
    def cadastrar_cliente(self) -> None:
        cpf = input("CPF (apenas números): ").strip()
        if self._buscar_cliente_por_cpf(cpf):
            print("Já existe cliente com esse CPF.")
            return

        nome = input("Nome completo: ").strip()
        data_nasc = input("Data de Nascimento (dd/mm/aaaa): ").strip()
        endereco = input("Endereço (logradouro, nº - bairro - cidade - UF): ").strip()

        cliente = Cliente(cpf=cpf, nome=nome, data_nascimento=data_nasc, endereco=endereco)
        self._clientes.append(cliente)
        print("Cliente cadastrado com sucesso!")

    def listar_clientes(self) -> None:
        if not self._clientes:
            print("Nenhum cliente cadastrado.")
            return
        for c in self._clientes:
            print(f"\nCliente: {c.nome}")
            print(f"CPF: {Formatador.cpf(c.cpf)} - Nasc.: {c.data_nascimento}")
            print(f"Endereço:\n{Formatador.endereco(c.endereco)}")
            if c.contas:
                nums = ", ".join(f"{conta.numero} (Ag. {conta.agencia})" for conta in c.contas)
                print(f"Contas: {nums}")
            else:
                print("Contas: (nenhuma)")
        print()

    def _buscar_cliente_por_cpf(self, cpf: str) -> Cliente | None:
        cpf = "".join(filter(str.isdigit, cpf))
        return next((c for c in self._clientes if c.cpf == cpf), None)

    # ---------- contas ----------
    def criar_conta_corrente(self) -> None:
        cpf = input("Informe o CPF do cliente: ").strip()
        cliente = self._buscar_cliente_por_cpf(cpf)
        if not cliente:
            print("Cliente não encontrado. Cadastre primeiro.")
            return

        numero = len(self._contas) + 1
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero)
        cliente.adicionar_conta(conta)
        self._contas.append(conta)
        print(f"Conta criada: Agência {conta.agencia}  Número {conta.numero}")

    def listar_contas(self) -> None:
        if not self._contas:
            print("Nenhuma conta cadastrada.")
            return
        for conta in self._contas:
            print(
                f"Agência: {conta.agencia} | Conta: {conta.numero} | "
                f"Tipo: {conta.__class__.__name__} | Cliente: {conta.cliente.nome}"
            )

    def _buscar_conta_por_numero(self, numero: int) -> Conta | None:
        return next((c for c in self._contas if c.numero == numero), None)

    # ---------- operações ----------
    def operar_deposito(self) -> None:
        numero = int(input("Número da conta: "))
        conta = self._buscar_conta_por_numero(numero)
        if not conta:
            print("Conta não encontrada.")
            return
        valor = float(input("Valor do depósito: ").replace(",", "."))
        trans = Deposito(valor)
        conta.cliente.realizar_transacao(conta, trans)

    def operar_saque(self) -> None:
        numero = int(input("Número da conta: "))
        conta = self._buscar_conta_por_numero(numero)
        if not conta:
            print("Conta não encontrada.")
            return
        valor = float(input("Valor do saque: ").replace(",", "."))
        trans = Saque(valor)
        conta.cliente.realizar_transacao(conta, trans)

    def operar_extrato(self) -> None:
        numero = int(input("Número da conta: "))
        conta = self._buscar_conta_por_numero(numero)
        if not conta:
            print("Conta não encontrada.")
            return
        conta.exibir_extrato()


# ================================
# Programa principal (menu)
# ================================
def main() -> None:
    banco = Banco()

    menu = """
=====================================================================
|                          $ BANCO PAYPY $                          |
================================ MENU ===============================
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Novo Cliente
    [5] Nova Conta Corrente
    [6] Listar Clientes
    [7] Listar Contas
    [0] Sair
=====================================================================
=> """

    while True:
        opcao = input(textwrap.dedent(menu)).strip()

        if opcao == "1":
            banco.operar_deposito()
        elif opcao == "2":
            banco.operar_saque()
        elif opcao == "3":
            banco.operar_extrato()
        elif opcao == "4":
            banco.cadastrar_cliente()
        elif opcao == "5":
            banco.criar_conta_corrente()
        elif opcao == "6":
            banco.listar_clientes()
        elif opcao == "7":
            banco.listar_contas()
        elif opcao == "0":
            print(" Obrigado por utilizar nosso sistema!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
