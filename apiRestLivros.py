from flask import Flask, jsonify

app = Flask(__name__) # iniciaçiza o servidor e permiter que o flask saiba onde o script está sendo executado

# povoamento de livros local
livros = [
    {"id": 1, "titulo": "1984", "autor": "George Orwell", "_links": {"self": "/livros/1"}},
    {"id": 2, "titulo": "Dom Quixote", "autor": "Miguel de Cervantes", "_links": {"self": "/livros/2"}}
]

# rota para fazer um get de livros
@app.route('/livros', methods=['GET'])
def get_livros():
    return jsonify({"livros": livros})

# executar o servidor flask na porta 5001
app.run(port=5001): 