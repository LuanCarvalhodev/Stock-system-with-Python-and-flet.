import pandas as pd  
from datetime import datetime  
import tkinter as tk  
from tkinter import messagebox
from tkinter import ttk
import random

# Estruturas de dados para Produtos, Categorias e Movimentações
# Define as classes para trabalhar com produtos, categorias e movimentações de estoque

class Categoria:
    """Classe para representar uma categoria de produto."""
    def __init__(self, id_categoria, nome):
        self.id_categoria = id_categoria 
        self.nome = nome  

class Produto:
    """Classe para representar um produto no estoque."""
    def __init__(self, id_produto, nome, categoria, preco, quantidade=0, status="Em Estoque"):
        self.id_produto = id_produto 
        self.nome = nome 
        self.categoria = categoria  
        self.preco = preco 
        self.quantidade = quantidade  
        self.status = status 

class Movimentacao:
    """Classe para registrar uma movimentação de estoque (entrada ou saída)."""
    def __init__(self, produto, tipo, quantidade):
        self.produto = produto 
        self.tipo = tipo 
        self.quantidade = quantidade  
        self.data = datetime.now()  

# Inicializando as listas que irão armazenar as categorias, produtos e movimentações
categorias = [
    Categoria(1, "Eletrônicos"),
    Categoria(2, "Móveis"),
    Categoria(3, "Eletrodomésticos"),
    Categoria(4," ")  # Categoria vazia, para produtos não categorizados
]

produtos = []  # Lista que irá armazenar os produtos cadastrados
movimentacoes = []  # Lista que irá armazenar o histórico de movimentações

def gerar_id_produto(nome):
    """Gera um ID único para o produto com base no nome."""
    for produto in produtos:
        if produto.nome.lower() == nome.lower():
            return produto.id_produto 
    while True:
        id_produto = random.randint(10000, 99999)  # Gera um número aleatório de 5 dígitos
        if not any(prod.id_produto == id_produto for prod in produtos):
            return id_produto  # Garante que o ID gerado é único

# Função para atualizar o status do produto
def atualizar_status_produto(produto):
    """Atualiza o status do produto dependendo da quantidade em estoque."""
    if produto.quantidade > 0:
        produto.status = "Em Estoque"  # Se houver quantidade em estoque, o status é "Em Estoque"
    elif produto.quantidade == 0:
        produto.status = "Em Falta"  # Se não houver quantidade, o status é "Em Falta"

# Funções para cadastrar e consultar dados no sistema
def cadastrar_categoria(id_categoria, nome):
    """Cadastra uma nova categoria no sistema."""
    categoria = Categoria(id_categoria, nome)
    categorias.append(categoria)  # Adiciona a categoria à lista de categorias

def cadastrar_produto(nome, id_categoria, preco, quantidade=0, status="Em Estoque"):
    """Cadastra um novo produto no sistema ou atualiza um produto existente."""
    id_produto = gerar_id_produto(nome)  # Gera um ID único para o novo produto
    categoria = next((cat for cat in categorias if cat.id_categoria == id_categoria), None)
    if categoria:
        # Verifica se o produto já existe
        produto_existente = next((prod for prod in produtos if prod.nome.lower() == nome.lower()), None)
        if produto_existente:
            # Se o produto já existe, pergunta ao usuário se deseja mover para outra categoria ou adicionar quantidade
            categoria_duplicada = produto_existente.categoria
            if categoria_duplicada != categoria:
                resposta = messagebox.askyesno("Produto existente", 
                                               f"O produto '{nome}' já existe na categoria '{categoria_duplicada.nome}'. Deseja adicionar a quantidade na categoria '{categoria.nome}' ou mover para essa categoria?")
                if resposta:  # Se o cliente escolheu 'Sim'
                    produto_existente.quantidade += quantidade
                    produto_existente.categoria = categoria  # Move o produto para a nova categoria
                    atualizar_status_produto(produto_existente)  # Atualiza o status
                    messagebox.showinfo("Sucesso", f"Produto '{nome}' movido para a categoria '{categoria.nome}' com {quantidade} unidades adicionais.")
                else:
                    produto_existente.quantidade += quantidade  # Apenas adiciona a quantidade
                    atualizar_status_produto(produto_existente)
                    messagebox.showinfo("Sucesso", f"Quantidade do produto '{nome}' na categoria '{categoria_duplicada.nome}' atualizada.")
            else:
                # Se o produto já está na categoria, só soma a quantidade.
                produto_existente.quantidade += quantidade
                atualizar_status_produto(produto_existente)
                messagebox.showinfo("Sucesso", f"Quantidade do produto '{nome}' na categoria '{categoria.nome}' atualizada.")
        else:
            # Se o produto não existe, cria um novo produto.
            produto = Produto(id_produto, nome, categoria, preco, quantidade, status)
            produtos.append(produto)  # Adiciona o produto à lista de produtos
            atualizar_status_produto(produto)  # Atualiza o status
            messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso na categoria '{categoria.nome}'. ID: {id_produto}")
    else:
        messagebox.showerror("Erro", "Categoria não encontrada!")  # Se a categoria não for encontrada, exibe erro

# Função para exibir produtos na tabela
def exibir_produtos(produtos_a_exibir=None):
    """Exibe os produtos cadastrados na tabela da interface gráfica."""
    for item in tree.get_children():
        tree.delete(item)  # Limpa a tabela antes de atualizar

    if produtos_a_exibir is None:
        produtos_a_exibir = produtos  

    # Insere os produtos na tabela com as informações relevantes
    for produto in produtos_a_exibir:
        tree.insert("", "end", values=(produto.id_produto, produto.nome, produto.categoria.nome, f"R$ {produto.preco:.2f}", produto.quantidade, produto.status))

# Funções para registrar movimentações de entrada e saída de estoque
def registrar_movimentacao(id_produto, tipo, quantidade):
    """Registra uma movimentação de entrada ou saída de estoque."""
    produto = next((prod for prod in produtos if prod.id_produto == id_produto), None)
    if produto:
        if tipo == 'saida' and produto.quantidade < quantidade:
            messagebox.showerror("Erro", "Quantidade insuficiente para saída.")  # Verifica se há estoque suficiente
            return
        movimentacao = Movimentacao(produto, tipo, quantidade)  # Cria a movimentação
        movimentacoes.append(movimentacao)  # Adiciona ao histórico de movimentações
        
        if tipo == 'entrada':
            produto.quantidade += quantidade  # Adiciona a quantidade ao estoque
        elif tipo == 'saida':
            produto.quantidade -= quantidade  # Remove a quantidade do estoque
        
        atualizar_status_produto(produto)  # Atualiza o status do produto
        messagebox.showinfo("Sucesso", f"Movimentação de {tipo} de {quantidade} unidades do produto '{produto.nome}' registrada.")
        exibir_produtos()  # Atualiza a tabela
    else:
        messagebox.showerror("Erro", "Produto não encontrado!")  # Se o produto não for encontrado, exibe erro

# Função para exportar dados dos produtos para um arquivo Excel
def exportar_dados_para_excel():
    """Exporta os dados dos produtos cadastrados para um arquivo Excel."""
    dados = {
        "ID Produto": [produto.id_produto for produto in produtos],
        "Nome": [produto.nome for produto in produtos],
        "Categoria": [produto.categoria.nome for produto in produtos],
        "Preço": [f"R$ {produto.preco:.2f}" for produto in produtos],
        "Quantidade em Estoque": [produto.quantidade for produto in produtos],
        "Status": [produto.status for produto in produtos]
    }
    df = pd.DataFrame(dados)  # Cria um DataFrame com os dados dos produtos
    export_path = r"C:\Users\USUARIO\Desktop\NERD\PORT\produtos.xlsx"  # Caminho do arquivo de exportação
    df.to_excel(export_path, index=False)  # Salva o DataFrame em um arquivo Excel
    messagebox.showinfo("Sucesso", f"Dados exportados para '{export_path}'.")

# Função para formatar o preço inserido pelo usuário (garante que a vírgula seja substituída por ponto)
def formatar_preco(preco):
    """Formata o preço para garantir que seja um valor numérico válido."""
    try:
        preco = preco.replace(',', '.')  # Troca a vírgula por ponto
        return float(preco)  # Converte para float
    except ValueError:
        return 0.0  # Retorna 0.0 em caso de erro

# Função para pesquisar produtos com base em nome, ID ou categoria
def pesquisar_produto():
    """Pesquisa produtos por ID, nome ou categoria."""
    termo = pesquisa_entry.get()  # Termo de pesquisa inserido pelo usuário
    categoria_selecionada = categoria_pesquisa_combobox.get()  # Categoria selecionada na combobox
    produtos_encontrados = []  

    if categoria_selecionada:  # Se uma categoria foi selecionada, filtra os produtos por categoria
        categoria = next((cat for cat in categorias if cat.nome.lower() == categoria_selecionada.lower()), None)
        if categoria:
            produtos_encontrados = [prod for prod in produtos if prod.categoria == categoria]
        else:
            messagebox.showerror("Erro", "Categoria não encontrada!")  # Exibe erro se a categoria não for encontrada
            return

    # Verifica se o termo de pesquisa é um número (ID) ou nome
    elif termo.isdigit():  # Se for um número (ID)
        id_pesquisa = int(termo)
        produtos_encontrados = [prod for prod in produtos if prod.id_produto == id_pesquisa]
    else:  # Se for um nome de produto
        produtos_encontrados = [prod for prod in produtos if termo.lower() in prod.nome.lower()]

    if produtos_encontrados:
        exibir_produtos(produtos_encontrados)  # Exibe os produtos encontrados
    else:
        messagebox.showinfo("Resultado da Pesquisa", "Nenhum produto encontrado.")  # Exibe mensagem caso não encontre produtos

# Configuração da Interface Gráfica (Tkinter)
root = tk.Tk()  # Cria a janela principal
root.title("Estoque")  # Define o título da janela

root.configure(bg="#f0f0f0")  # Configura o fundo da janela
root.geometry("1250x700")  # Define o tamanho da janela

# Frame para cadastro de produto
frame_cadastro = tk.LabelFrame(root, text="Cadastrar Produto", font=("Arial", 12, "bold"), padx=10, pady=10, bg="#f0f0f0")
frame_cadastro.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Adicionando campos para cadastro de nome, categoria, preço e quantidade.
tk.Label(frame_cadastro, text="Nome:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, pady=5, sticky="w")
nome_entry = tk.Entry(frame_cadastro, font=("Arial", 10), width=30)
nome_entry.grid(row=0, column=1, pady=5)

tk.Label(frame_cadastro, text="Categoria:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, pady=5, sticky="w")
categoria_combobox = ttk.Combobox(frame_cadastro, values=[cat.nome for cat in categorias], font=("Arial", 10), state="readonly")
categoria_combobox.grid(row=1, column=1, pady=5)

tk.Label(frame_cadastro, text="Preço (R$):", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, pady=5, sticky="w")
preco_entry = tk.Entry(frame_cadastro, font=("Arial", 10), width=30)
preco_entry.grid(row=2, column=1, pady=5)

tk.Label(frame_cadastro, text="Quantidade:", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, pady=5, sticky="w")
quantidade_entry = tk.Entry(frame_cadastro, font=("Arial", 10), width=30)
quantidade_entry.grid(row=3, column=1, pady=5)

def cadastrar_produto_interface():
    """Função para cadastrar um produto pela interface gráfica."""
    try:
        nome = nome_entry.get()
        categoria_nome = categoria_combobox.get()
        categoria = next((cat for cat in categorias if cat.nome == categoria_nome), None)
        if not categoria:
            messagebox.showerror("Erro", "Categoria inválida, selecione uma categoria existente.")
            return
        
        preco = formatar_preco(preco_entry.get())
        quantidade = int(quantidade_entry.get())
        cadastrar_produto(nome, categoria.id_categoria, preco, quantidade)
        exibir_produtos()
    except ValueError:
        messagebox.showerror("Erro", "Valores inválidos, verifique os campos.")  # Exibe erro se algum valor estiver incorreto

tk.Button(frame_cadastro, text="Cadastrar", command=cadastrar_produto_interface, font=("Arial", 10), bg="#4CAF50", fg="white", relief="raised").grid(row=4, columnspan=2, pady=10)

# Tabela para exibição de produtos
frame_tabela = tk.LabelFrame(root, text="Produtos em Estoque", font=("Arial", 12, "bold"), padx=10, pady=10, bg="#f0f0f0")
frame_tabela.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

columns = ("ID Produto", "Nome", "Categoria", "Preço", "Quantidade", "Status")  # Define as colunas da tabela
tree = ttk.Treeview(frame_tabela, columns=columns, show="headings")  
for col in columns:
    tree.heading(col, text=col) 
tree.pack()

# Frame para pesquisa de produtos
frame_pesquisa = tk.LabelFrame(root, text="Pesquisar Produto", font=("Arial", 12, "bold"), padx=10, pady=10, bg="#f0f0f0")
frame_pesquisa.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Adicionando campo de pesquisa
tk.Label(frame_pesquisa, text="Pesquisar por ID, Nome ou Categoria:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, pady=5, sticky="w")
pesquisa_entry = tk.Entry(frame_pesquisa, font=("Arial", 10), width=20)
pesquisa_entry.grid(row=0, column=1, pady=5)

# Adicionando combobox para selecionar a categoria para pesquisa
categoria_pesquisa_combobox = ttk.Combobox(frame_pesquisa, values=[cat.nome for cat in categorias], font=("Arial", 10), state="readonly")
categoria_pesquisa_combobox.grid(row=1, column=1, padx=10, pady=10)

tk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_produto, font=("Arial", 10), bg="#2196F3", fg="white", relief="raised").grid(row=2, columnspan=2, pady=5)

# Botões de movimentação e exportação
frame_opcoes = tk.LabelFrame(root, text="Opções", font=("Arial", 12, "bold"), padx=10, pady=10, bg="#f0f0f0")
frame_opcoes.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

# Botão para exportar dados para um arquivo xlsx
tk.Button(frame_opcoes, text="Exportar para Excel", command=exportar_dados_para_excel, font=("Arial", 10), bg="#2196F3", fg="white", relief="raised").grid(row=1, columnspan=2, pady=10)

# Exibir a interface gráfica
exibir_produtos()  
root.mainloop()
