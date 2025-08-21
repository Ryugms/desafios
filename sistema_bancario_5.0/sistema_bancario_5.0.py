# Sistema Bancário 5.0
import csv
import os
import textwrap
from abc import ABC, abstractmethod
from datetime import date, datetime

# ==============================
# Constantes
# ==============================
LIMITE_SAQUES = 10
LIMITE = 500
AGENCIA = "0001"
ARQUIVO_CLIENTES = "clientes.csv"
ARQUIVO_LOG = "log.txt"


# ==============================
# Utilidades de entrada segura
# ==============================
def ler_numero(mensagem, tipo=int):
    while True:
        valor = input(mensagem).strip()
        if not valor:
            print("Opção inválida. Digite novamente.")
            continue
        try:
            return tipo(valor)
        except ValueError:
            print("Entrada inválida. Digite um número válido.")


# ==============================
# Decorador de Logs
# ==============================
def log_transacao(func):
    def wrapper(self, *args, **kwargs):
        resultado = func(self, *args, **kwargs)
        if resultado:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tipo = func.__name__.capitalize()
            valor = args[0] if args else 0.0
            log = f"[{data_hora}] | " f"{tipo} | Valor: R$ {float(valor):.2f}"
            # registra em memória e no arquivo
            self._extrato.append(log)
            try:
                with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
                    f.write(log + "\n")
            except OSError as exc:
                print(f"[AVISO] Não foi possível escrever o log: {exc}")
            print(f"[LOG] {log}")
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
        if not telefone:
            return ""
        return f"(55)({telefone[:2]}){telefone[2:6]}-{telefone[6:]}"

    @staticmethod
    def data_nascimento(data_nascimento):
        if len(data_nascimento) == 8:
            return f"{data_nascimento[:2]}/{data_nascimento[2:4]}/{data_nascimento[4:]}"
        return data_nascimento

    @staticmethod
    def endereco(endereco, largura=40):
        return "\n".join(textwrap.wrap(endereco, largura)) if endereco else ""


# ==============================
# Classes de domínio
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


class Conta(ABC):
    def __init__(self, cliente, numero, saldo=0.0, criada_em=None, numero_saques=0):
        self._cliente = cliente
        self._agencia = AGENCIA
        self._numero = int(numero)
        self._saldo = float(saldo)
        self._extrato = []
        self._numero_saques = int(numero_saques)
        self._data_ultimo_saque = date.today()
        self._criada_em = (
            datetime.strptime(criada_em, "%Y-%m-%d %H:%M:%S")
            if isinstance(criada_em, str) and criada_em
            else datetime.now()
        )

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
    def sacar(self, valor): ...

    @log_transacao
    def depositar(self, valor):
        if valor > 0:
            self._saldo += float(valor)
            print("Depósito realizado com sucesso!")
            return True
        print("Valor inválido para depósito.")
        return False

    def exibir_extrato(self):
        print("\n############################ EXTRATO ###########################")
        print(
            f"Agência {self.agencia}  Conta {self.numero}  Cliente: {self.cliente.nome}"
        )
        if not self._extrato:
            print("Não foram realizadas movimentações.")
        else:
            for mov in self._extrato:
                print(mov)
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print("################################################################\n")

    # Gerador de transações (mantido)
    def gerar_transacoes(self, tipo=None):
        for transacao in self._extrato:
            if not tipo or tipo.lower() in transacao.lower():
                yield transacao


class ContaCorrente(Conta):
    @log_transacao
    def sacar(self, valor):
        hoje = date.today()
        if self._data_ultimo_saque != hoje:
            self._numero_saques = 0
            self._data_ultimo_saque = hoje

        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        if valor > LIMITE:
            print("Valor excede o limite de saque.")
            return False
        if self._numero_saques >= LIMITE_SAQUES:
            print("Limite de saques diários excedido.")
            return False
        if valor > 0:
            self._saldo -= float(valor)
            self._numero_saques += 1
            print("Saque realizado com sucesso!")
            return True
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
        if valor > 0:
            self._saldo -= float(valor)
            self._numero_saques += 1
            print("Saque realizado com sucesso!")
            return True
        print("Valor inválido.")
        return False


# ==============================
# Iterador personalizado (mantido)
# ==============================
class ContaIterador:
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
# Classe Banco (corrigida)
# ==============================
class Banco:
    CAMPOS = [
        "cpf",
        "nome",
        "estado_civil",
        "data_nascimento",
        "telefone",
        "endereco",
        "conta_numero",
        "conta_tipo",
        "saldo",
        "criada_em",
        "numero_saques",
    ]

    def __init__(self):
        self.clientes = []
        self.contas = []
        self._garantir_cabecalho_csv()
        self.carregar_dados()

    # ---------- Persistência ----------
    def _garantir_cabecalho_csv(self):
        """Cria o CSV com cabeçalho se não existir."""
        if not os.path.exists(ARQUIVO_CLIENTES):
            try:
                with open(ARQUIVO_CLIENTES, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(self.CAMPOS)
            except OSError as exc:
                print(f"[AVISO] Não foi possível criar {ARQUIVO_CLIENTES}: {exc}")

    def salvar_dados(self):
        """Salva toda a fotografia atual (clientes e contas)."""
        try:
            with open(ARQUIVO_CLIENTES, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.CAMPOS, delimiter=";")
                writer.writeheader()
                # Clientes sem conta
                for c in self.clientes:
                    if not c.contas:
                        writer.writerow(
                            {
                                "cpf": c.cpf,
                                "nome": c.nome,
                                "estado_civil": c.estado_civil,
                                "data_nascimento": c.data_nascimento,
                                "telefone": c.telefone,
                                "endereco": c.endereco,
                                "conta_numero": "",
                                "conta_tipo": "",
                                "saldo": "",
                                "criada_em": "",
                                "numero_saques": "",
                            }
                        )
                # Clientes com contas (uma linha por conta)
                for conta in self.contas:
                    writer.writerow(
                        {
                            "cpf": conta.cliente.cpf,
                            "nome": conta.cliente.nome,
                            "estado_civil": conta.cliente.estado_civil,
                            "data_nascimento": conta.cliente.data_nascimento,
                            "telefone": conta.cliente.telefone,
                            "endereco": conta.cliente.endereco,
                            "conta_numero": conta.numero,
                            "conta_tipo": conta.__class__.__name__,
                            "saldo": f"{conta.saldo:.2f}",
                            "criada_em": conta.criada_em.strftime("%Y-%m-%d %H:%M:%S"),
                            "numero_saques": conta._numero_saques,
                        }
                    )
        except OSError as exc:
            print(f"[AVISO] Não foi possível salvar {ARQUIVO_CLIENTES}: {exc}")

    def carregar_dados(self):
        """Carrega clientes e contas do CSV (se existir e tiver conteúdo)."""
        if not os.path.exists(ARQUIVO_CLIENTES):
            return
        try:
            with open(ARQUIVO_CLIENTES, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row in reader:
                    if not row.get("cpf"):
                        continue
                    # cliente (evita duplicar pelo CPF)
                    cliente = next(
                        (c for c in self.clientes if c.cpf == row["cpf"]), None
                    )
                    if not cliente:
                        cliente = Cliente(
                            row.get("nome", ""),
                            row.get("estado_civil", ""),
                            row.get("data_nascimento", ""),
                            row.get("cpf", ""),
                            row.get("telefone", ""),
                            row.get("endereco", ""),
                        )
                        self.clientes.append(cliente)
                    # conta (se existir número)
                    num = row.get("conta_numero", "")
                    if str(num).strip():
                        tipo = row.get("conta_tipo", "")
                        saldo = row.get("saldo", "0") or "0"
                        criada_em = row.get("criada_em", "")
                        ns = int(row.get("numero_saques", "0") or 0)
                        if tipo == "ContaPoupanca":
                            conta = ContaPoupanca(
                                cliente,
                                int(num),
                                saldo=saldo,
                                criada_em=criada_em,
                                numero_saques=ns,
                            )
                        else:
                            conta = ContaCorrente(
                                cliente,
                                int(num),
                                saldo=saldo,
                                criada_em=criada_em,
                                numero_saques=ns,
                            )
                        cliente.adicionar_conta(conta)
                        self.contas.append(conta)
        except OSError as exc:
            print(f"[AVISO] Não foi possível ler {ARQUIVO_CLIENTES}: {exc}")

    # ---------- Utilidades internas ----------
    def _encontrar_cliente_por_cpf(self, cpf):
        return next((c for c in self.clientes if c.cpf == cpf), None)

    def _encontrar_conta_por_numero(self, numero):
        return next((c for c in self.contas if c.numero == numero), None)

    def _proximo_numero_conta(self):
        return max((c.numero for c in self.contas), default=0) + 1

    # ---------- Opções do menu ----------
    # Opção 4
    def cadastrar_cliente(self):
        cpf = input("CPF (apenas números): ").strip()
        if not cpf:
            print("CPF inválido.")
            return
        if self._encontrar_cliente_por_cpf(cpf):
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
        self.salvar_dados()  # persiste clientes sem conta

    # Opção 5
    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ").strip()
        cliente = self._encontrar_cliente_por_cpf(cpf)
        if not cliente:
            print("Usuário não encontrado. Cadastre primeiro.")
            return

        tipo = input("Tipo da conta, [1] corrente, [2] poupanca: ").strip()
        numero = self._proximo_numero_conta()

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
        self.salvar_dados()

    # Opção 6
    def listar_clientes(self):
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
            return
        for c in self.clientes:
            print(f"\n   {c.nome_completo}")
            print(
                f" - Nasc.: {Formatador.data_nascimento(c.data_nascimento)} - CPF: {Formatador.cpf(c.cpf)}"
            )
            print(
                f" - Tel: {Formatador.telefone(c.telefone)}  Estado Civil: {c.estado_civil}"
            )
            print(f" - {Formatador.endereco(c.endereco)}\n")

    # Opção 7
    def listar_contas(self):
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        for conta in self.contas:
            print(
                f" Cliente: {conta.cliente.nome_completo}, Agência: {conta.agencia}, Conta: {conta.numero}, Tipo: {conta.__class__.__name__}"
            )

    # Opção 8
    def gerar_relatorio(self, filtro=None):
        print("\n===== RELATÓRIO DE CONTAS =====")
        if not self.contas:
            print("Nenhuma conta cadastrada.")
        for conta in self.contas:
            if not filtro or isinstance(conta, filtro):
                saques_hoje = (
                    conta._numero_saques
                    if conta._data_ultimo_saque == date.today()
                    else 0
                )
                print(f"\nCliente: {conta.cliente.nome_completo}")
                print(
                    f"Agência: {conta.agencia}  Conta: {conta.numero}  Tipo: {conta.__class__.__name__}"
                )
                print(f"Saldo: R$ {conta.saldo:.2f}")
                print(
                    f"Data de criação: {conta.criada_em.strftime('%d/%m/%Y %H:%M:%S')}"
                )
                print(f"Saques realizados hoje: {saques_hoje}")
        print("=================================\n")

    # Extra (mesma do 4.0/4.3)
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
    |                  $ BANCO PAYPY $                        |
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
            conta = banco._encontrar_conta_por_numero(numero)
            if conta:
                valor = ler_numero("Valor para depósito: ", float)
                if conta.depositar(valor):
                    banco.salvar_dados()
            else:
                print("Conta não encontrada.")

        elif opcao == "2":
            numero = ler_numero("Informe o número da conta: ", int)
            conta = banco._encontrar_conta_por_numero(numero)
            if conta:
                valor = ler_numero("Valor para saque: ", float)
                if conta.sacar(valor):
                    banco.salvar_dados()
            else:
                print("Conta não encontrada.")

        elif opcao == "3":
            numero = ler_numero("Informe o número da conta: ", int)
            conta = banco._encontrar_conta_por_numero(numero)
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
            banco.salvar_dados()
            print("Dados salvos! Obrigado por utilizar o sistema!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
