from urllib import request
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__) # iniciaçiza o servidor e permiter que o flask saiba onde o script está sendo executado

def init_db():
    conn = sqlite3.connect("livros.sqlite3")  # Banco de dados salvo como .sqlite3
    cursor = conn.cursor()
    cursor.execute("""
    ALTER TABLE livros
        ADD n_paginas INT;
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros_2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            n_paginas INTEGER,
            autor TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# povoamento de livros local
# livros = [
#     {"id": 1, "titulo": "1984", "autor": "George Orwell", "_links": {"self": "/livros/1"}},
#     {"id": 2, "titulo": "Dom Quixote", "autor": "Miguel de Cervantes", "_links": {"self": "/livros/2"}},
#     {"id": 3, "titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "_links": {"self": "/livros/3"}},
#     {"id": 4, "titulo": "Orgulho e Preconceito", "autor": "Jane Austen", "_links": {"self": "/livros/4"}},
#     {"id": 5, "titulo": "Crime e Castigo", "autor": "Fiódor Dostoiévski", "_links": {"self": "/livros/5"}},
#     {"id": 6, "titulo": "Cem Anos de Solidão", "autor": "Gabriel García Márquez", "_links": {"self": "/livros/6"}},
#     {"id": 7, "titulo": "A Revolução dos Bichos", "autor": "George Orwell", "_links": {"self": "/livros/7"}},
#     {"id": 8, "titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "_links": {"self": "/livros/8"}},
#     {"id": 9, "titulo": "O Nome do Vento", "autor": "Patrick Rothfuss", "_links": {"self": "/livros/9"}},
#     {"id": 10, "titulo": "Harry Potter e a Pedra Filosofal", "autor": "J.K. Rowling", "_links": {"self": "/livros/10"}},
#     {"id": 11, "titulo": "Moby Dick", "autor": "Herman Melville", "_links": {"self": "/livros/11"}},
#     {"id": 12, "titulo": "As Crônicas de Nárnia", "autor": "C.S. Lewis", "_links": {"self": "/livros/12"}},
#     {"id": 13, "titulo": "O Hobbit", "autor": "J.R.R. Tolkien", "_links": {"self": "/livros/13"}},
#     {"id": 14, "titulo": "Os Miseráveis", "autor": "Victor Hugo", "_links": {"self": "/livros/14"}},
#     {"id": 15, "titulo": "O Conde de Monte Cristo", "autor": "Alexandre Dumas", "_links": {"self": "/livros/15"}},
#     {"id": 16, "titulo": "Admirável Mundo Novo", "autor": "Aldous Huxley", "_links": {"self": "/livros/16"}},
#     {"id": 17, "titulo": "O Morro dos Ventos Uivantes", "autor": "Emily Brontë", "_links": {"self": "/livros/17"}},
#     {"id": 18, "titulo": "A Menina que Roubava Livros", "autor": "Markus Zusak", "_links": {"self": "/livros/18"}},
#     {"id": 19, "titulo": "A Metamorfose", "autor": "Franz Kafka", "_links": {"self": "/livros/19"}},
#     {"id": 20, "titulo": "Drácula", "autor": "Bram Stoker", "_links": {"self": "/livros/20"}}
# ]

# Rota para obter todos os livros do banco de dados
@app.route('/livros', methods=['GET'])
def get_livros():
    conn = sqlite3.connect("livros.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, autor FROM livros")
    
    livros = [
        {"id": row[0], 
        "titulo": row[1], 
        "n_paginas": row[2], 
        "autor": row[3], 
        "_links": {
            "self": f"/livros/{row[0]}", 
            "emprestimos": f"/livros/{row[0]}/emprestimos"
        }
    } for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({"livros": livros})

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