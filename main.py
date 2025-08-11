import json
import os

from cliente import Cliente
from pedido import Pedido
from produto import Produto

produtos: list[Produto] = []
clientes: list[Cliente] = []
pedidos:  list[Pedido]  = []

def run():

    """Recuperar informações e corrigir contadores"""
    global produtos, clientes, pedidos
    produtos = [Produto.carregar_dados(p) for p in ler_dados("produtos")]
    Produto._contador = max((p.codigo for p in produtos), default=0)

    clientes = [Cliente.carregar_dados(c) for c in ler_dados("clientes")]
    Cliente._contador = max((p.codigo for p in clientes), default=0)

    pedidos = [Pedido.carregar_dados(p) for p in ler_dados("pedidos")]
    Pedido._contador = max((p.codigo for p in pedidos), default=0)

    opcao = ""
    while opcao != 'x':
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Pedidos")
        print("2 - Clientes")
        print("3 - Cardápio (Produtos)")
        print("x - Sair")

        """Opções do menu principal"""
        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                menu_pedidos()
            case "2":
                menu_clientes()
            case "3":
                menu_produtos()
            case _:
                print("Opção inválida! Tente novamente.")

    print("Encerrando o programa...")

"""Lista o menu de opçoes do pedido"""
def menu_pedidos():
    opcao = ""
    while opcao != 'x':
        print("\n--- MENU PEDIDOS ---")
        print("1 - Cadastrar pedido")
        print("2 - Listar pedidos")
        print("x - Voltar")

        opcao = input("Escolha: ")
        match opcao:
            case "1":
                cadastrar_pedido()
            case "2":
                for ped in pedidos:
                    print(f"Pedido código {ped.codigo} | Cliente telefone: {ped.cliente_telefone} | Produtos: {ped.itens} | Data: {ped.data_criacao} | Status: {ped.status}")

                """Finaliza pedido"""
                opcao_pedido = input("Deseja finalizar algum pedido? [S/N]: ")
                if opcao_pedido.upper() == "S":
                    codigo_pedido = int(input("Digite o código do pedido: "))
                    pedido = next(ped for ped in pedidos if ped.codigo == codigo_pedido)
                    pedido.finalizar()

                    """Monta dicionário e salva o registro no arquivo"""
                    dicionario = [p.obter_dicionario() for p in pedidos]
                    salvar_dados(dicionario, "pedidos")
            case _:
                print("Opção inválida.")

"""Lista o menu de opçoes do cliente"""
def menu_clientes():
    opcao = ""

    while opcao != 'x':
        print("\n--- MENU CLIENTES ---")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Remover cliente")
        print("x - Voltar")

        opcao = input("Escolha: ")

        match opcao:
            case "1":
                cadastrar_cliente()
            case "2":
                for c in clientes:
                    print(f"Código: {c.codigo} | Telefone: {c.telefone} | Nome: {c.nome} | Sobrenome: {c.sobrenome}")
            case "3":
                remover_cliente()
            case _:
                print("Opção inválida.")

"""Lista o menu de opçoes do produto"""
def menu_produtos():
    opcao = ""

    while opcao != 'x':
        print("\n--- MENU PRODUTOS ---")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Remover produto")
        print("x - Voltar")

        opcao = input("Escolha: ")

        match opcao:
            case "1":
                cadastrar_produto()
            case "2":
                for p in produtos:
                    print(f"Código: {p.codigo} | Nome: {p.nome} | Preço: {p.preco:.2f}")
            case "3":
                remover_produto()
            case "0":
                break
            case _:
                print("Opção inválida.")

def cadastrar_pedido():
    """Valida se existe produtos cadastrados"""
    if not produtos:
        print("Nenhum produto cadastrado!")
        return

    telefone = str(input("Telefone do cliente: "))

    """Busca cliente por telefone"""
    cliente = next((c for c in clientes if c.telefone == telefone), None)

    """Valida de o cliente existe"""
    if not cliente:
        print("Para fazer o pedido, cadastre as informações do cliente: ")
        cliente = cadastrar_cliente()

    """Adiciona itens do pedido"""
    itens = []
    while True:
        limpar_console()
        print(f"\n#Pedido para {cliente.nome} {cliente.sobrenome}")
        print("--- CARDAPIO ---")
        for p in produtos:
            print(f"Código: {p.codigo} | Nome: {p.nome} | Preço: {p.preco:.2f}")

        print("----------------")
        print(f"Itens adicionados: {str(itens)}")
        item_codigo = int(input("Código do produto (0 para finalizar): "))
        if item_codigo == 0:
            break
        itens.append(item_codigo)

    """Adicionar pedido na lista"""
    pedido = Pedido(itens, cliente.telefone)
    pedidos.append(pedido)

    """Monta dicionário e salva o registro no arquivo"""
    dicionario = [p.obter_dicionario() for p in pedidos]
    salvar_dados(dicionario, "pedidos")

    print(f"Pedido {pedido.codigo} criado!")

def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    sobrenome = input("Sobrenome do cliente: ")
    telefone = input("Telefone do cliente: ")
    cliente = next((c for c in clientes if c.telefone == telefone), None)

    if cliente:
        print(f"Já existe um cliente com o número {telefone}")
        return

    """Adiciona o cliente na lista"""
    cliente = Cliente(nome, sobrenome, telefone)
    clientes.append(cliente)

    """Monta dicionário e salva o registro no arquivo"""
    dicionario = [c.obter_dicionario() for c in clientes]
    salvar_dados(dicionario, "clientes")

    print("Cliente cadastrado!")

    return cliente

def cadastrar_produto():
    """Imputar os dados do produto"""
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    preco = float(input("Preço: "))

    """Adiciona o protudo na lista"""
    produto = Produto(nome, descricao, preco)
    produtos.append(produto)

    """Monta dicionário e salva o registro no arquivo"""
    dicionario = [p.obter_dicionario() for p in produtos]
    salvar_dados(dicionario, "produtos")
    print(f"Produto {produto.nome} cadastrado com Código {produto.codigo}!")

def remover_cliente():
    limpar_console()
    print("--- CLIENTES ---")
    for c in clientes:
        print(f"Telefone: {c.telefone} | Nome: {c.nome} | Sobrenome: {c.sobrenome}")

    print("----------------")
    telefone = str(input("Insira telefone do cliente para remover: "))
    try:
        cliente = next((c for c in clientes if c.telefone == telefone), None)
        if cliente:
            clientes.remove(cliente)

            """Monta dicionário e salva o registro no arquivo"""
            dicionario = [c.obter_dicionario() for c in clientes]
            salvar_dados(dicionario, "clientes")
            print(f"Cliente {cliente.nome} removido com sucesso!")
        else:
            print("Cliente não encontrado.")
    except ValueError:
        print("ID inválido!")

def remover_produto():
    limpar_console()
    print("--- CARDAPIO ---")
    for p in produtos:
        print(f"Código: {p.codigo} | Nome: {p.nome} | Preço: {p.preco:.2f}")

    print("----------------")
    item_codigo = int(input("Insira o código do produto para remover: "))
    try:
        produto = next((p for p in produtos if p.codigo == item_codigo), None)
        if produto:
            produtos.remove(produto)

            """Monta dicionário e salva o registro no arquivo"""
            dicionario = [p.obter_dicionario() for p in produtos]
            salvar_dados(dicionario, "produtos")
            print(f"Produto {produto.nome} removido com sucesso!")
        else:
            print("Produto não encontrado.")
    except ValueError:
        print("ID inválido!")

"""Salvar dados no arquivo"""
def salvar_dados(dicionario, nome_arquivo):
    os.makedirs("arquivos_dados", exist_ok=True)
    with open('arquivos_dados/' + nome_arquivo + '.json', "w") as f:
        json.dump(dicionario, f)
        f.close()

"""Ler dados do arquivo"""
def ler_dados(nome_arquivo: str) -> list:
    try:
        with open('arquivos_dados/' + nome_arquivo + '.json', "r", encoding="utf-8") as f:
            dados = json.load(f)
            f.close()
            return dados
    except FileNotFoundError:
        return []

def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    run()
