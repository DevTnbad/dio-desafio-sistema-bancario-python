import textwrap

def menu():
    menu = """\n
    ############ Menu ############
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuario
    [q] Sair
    => """
    return input(textwrap.dedent(menu))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao in ["d", "s", "e"]:
            if not contas:
                print("\n@@@ Não há contas cadastradas. Crie uma nova conta primeiro. @@@")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = selecionar_conta(numero_conta, contas)

            if not conta:
                print("\n@@@ Conta não encontrada. @@@")
                continue

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor, conta['extrato'])

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            conta['saldo'], conta['extrato'], conta['numero_saques'] = sacar(
                conta['saldo'], valor, conta['extrato'], conta['limite'], 
                conta['numero_saques'], LIMITE_SAQUES)

        elif opcao == "e":
            exibir_extrato(conta['saldo'], conta['extrato'])

        elif opcao == "nc":
            criar_conta(AGENCIA, contas, usuarios)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            sair()
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES, /):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato, /):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios, /):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios, /):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, contas, usuarios, /):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        numero_conta = len(contas) + 1
        contas.append({
            "agencia": agencia, 
            "numero_conta": numero_conta, 
            "usuario": usuario, 
            "saldo": 0, 
            "extrato": "", 
            "limite": 500, 
            "numero_saques": 0
        })
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado, crie um usuário primeiro! @@@")

def listar_contas(contas, /):
    if contas:
        print("\n================ LISTA DE CONTAS ================")
        for conta in contas:
            linha = f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}"
            print(linha)
        print("=================================================")
    else:
        print("\n@@@ Não há contas cadastradas. @@@")

def selecionar_conta(numero_conta, contas, /):
    for conta in contas:
        if conta["numero_conta"] == numero_conta:
            print("\n=== Conta selecionada com sucesso! ===")
            return conta
    return None

def sair():
    print("Obrigado por usar nosso sistema bancário! Até a próxima.")

main()