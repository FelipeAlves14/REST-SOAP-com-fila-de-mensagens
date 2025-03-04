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