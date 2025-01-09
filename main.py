import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import uuid
import json


# Nome do arquivo para salvar os dados
ARQUIVO_JSON = "inventario.json"

# Função para carregar os dados do json
def carregar_inventario():
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []  # arquivo não existindo, retorna uma lista vazia
    except json.JSONDecodeError:
        print("Erro ao carregar o arquivo JSON. Inicializando inventário vazio.")
        return []

# Função para salvar os dados no json
def salvar_inventario():
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(inventario, arquivo, indent=4)

# Lista para puxar todos os produtos
inventario = carregar_inventario()


# Funcionalidades


# Função para adicionar um produto
def adicionar_produto(Nome, Categoria, Quantidade, Preco):
    try:
        Quantidade = int(Quantidade)
        Preco = float(Preco)
    except ValueError:
        return False, "Quantidade deve ser um número inteiro e preço deve ser um número decimal."

    produto_id = str(uuid.uuid4())[:7]
    produto = {
        "ID": produto_id,
        "Nome": Nome,
        "Categoria": Categoria,
        "Quantidade": Quantidade,
        "Preco": Preco,
    }
    inventario.append(produto)
    salvar_inventario()
    return True, "Produto adicionado com sucess!"

# Função para listar produtos
def listar_produtos():
    if not inventario:
        return []
    return inventario  # Retorna a lista de produtos

# Função para excluir um produto
def excluir_produto(produto_id):
    produto = next((p for p in inventario if p["ID"] == produto_id), None)
    if produto:
        inventario.remove(produto)
        salvar_inventario()
        return True, f"Produto {produto['Nome']} excluído com sucess!"
    return False, "Produto não encontrado."

# Função para atualizar um produto
def atualizar_produto(produto_id, Nome=None, Categoria=None, Quantidade=None, Preco=None):
    produto = next((p for p in inventario if p["ID"] == produto_id), None)
    if produto:
        if Nome: produto["Nome"] = Nome
        if Categoria: produto["Categoria"] = Categoria
        if Quantidade: produto["Quantidade"] = int(Quantidade)
        if Preco: produto["Preco"] = float(Preco)
        salvar_inventario()
        return True, "Produto atualizado com sucess!"
    return False, "Produto não encontrado."

# iniciar o inventário 
inventario = carregar_inventario()

# Classe principal
class data_table:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Estoque")
        self.root.geometry("1000x800")
        self.headers = ["ID", "Nome", "Categoria", "Preço", "Quantidade"]
        self.inventory = listar_produtos()
        self.create_widgets()

    def create_widgets(self):
        top_button_frame = tb.Frame(self.root)
        top_button_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.search_var = tk.StringVar()
        pesquisa_label = tb.Label(top_button_frame, text="Buscar por ID:")
        pesquisa_label.pack(padx=2, pady=2, side="left")
        search_entry = tb.Entry(top_button_frame, textvariable=self.search_var, width=40, bootstyle="secondary")
        search_entry.pack(side="left", padx=10)
        search_btn = tb.Button(top_button_frame, text="Buscar", command=self.buscar_data, bootstyle="info")
        search_btn.pack(side="left", padx=10)

        filter_btn = tb.Button(top_button_frame, text="Filtrar", command=self.abrir_filtro, bootstyle="warning")
        filter_btn.pack(side="right", padx=10)

        frame_table = tb.Frame(self.root)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = tb.Treeview(frame_table, columns=self.headers, show="headings", selectmode="browse", bootstyle="dark")
        self.tree.pack(fill="both", expand=True)

        for header in self.headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, anchor="center")

        self.preencher_tabela(self.inventory)

        bottom_button_frame = tb.Frame(self.root)
        bottom_button_frame.pack(fill="x", padx=10, pady=10)

        btn_add = tb.Button(bottom_button_frame, text="Adicionar", command=self.adicionar_data, bootstyle="success")
        btn_add.pack(side="left", padx=5)

        btn_apagar = tb.Button(bottom_button_frame, text="Excluir", command=self.apagar_produto, bootstyle="danger")
        btn_apagar.pack(side="left", padx=5)

        btn_atualizar = tb.Button(bottom_button_frame, text="Atualizar", command=self.atualizar_tabelaa, bootstyle="info")
        btn_atualizar.pack(side="right", padx=5)

        btn_editar = tb.Button(bottom_button_frame, text="Editar", command=self.editar, bootstyle="warning")
        btn_editar.pack(side="left", padx=5)

    def abrir_filtro(self):
        filtro_window = tk.Toplevel(self.root)
        filtro_window.title("Filtrar Produtos")
        filtro_window.geometry("500x300")

        categoria_label = tb.Label(filtro_window, text="Filtrar por Categoria:")
        categoria_label.pack(padx=10, pady=5)
        categoria_var = tk.StringVar()
        categoria_entry = tb.Entry(filtro_window, textvariable=categoria_var)
        categoria_entry.pack(padx=10, pady=5)

        ordenacao_label = tb.Label(filtro_window, text="Ordenar por:")
        ordenacao_label.pack(padx=10, pady=5)
        ordenacao_var = tk.StringVar(value="Nome")
        ordenacao_menu = tb.Combobox(
            filtro_window,
            textvariable=ordenacao_var,
            values=["Nome", "Quantidade", "Preço"],
            state="readonly"
        )
        ordenacao_menu.pack(padx=10, pady=5)

        def aplicar_filtros():
            categoria = categoria_var.get()
            ordenacao = ordenacao_var.get().lower()

            filtrados = [
                produto for produto in self.inventory
                if not categoria or produto["Categoria"].lower() == categoria.lower()
            ]

            if ordenacao == "quantidade":
                filtrados.sort(key=lambda p: p["Quantidade"])
            elif ordenacao == "preço":
                filtrados.sort(key=lambda p: p["Preco"])
            else:  # Nome é ordenacao padrão
                filtrados.sort(key=lambda p: p["Nome"].lower())

            self.preencher_tabela(filtrados)
            filtro_window.destroy()

        aplicar_btn = tb.Button(filtro_window, text="Aplicar", command=aplicar_filtros, bootstyle="success")
        aplicar_btn.pack(padx=10, pady=10)

        cancelar_btn = tb.Button(filtro_window, text="Cancelar", command=filtro_window.destroy, bootstyle="danger")
        cancelar_btn.pack(padx=10, pady=5)

    def preencher_tabela(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not data:
            self.tree.insert("", "end", values=["", "Sem produtos", "", "", ""])
        else:
            for produto in data:
                values = [produto["ID"], produto["Nome"], produto["Categoria"],
                          produto["Quantidade"], f"R$: {produto['Preco']:.2f}"]
                self.tree.insert("", "end", values=values)

    def buscar_data(self):
        query = self.search_var.get().lower()
        filtred_data = [
            row for row in self.inventory if query in row["ID"].lower()
        ]
        self.preencher_tabela(filtred_data)

    def adicionar_data(self):
        # Criação de uma nova janela para adicionar um produto
        add_window = tk.Toplevel(self.root)
        add_window.geometry("600x400")
        add_window.title("Adicionar Produto")

        # Campos de nome, categoria, quantidade e preço
        nome_label = tb.Label(add_window, text="Nome do Produto")
        nome_label.pack(padx=10, pady=5)
        nome_entry = tb.Entry(add_window)
        nome_entry.pack(padx=10, pady=5)

        categoria_label = tb.Label(add_window, text="Categoria")
        categoria_label.pack(padx=10, pady=5)
        categoria_entry = tb.Entry(add_window)
        categoria_entry.pack(padx=10, pady=5)

        quantidade_label = tb.Label(add_window, text="Quantidade")
        quantidade_label.pack(padx=10, pady=5)
        quantidade_entry = tb.Entry(add_window)
        quantidade_entry.pack(padx=10, pady=5)

        preco_label = tb.Label(add_window, text="Preço")
        preco_label.pack(padx=10, pady=5)
        preco_entry = tb.Entry(add_window)
        preco_entry.pack(padx=10, pady=5)

        # Função para salvar o produto
        def salvar_produto():
            Nome = nome_entry.get()
            Categoria = categoria_entry.get()
            Quantidade = quantidade_entry.get()
            Preco = preco_entry.get()

            # adiciona o produto
            sucess, mensagem = adicionar_produto(Nome, Categoria, Quantidade, Preco)
            messagebox.showinfo("Resultado", mensagem)

            if sucess:
                self.preencher_tabela(listar_produtos())  # Atualiza a tabela
            add_window.destroy()  # Fecha a janela de adicionar produto

        # Botão para salvar o produto
        botao_salvar = tb.Button(add_window, text="Salvar", command=salvar_produto, bootstyle="success" )
        botao_salvar.pack(padx=10, pady=10)

        # Botão para fechar a janela
        botao_cancelar = tb.Button(add_window, text="Cancelar", command=add_window.destroy,  bootstyle="danger")
        botao_cancelar.pack(padx=10, pady=5)

    # Função para excluir um produto
    def apagar_produto(self):
        item_selecionado = self.tree.focus()
        if not item_selecionado:  # Se nenhum item for selecionado
            # Abre uma janela para digitar o ID do produto a ser excluído
            excluir_window = tk.Toplevel(self.root)
            excluir_window.geometry("400x200")
            excluir_window.title("Excluir Produto")

            label_id = tb.Label(excluir_window, text="Digite o ID do Produto:")
            label_id.pack(padx=10, pady=10)
            id_entry = tb.Entry(excluir_window)
            id_entry.pack(padx=10, pady=5)

            # FALTA POR CASO NAO ENCONTRE O ID

            def excluir_por_id():
                produto_id = id_entry.get()
                sucess, mensagem = excluir_produto(produto_id)  # Aqui chama a função de exclusão
                messagebox.showinfo("Resultado", mensagem)
                if sucess:
                    self.preencher_tabela(listar_produtos())  # Atualizo a tabela
                excluir_window.destroy()  # Fecho a janela de excluir

            botao_excluir = tb.Button(excluir_window, text="Excluir", command=excluir_por_id, bootstyle="danger")
            botao_excluir.pack(pady=10)

            botao_cancelar = tb.Button(excluir_window, text="Cancelar", command=excluir_window.destroy, bootstyle="secondary")
            botao_cancelar.pack(pady=5)
            return

        # Caso algum item seja selecionado exclusão segue normalmente
        values = self.tree.item(item_selecionado, "values")
        product_id = values[0]
        sucess, mensagem = excluir_produto(product_id)
        messagebox.showinfo("Resultado", mensagem)
        if sucess:
            self.preencher_tabela(listar_produtos())

    def atualizar_tabelaa(self):
        self.preencher_tabela(listar_produtos())

    # Função para editar um produto
    def editar(self):
        item_selecionado = self.tree.focus()
        if not item_selecionado:  # Se nenhum item for selecionado
            # Abre uma janela para digitar o ID do produto a ser editado
            editar_window = tk.Toplevel(self.root)
            editar_window.geometry("600x300")
            editar_window.title("Editar Produto")

            label_id = tb.Label(editar_window, text="Digite o ID do Produto:")
            label_id.pack(padx=10, pady=10)
            id_entry = tb.Entry(editar_window)
            id_entry.pack(padx=10, pady=5)

            def editar_por_id():
                produto_id = id_entry.get()
                produto = next((p for p in self.inventory if p["ID"] == produto_id), None)
                if produto:
                    # Se o id bater com um existente chamo a janela para editar
                    self.editar_produto(produto_id)  # Chama a função de edição padrão
                    editar_window.destroy()  # Fecha a janela de digitação do ID
                else:
                    messagebox.showwarning("Aviso", "ID não encontrado!")

            botao_editar = tb.Button(editar_window, text="Editar", command=editar_por_id, bootstyle="warning")
            botao_editar.pack(pady=10)

            botao_cancelar = tb.Button(editar_window, text="Cancelar", command=editar_window.destroy, bootstyle="secondary")
            botao_cancelar.pack(pady=5)
            return

        # Caso algum item esteja selecionado a edição segue normalmente
        values = self.tree.item(item_selecionado, "values")
        product_id = values[0]
        self.editar_produto(product_id)

    # Função de edição por ID
    def editar_produto(self, produto_id):
        produto = next((p for p in self.inventory if p["ID"] == produto_id), None)
        if produto:
            edit_window = tk.Toplevel(self.root)
            edit_window.geometry("600x400")
            edit_window.title(f"Editar Produto {produto_id}")

            nome_label = tb.Label(edit_window, text="Nome do Produto")
            nome_label.pack(padx=10, pady=5)
            nome_entry = tb.Entry(edit_window)
            nome_entry.insert(0, produto["Nome"])
            nome_entry.pack(padx=10, pady=5)

            categoria_label = tb.Label(edit_window, text="Categoria")
            categoria_label.pack(padx=10, pady=5)
            categoria_entry = tb.Entry(edit_window)
            categoria_entry.insert(0, produto["Categoria"])
            categoria_entry.pack(padx=10, pady=5)

            quantidade_label = tb.Label(edit_window, text="Quantidade")
            quantidade_label.pack(padx=10, pady=5)
            quantidade_entry = tb.Entry(edit_window)
            quantidade_entry.insert(0, produto["Quantidade"])
            quantidade_entry.pack(padx=10, pady=5)

            preco_label = tb.Label(edit_window, text="Preço")
            preco_label.pack(padx=10, pady=5)
            preco_entry = tb.Entry(edit_window)
            preco_entry.insert(0, produto["Preco"])
            preco_entry.pack(padx=10, pady=5)

            def salvar_mudancas():
                novo_nome = nome_entry.get()
                nova_categoria = categoria_entry.get()
                nova_quantidade = quantidade_entry.get()
                novo_preco = preco_entry.get()
                sucess, mensagem = atualizar_produto(produto_id, novo_nome, nova_categoria, nova_quantidade, novo_preco)
                messagebox.showinfo("Resultado", mensagem)
                if sucess:
                    self.preencher_tabela(listar_produtos())
                edit_window.destroy()
                
            def fechar():
                edit_window.destroy()

            botao_salvar = tb.Button(edit_window, text="Salvar", command=salvar_mudancas, bootstyle="success")
            botao_salvar.pack(padx=10, pady=10)
            
            botao_cancelar = tb.Button(edit_window, text="Cancelar", command=fechar, bootstyle="danger")
            botao_cancelar.pack(padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()

    # Defino o tema desejado para a janela inteira
    style = tb.Style()
    style.theme_use("superhero")
    
    app = data_table(root)
    root.mainloop()