const express = require('express');
const swaggerUi = require('swagger-ui-express');

const app = express();

// Definição do Swagger
const swaggerDocument = {
    openapi: "3.0.0",
    info: {
        title: "API Gateway com HATEOAS",
        version: "1.0.0",
        description: "API Gateway com links HATEOAS e documentação Swagger"
    },
    servers: [{ url: "http://localhost:3000" }],
    paths: {
        "/livros/{id}": {
            get: {
                summary: "Obter detalhes de um livro",
                parameters: [
                    { name: "id", in: "path", required: true, schema: { type: "string" } }
                ],
                tags: ["Livros"],
                responses: {
                    "200": {
                        description: "Livro encontrado",
                        content: {
                            "application/json": {
                                example: {
                                    id: "1",
                                    nome: "João",
                                    _links: {
                                        self: { href: "/livros/1" },
                                        emprestimo: { href: "/livros/1/emprestimo" }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            delete: {
                summary: "Deletar um usuário específico",
                parameters: [
                    { name: "id", in: "path", required: true, schema: { type: "string" } }
                ],
                tags: ["Usuários"],
                responses: {
                    "204": {
                        description: "Usuário deletado"
                    }
                }
            }
        },
        "/usuarios": {
            get: {
                summary: "Listar usuários",
                tags: ["Usuários"],
                responses: {
                    "200": {
                        description: "Lista de usuários",
                        content: {
                            "application/json": {
                                example: [
                                    { id: "1", nome: "João" },
                                    { id: "2", nome: "Maria" }
                                ]
                            }
                        }
                    }
                }
            },
            post: {
                summary: "Criar um novo usuário",
                tags: ["Usuários"],
                responses: {
                    "201": {
                        description: "Usuário criado",
                        content: {
                            "application/json": {
                                example: {
                                    id: "3",
                                    nome: "José"
                                }
                            }
                        }
                    },
                    "400": {
                        description: "Erro de validação",
                        content: {
                            "application/json": {
                                example: {
                                    erro: "Campo 'nome' é obrigatório"
                                }
                            }
                        }
                    }
                },
                requestBody: {
                    content: {
                        "application/json": {
                            schema: {
                                type: "object",
                                properties: {
                                    idade: { type: "string" },
                                    nome: { type: "string" }
                                }
                            }
                        }
                    }
                },
            }
        },
        "/usuarios/{id}/pedidos": {
            get: {
                summary: "Obter pedidos de um usuário",
                parameters: [
                    { name: "id", in: "path", required: true, schema: { type: "string" } }
                ],
                tags: ["Pedidos"],
                responses: {
                    "200": {
                        description: "Lista de pedidos",
                        content: {
                            "application/json": {
                                example: {
                                    pedidos: [
                                        { id: 1, usuarioId: "1", valor: 99.90 },
                                        { id: 2, usuarioId: "1", valor: 150.00 }
                                    ],
                                    _links: {
                                        self: { href: "/usuarios/1/pedidos" },
                                        usuario: { href: "/usuarios/1" }
                                    }
                                }
                            }
                        }
                    }
                }
            },
        }
    }
};

// Rota para usuários com HATEOAS
app.get('/usuarios/:id', (req, res) => {
    const userId = req.params.id;
    res.json({
        id: userId,
        nome: "João",
        _links: {
            self: { href: `/usuarios/${userId}` },
            pedidos: { href: `/usuarios/${userId}/pedidos` }
        }
    });
});

// Rota para pedidos com HATEOAS
app.get('/usuarios/:id/pedidos', (req, res) => {
    const userId = req.params.id;
    res.json({
        pedidos: [
            { id: 1, usuarioId: userId, valor: 99.90 },
            { id: 2, usuarioId: userId, valor: 150.00 }
        ],
        _links: {
            self: { href: `/usuarios/${userId}/pedidos` },
            usuario: { href: `/usuarios/${userId}` }
        }
    });
});

// Documentação Swagger
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Inicia o servidor
app.listen(3000, () => {
    console.log("🚀 API Gateway rodando em http://localhost:3000");
    console.log("📄 Documentação Swagger disponível em http://localhost:3000/docs");
});
