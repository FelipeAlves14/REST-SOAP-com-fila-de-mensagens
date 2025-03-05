from urllib import request
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__) # inicializa o servidor e permiter que o flask saiba onde o script está sendo executado

def init_db():
    conn = sqlite3.connect("livros.sqlite3")  # Banco de dados salvo como .sqlite3
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            n_paginas INTEGER,
            autor TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# Rota para adicionar um novo livro ao banco de dados
@app.route('/livros', methods=['POST'])
def add_livro():
    livro = request.get_json()
    novo_livro = livro['infos']
    conn = sqlite3.connect("livros.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO livros (titulo, n_paginas, autor) VALUES (?, ?, ?)", (novo_livro["titulo"], novo_livro["n_paginas"], novo_livro["autor"]))
    conn.commit()
    
    livro_id = cursor.lastrowid  # Obtém o ID gerado automaticamente
    conn.close()

    novo_livro["id"] = livro_id
    novo_livro["_links"] = {"self": f"/livros/{livro_id}"}
    
    return jsonify(novo_livro), 201

# Iniciar o banco de dados e rodar o servidor Flask
if __name__ == "__main__":
    init_db()  # Criar a tabela se ainda não existir
    app.run(port=5000)

    
# ----------------------------------- VERSÃO COM DADOS MOCADOS
# from flask import Flask, jsonify, request

# Dados mockados
# LIVROS = [
#     {"id": 1, "titulo": "Dom Casmurro", "n_paginas": 300, "autor": "Machado de Assis", "_links": {"self": "/livros/1", "emprestimos": "/livros/1/emprestimos"}},
#     {"id": 2, "titulo": "1984", "n_paginas": 328, "autor": "George Orwell", "_links": {"self": "/livros/2", "emprestimos": "/livros/2/emprestimos"}},
#     {"id": 3, "titulo": "A Moreninha", "n_paginas": 212, "autor": "Joaquim Manuel de Macedo", "_links": {"self": "/livros/3", "emprestimos": "/livros/3/emprestimos"}}
# ]

# app = Flask(__name__)

# # Rota para obter todos os livros mockados
# @app.route('/livros', methods=['GET'])
# def get_livros():
#     return jsonify({"livros": LIVROS})

# # Rota para adicionar um novo livro (mockado)
# @app.route('/livros', methods=['POST'])
# def add_livro():
#     livro = request.get_json()
#     novo_livro = {}
#     novo_id = len(LIVROS) + 1  # Simulando um ID único
#     novo_livro["id"] = novo_id
#     novo_livro["infos"] = livro['infos']
#     # Simula a criação de um novo livro
#     novo_livro["_links"] = {"self": f"/livros/{novo_id}", "emprestimos": f"/livros/{novo_id}/emprestimos"}
    
#     LIVROS.append(novo_livro)  # Adiciona o livro mockado à lista
    
#     return jsonify(novo_livro), 201

# # Iniciar o servidor Flask
# if __name__ == "__main__":
#     app.run(port=5000)
    
# Rota para obter todos os livros do banco de dados
# @app.route('/livros', methods=['GET'])
# def get_livros():
# conn = sqlite3.connect("livros.sqlite3")
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM livros;")
# livros = [
#     {"id": row[0], 
#     "titulo": row[1], 
#     "n_paginas": row[2], 
#     "autor": row[3], 
#     "_links": {
#         "self": f"/livros/{row[0]}", 
#         "emprestimos": f"/livros/{row[0]}/emprestimos"
#     }
# } for row in cursor.fetchall()]
# conn.close()

#     return jsonify({"livros": LIVROS})