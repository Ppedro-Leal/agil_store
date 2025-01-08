import tkinter as tk
from tkinter import ttk, messagebox
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

# Lista para armazenar os produtos
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
    return inventario  # Retorna a lista de dicionários

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

# Carregar inventário inicial
inventario = carregar_inventario()

class data_table:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Estoque")
        self.root.geometry("1000x800")
        self.headers = ["ID", "Nome", "Categoria", "Preo", "Quantidade"]
        self.inventory = listar_produtos()
        self.create_widgets()

    def create_widgets(self):
        top_button_frame = ttk.Frame(self.root)
        top_button_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_button_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=10)
        search_btn = ttk.Button(top_button_frame, text="Buscar", command=self.buscar_data)
        search_btn.pack(side="right", padx=10)

        frame_table = ttk.Frame(self.root)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_table, columns=self.headers, show="headings", selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        for header in self.headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, anchor="center")

        self.preencher_tabela(self.inventory)

        bottom_button_frame = ttk.Frame(self.root)
        bottom_button_frame.pack(fill="x", padx=10, pady=10)

        btn_add = ttk.Button(bottom_button_frame, text="Adicionar", command=self.adicionar_data)
        btn_add.pack(side="left", padx=5)

        btn_apagar = ttk.Button(bottom_button_frame, text="Excluir", command=self.apagar_produto)
        btn_apagar.pack(side="left", padx=5)

        btn_atualizar = ttk.Button(bottom_button_frame, text="Atualizar", command=self.atualizar_tabelaa)
        btn_atualizar.pack(side="left", padx=5)

        btn_editar = ttk.Button(bottom_button_frame, text="Editar", command=self.editar_produto)
        btn_editar.pack(side="left", padx=5)

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
        add_window.title("Adicionar Produto")

        # Campos para o nome, categoria, quantidade e preço
        nome_label = ttk.Label(add_window, text="Nome do Produto")
        nome_label.pack(padx=10, pady=5)
        nome_entry = ttk.Entry(add_window)
        nome_entry.pack(padx=10, pady=5)

        categoria_label = ttk.Label(add_window, text="Categoria")
        categoria_label.pack(padx=10, pady=5)
        categoria_entry = ttk.Entry(add_window)
        categoria_entry.pack(padx=10, pady=5)

        quantidade_label = ttk.Label(add_window, text="Quantidade")
        quantidade_label.pack(padx=10, pady=5)
        quantidade_entry = ttk.Entry(add_window)
        quantidade_entry.pack(padx=10, pady=5)

        preco_label = ttk.Label(add_window, text="Preco")
        preco_label.pack(padx=10, pady=5)
        preco_entry = ttk.Entry(add_window)
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
        botao_salvar = ttk.Button(add_window, text="Salvar", command=salvar_produto)
        botao_salvar.pack(padx=10, pady=10)

        # Botão para fechar a janela
        botao_cancelar = ttk.Button(add_window, text="Cancelar", command=add_window.destroy)
        botao_cancelar.pack(padx=10, pady=5)

    def apagar_produto(self):
        item_selecionado = self.tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            return

        values = self.tree.item(item_selecionado, "values")
        product_id = values[0]
        sucess, mensagem = excluir_produto(product_id)
        messagebox.showinfo("Resultado", mensagem)
        if sucess:
            self.preencher_tabela(listar_produtos())

    def atualizar_tabelaa(self):
        self.preencher_tabela(listar_produtos())

    def editar_produto(self):
        item_selecionado = self.tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para editar.")
            return

        values = self.tree.item(item_selecionado, "values")
        product_id = values[0]

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Editar Produto {product_id}")

        nome_entry = ttk.Entry(edit_window)
        nome_entry.insert(0, values[1])
        nome_entry.pack(padx=10, pady=5)

        categoria_entry = ttk.Entry(edit_window)
        categoria_entry.insert(0, values[2])
        categoria_entry.pack(padx=10, pady=5)

        quantidade_entry = ttk.Entry(edit_window)
        quantidade_entry.insert(0, values[3])
        quantidade_entry.pack(padx=10, pady=5)

        preco_entry = ttk.Entry(edit_window)
        preco_entry.insert(0, values[4])
        preco_entry.pack(padx=10, pady=5)

        def salvar_mudancas():
            novo_nome = nome_entry.get()
            nova_categoria = categoria_entry.get()
            nova_quantidade = quantidade_entry.get()
            novo_preco = preco_entry.get()
            sucess, mensagem = atualizar_produto(product_id, novo_nome, nova_categoria, nova_quantidade, novo_preco)
            messagebox.showinfo("Resultado", mensagem)
            if sucess:
                self.preencher_tabela(listar_produtos())
            edit_window.destroy()

        botao_salvar = ttk.Button(edit_window, text="Salvar", command=salvar_mudancas)
        botao_salvar.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = data_table(root)
    root.mainloop()
