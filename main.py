""" Modulos gerando id randomico e modulo json para trabalhar com o arquivos json"""
import uuid
import json

# Nome do arquivo para salvar os dados
ARQUIVO_JSON = "inventario.json"


# Função para carregar os dados do json criado
def carregar_inventario():
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []  # arquivo não tiver existindo, retorna uma lista vazia
    except json.JSONDecodeError:
        print("Arquivo JSON não encontrado!. Inicializando inventário vazio.")
        return []


# Função para ficar salvando os dados no json
def salvar_inventario():
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(inventario, arquivo, indent=4)


# Lista para armazenar os produtos
inventario = carregar_inventario()


# Função para adicionar um produto
def adicionar_produto():
    print("\n--- Adicionar Produto ---")
    # Solicitando as informações do produto
    nome = input("Nome do Produto: ").strip()
    categoria = input("Categoria: ").strip()

    # Validação para quantidade e preço
    try:
        quantidade = int(input("Quantidade em Estoque: ").strip())
        preco = float(input("Preço (R$): ").strip())
    except ValueError:
        print("Erro: Quantidade deve ser um número inteiro e Preço deve ser um número decimal.")
        return

    # Gera um ID único de 7 caracteres
    produto_id = str(uuid.uuid4())[:7]
    # Criando um dicionário para o produto
    produto = {
        "id": produto_id,
        "nome": nome,
        "categoria": categoria,
        "quantidade": quantidade,
        "preco": preco
    }
    # dando append para adicionar o produto ao inventário
    inventario.append(produto)
    salvar_inventario()  # Salvando no arquivo json
    print("Produto adicionado com sucesso!")


# Função para listar os produtos
def listar_produtos():
    print("\n--- Listar Produtos ---") 
    if not inventario: # Se não houver inventário retornar que está vazio
        print("Nenhum produto cadastrado no inventário.")
        return

    # Exibindo cabeçalho da tabela
    print(f"{'ID':<36} {'Nome':<20} {'Categoria':<15} {'Quantidade':<10} {'Preço (R$)':<10}")
    print("-" * 90)

    # Exibindo os produtos cadastrados
    for produto in inventario:
        print(f"{produto['id']:<36} {produto['nome']:<20} {produto['categoria']:<15} {produto['quantidade']:<10} {produto['preco']:<10.2f}")


# Atualizar informações de um produto existente pelo ID dele
def atualizar_produto():
    listar_produtos()
    produto_id = input("\nInforme o ID do produto que deseja atualizar: ").strip()
    produto = next((p for p in inventario if p["id"] == produto_id), None)

    if not produto:
        print("Produto não encontrado.")
        return

    print("\nQuais campos deseja atualizar?")
    print("1. Nome")
    print("2. Categoria")
    print("3. Quantidade")
    print("4. Preço")
    campos = input("Informe os números separados por vírgulas (ex: 1,2): ").split(",")

    for campo in map(str.strip, campos):
        if campo == "1":
            novo_nome = input("Novo Nome: ").strip()
            produto["nome"] = novo_nome
        elif campo == "2":
            nova_categoria = input("Nova Categoria: ").strip()
            produto["categoria"] = nova_categoria
        elif campo == "3":
            nova_quantidade = int(input("Nova Quantidade: ").strip())
            produto["quantidade"] = nova_quantidade
        elif campo == "4":
            novo_preco = float(input("Novo Preço (R$): ").strip())
            produto["preco"] = novo_preco
        else:
            print(f"Campo inválido: {campo}")

    salvar_inventario()
    print("Produto atualizado com sucesso!")


# Excluir produto do inventário pelo ID
def excluir_produto():
    listar_produtos()
    produto_id = input("\nInforme o ID do produto que deseja excluir: ").strip() # Recebo o ID que quer excluir
    produto = next((p for p in inventario if p["id"] == produto_id), None) # Mapeio procurando pelo produto que possui ID igual

    if not produto: # Caso o id não seja encontrado
        print("Produto não encontrado.")
        return

    confirmacao = input(f"Tem certeza que deseja excluir o produto '{produto['nome']}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        inventario.remove(produto)
        salvar_inventario()
        print("Produto excluído com sucesso!")
    else:
        print("Exclusão cancelada.")


# Menu principal
def menu():
    while True:
        print("\n1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Produto")
        print("4. Excluir Produto")
        print("5. Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            adicionar_produto()
        elif escolha == "2":
            listar_produtos()
        elif escolha == "3":
            atualizar_produto()
        elif escolha == "4":
            excluir_produto()
        elif escolha == "5":
            salvar_inventario()
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida.")


# Executando o programa
if __name__ == "__main__":
    menu()
