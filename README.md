# Gerenciador de Estoque

Este projeto é um **Gerenciador de Estoque** desenvolvido em Python com interface gráfica utilizando **ttkbootstrap** e **tkinter**. Ele permite o gerenciamento completo de um inventário de produtos, incluindo funcionalidades como adição, listagem, edição, exclusão e filtragem de produtos.

## Funcionalidades

- **Adicionar produtos:** Inclua novos itens no inventário, especificando nome, categoria, quantidade e preço.
- **Listar produtos:** Visualize todos os produtos cadastrados no inventário.
- **Editar produtos:** Atualize informações de itens específicos, como nome, categoria, quantidade e preço.
- **Excluir produtos:** Remova itens do inventário usando o ID.
- **Filtrar produtos:** Busque por categorias e ordene os resultados por nome, quantidade ou preço.
- **Salvar e carregar inventário:** Os dados são persistidos em um arquivo JSON, garantindo que o inventário seja mantido entre execuções do programa.

## Pré-requisitos

- **Python 3.10 ou superior**
- Biblioteca **ttkbootstrap**

### Instalando o ttkbootstrap

```bash
pip install ttkbootstrap
```

## Como executar

1. Certifique-se de ter o Python e as dependências instaladas.
2. Clone este repositório ou copie os arquivos do projeto.
3. Execute o script principal:

```bash
python main.py
```

## Estrutura do Projeto

- **`inventario.json`**: Arquivo onde os dados do inventário são armazenados.
- **Funções principais:**
  - `adicionar_produto()`: Adiciona um novo produto ao inventário.
  - `listar_produtos()`: Lista todos os produtos do inventário.
  - `atualizar_produto()`: Atualiza informações de um produto específico.
  - `excluir_produto()`: Remove um produto do inventário pelo ID.
- **Interface gráfica:**
  - Criada com `ttkbootstrap` e `tkinter` para uma interface moderna e amigável ao usuário.

## Detalhes da Interface

- **Tabela de produtos:** Exibe todos os itens do inventário com as colunas: ID, Nome, Categoria, Quantidade e Preço.
- **Botões de ação:**
  - Adicionar produto.
  - Editar produto.
  - Excluir produto.
  - Filtrar e buscar itens.

## Exemplo de Uso

1. **Adicionando um produto:**
   - Clique no botão **Adicionar**.
   - Preencha os campos "Nome", "Categoria", "Quantidade" e "Preço".
   - Clique em **Salvar** para registrar o produto.

2. **Editando um produto:**
   - Selecione o produto na tabela.
   - Clique no botão **Editar** e faça as alterações necessárias.
   - Clique em **Salvar**.

3. **Excluindo um produto:**
   - Selecione o produto na tabela e clique em **Excluir**.
   - Ou use o ID do produto para excluir manualmente.

4. **Filtrando e ordenando:**
   - Clique no botão **Filtrar**, escolha uma categoria e um critério de ordenação.
   - Clique em **Aplicar** para ver os resultados filtrados.

## Tecnologias Utilizadas

- **Python**
- **tkinter**
- **ttkbootstrap**
- **JSON**

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).




---

Se tiver dúvidas ou problemas, entre em contato!