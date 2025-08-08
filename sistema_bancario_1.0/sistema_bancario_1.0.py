## Sistema Bancário ##

usuario = input("digite seu nome: ")
print(f"Bem vindo ao Banco PAYPY {usuario}!")

# Menu #
menu = f"""
$$$$$$$$$$$$$$$$  BANCO PAYPY  $$$$$$$$$$$$$$$
##########           MENU           ##########
#                                            #
#     [1] DEPOSITAR                          #
#     [2] SACAR                              #
#     [3] EXTRATO                            #
#     [0] SAIR                               #
#                                            #
##############################################
=> """

#print(menu)

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# Extrato
menu_extrato = f"""
$$$$$$$$$$$$$$$$  BANCO PAYPY  $$$$$$$$$$$$$$$
################## EXTRATO ###################
"""

# Agradecimento
agradece = f"""
$$$$$$$$$$$$$$$$  BANCO PAYPY  $$$$$$$$$$$$$$$
##############################################
#    Obrigado por utilizar nosso sistema!    #
##############################################
"""

## Mensagens ##
excedeu_l = "Operação falhou, o valor do saque excede o limite."
excedeu_s = "Operação falhou! Número máximo de saques excedido."
insuficiente = "Não foi possivel realizar esta operação devido a saldo insuficiente."
invalido = "Operação falhou, o valor informado é invalido"
sucesso_d = "Deposito efetuado com sucesso!"
sucesso_s = "Saque efetuado com sucesso!"

# Inicio
while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(sucesso_d)
        else:
            print(invalido)

    elif opcao == "2":
        valor = float(input("Digite o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print(insuficiente)
        
        elif excedeu_limite:
            print(excedeu_l)

        elif excedeu_saques:
            print(excedeu_s)

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(sucesso_s)

        else:
            print(invalido)

    elif opcao == "3":
        print(menu_extrato)
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo atual: R$ {saldo:.2f}")
        print("\n##############################################\n")


    elif opcao == "0":
        print(agradece)
        break

    else:
        print(invalido)


