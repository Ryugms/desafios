## Sistema Bancário v2.0 ##
import datetime
import textwrap

# Constantes
LIMITE_SAQUES = 3
LIMITE = 500
AGENCIA = "0001"

# Estruturas de dados
usuarios = []
contas = []

# Funções

def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_telefone(telefone):
    return f"(55)({telefone[:2]}){telefone[2:6]}-{telefone[6:]}"

def cadastrar_usuario():
    cpf = input("CPF (apenas números): ").strip()
    if any(u['cpf'] == cpf for u in usuarios):
        print("Usuário já cadastrado com este CPF.")
        return

    nome = input("Nome: ").strip()
    sobrenome = input("Sobrenome: ").strip()
    data_nascimento = input("Data de Nascimento: ").strip() 
    telefone = input("Telefone (DDD + número): ").strip()
    endereco = input("Endereço (logradouro, nº - bairro - cidade - estado): ").strip()

    usuarios.append({
        "nome": nome,
        "sobrenome": sobrenome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "telefone": telefone,
        "endereco": endereco
    })
    print("Usuário cadastrado com sucesso!")

def listar_usuarios():
    for u in usuarios:
        print(f"   {u['nome']} {u['sobrenome']} \n - Data de Nasc.: {u['data_nascimento']} - CPF: {formatar_cpf(u['cpf'])} \n - Tel: {formatar_telefone(u['telefone'])} \n - {u['endereco']}")

def criar_conta():
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)

    if not usuario:
        print("Usuário não encontrado. Cadastre primeiro.")
        return

    tipo = input("Tipo da conta (corrente/poupanca): ").strip().lower()
    if tipo not in ["corrente", "poupanca"]:
        print("Tipo inválido.")
        return

    numero = len(contas) + 1
    contas.append({
        "agencia": AGENCIA,
        "numero": numero,
        "usuario": usuario,
        "tipo": tipo,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0
    })
    print(f"Conta criada com sucesso! Agência: {AGENCIA} Conta: {numero}")

def listar_contas():
    for c in contas:
        usuario = c['usuario']
        print(f"Agência: {c['agencia']}, Conta: {c['numero']}, Tipo: {c['tipo']}, Cliente: {usuario['nome']} {usuario['sobrenome']}")

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Valor inválido para depósito.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Saldo insuficiente.")
    elif valor > limite:
        print("Valor excede o limite de saque.")
    elif numero_saques >= limite_saques:
        print("Limite de saques diários excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Valor inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    data = datetime.datetime.now().strftime("%d/%m/%y")
    print("\n####################### EXTRATO ######################")
    print(f"Data: {data}")
    print(extrato if extrato else "Nenhuma movimentação realizada.")
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("######################################################\n")

# Menu interativo
menu_texto = """
===========================================================
|		      $ BANCO PAYPY $			  |
|							  |
=========================== MENU ==========================
		[1] Depositar
		[2] Sacar
		[3] Extrato
		[4] Novo Usuário
		[5] Nova Conta
		[6] Listar Usuários
		[7] Listar Contas
		[0] Sair
===========================================================
=> """

while True:
    opcao = input(textwrap.dedent(menu_texto))

    if opcao == "1":
        numero = int(input("Informe o número da conta: "))
        conta = next((c for c in contas if c['numero'] == numero), None)
        if conta:
            valor = float(input("Valor para depósito: "))
            conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor, conta['extrato'])
        else:
            print("Conta não encontrada.")

    elif opcao == "2":
        numero = int(input("Informe o número da conta: "))
        conta = next((c for c in contas if c['numero'] == numero), None)
        if conta:
            valor = float(input("Valor para saque: "))
            conta['saldo'], conta['extrato'], conta['numero_saques'] = sacar(
                saldo=conta['saldo'], valor=valor, extrato=conta['extrato'],
                limite=LIMITE, numero_saques=conta['numero_saques'], limite_saques=LIMITE_SAQUES)
        else:
            print("Conta não encontrada.")

    elif opcao == "3":
        numero = int(input("Informe o número da conta: "))
        conta = next((c for c in contas if c['numero'] == numero), None)
        if conta:
            exibir_extrato(conta['saldo'], extrato=conta['extrato'])
        else:
            print("Conta não encontrada.")

    elif opcao == "4":
        cadastrar_usuario()

    elif opcao == "5":
        criar_conta()

    elif opcao == "6":
        listar_usuarios()

    elif opcao == "7":
        listar_contas()

    elif opcao == "0":
        print("Obrigado por utilizar nosso sistema!")
        break

    else:
        print("Opção inválida.")
