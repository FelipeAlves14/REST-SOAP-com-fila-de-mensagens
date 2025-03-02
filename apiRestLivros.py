from urllib import request
from flask import Flask, jsonify

app = Flask(__name__) # iniciaçiza o servidor e permiter que o flask saiba onde o script está sendo executado

# povoamento de livros local
livros = [
    {"id": 1, "titulo": "1984", "autor": "George Orwell", "_links": {"self": "/livros/1"}},
    {"id": 2, "titulo": "Dom Quixote", "autor": "Miguel de Cervantes", "_links": {"self": "/livros/2"}},
    {"id": 3, "titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "_links": {"self": "/livros/3"}},
    {"id": 4, "titulo": "Orgulho e Preconceito", "autor": "Jane Austen", "_links": {"self": "/livros/4"}},
    {"id": 5, "titulo": "Crime e Castigo", "autor": "Fiódor Dostoiévski", "_links": {"self": "/livros/5"}},
    {"id": 6, "titulo": "Cem Anos de Solidão", "autor": "Gabriel García Márquez", "_links": {"self": "/livros/6"}},
    {"id": 7, "titulo": "A Revolução dos Bichos", "autor": "George Orwell", "_links": {"self": "/livros/7"}},
    {"id": 8, "titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "_links": {"self": "/livros/8"}},
    {"id": 9, "titulo": "O Nome do Vento", "autor": "Patrick Rothfuss", "_links": {"self": "/livros/9"}},
    {"id": 10, "titulo": "Harry Potter e a Pedra Filosofal", "autor": "J.K. Rowling", "_links": {"self": "/livros/10"}},
    {"id": 11, "titulo": "Moby Dick", "autor": "Herman Melville", "_links": {"self": "/livros/11"}},
    {"id": 12, "titulo": "As Crônicas de Nárnia", "autor": "C.S. Lewis", "_links": {"self": "/livros/12"}},
    {"id": 13, "titulo": "O Hobbit", "autor": "J.R.R. Tolkien", "_links": {"self": "/livros/13"}},
    {"id": 14, "titulo": "Os Miseráveis", "autor": "Victor Hugo", "_links": {"self": "/livros/14"}},
    {"id": 15, "titulo": "O Conde de Monte Cristo", "autor": "Alexandre Dumas", "_links": {"self": "/livros/15"}},
    {"id": 16, "titulo": "Admirável Mundo Novo", "autor": "Aldous Huxley", "_links": {"self": "/livros/16"}},
    {"id": 17, "titulo": "O Morro dos Ventos Uivantes", "autor": "Emily Brontë", "_links": {"self": "/livros/17"}},
    {"id": 18, "titulo": "A Menina que Roubava Livros", "autor": "Markus Zusak", "_links": {"self": "/livros/18"}},
    {"id": 19, "titulo": "A Metamorfose", "autor": "Franz Kafka", "_links": {"self": "/livros/19"}},
    {"id": 20, "titulo": "Drácula", "autor": "Bram Stoker", "_links": {"self": "/livros/20"}}
]

# rota para fazer um get de livros
@app.route('/livros', methods=['GET'])
def get_livros():
    return jsonify({"livros": livros})

@app.route('/livros', methods=['POST'])
def add_livro():
    novo_livro = request.json
    novo_livro["id"] = len(livros) + 1
    novo_livro["_links"] = {"self": f"/livros/{novo_livro['id']}"}
    livros.append(novo_livro)
    return jsonify(novo_livro), 201

# executar o servidor flask na porta 5001
app.run(port=5000)