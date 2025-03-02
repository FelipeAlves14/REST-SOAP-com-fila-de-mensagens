const express = require('express');
const swaggerUi = require('swagger-ui-express');
const { prisma } = require('@prisma/client');
const soapRequest = require('easy-soap-request');
const amqp = require("amqplib");
const axios = require("axios");
const xml2js = require("xml2js");

const app = express();

const RABBITMQ_URL = "amqp://localhost:5672"; 
const QUEUE_NAME = "request_queue";

// conexão com o sistema de mensageria (RabbitMQ)
async function connectRabbitMQ() {
    const connection = await amqp.connect(RABBITMQ_URL);
    const channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME, { durable: true });
    return channel;
};

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
                                    id: 1,
                                    titulo: "Ainda Estou Aqui",
                                    n_paginas: 300,
                                    autor: "Marcelo Rubens Paiva",
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
                summary: "Deletar um livro específico",
                parameters: [
                    { name: "id", in: "path", required: true, schema: { type: "string" } }
                ],
                tags: ["Livros"],
                responses: {
                    "204": {
                        description: "Livro deletado"
                    }
                }
            }
        },
        "/livros": {
            get: {
                summary: "Listar livros",
                tags: ["Livros"],
                responses: {
                    "200": {
                        description: "Lista de livros",
                        content: {
                            "application/json": {
                                example: [{
                                    id: 1,
                                    titulo: "Ainda Estou Aqui",
                                    n_paginas: 300,
                                    autor: "Marcelo Rubens Paiva",
                                }]
                            }
                        }
                    }
                }
            },
            post: {
                summary: "Criar um novo livro",
                tags: ["Livros"],
                responses: {
                    "201": {
                        description: "livro criado",
                        content: {
                            "application/json": {
                                example: {
                                    id: 1,
                                    titulo: "Ainda Estou Aqui",
                                    n_paginas: 300,
                                    autor: "Marcelo Rubens Paiva",
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
                                    titulo: "Ainda Estou Aqui",
                                    n_paginas: 300,
                                    autor: "Marcelo Rubens Paiva",
                                }
                            }
                        }
                    }
                },
            }
        },
        "/emprestimos": {
            get: {
                summary: "Listar empréstimos",
                tags: ["Empréstimos"],
                responses: {
                    "200": {
                        description: "Lista de empréstimos",
                        content: {
                            "application/json": {
                                example: [{
                                    data_emprestimo: "2022-10-10",
                                    data_devolucao: "2022-10-17",
                                    livro_id: 1
                                }]
                            }
                        }
                    }
                }
            },
            post: {
                summary: "Criar um novo empréstimo",
                tags: ["Empréstimos"],
                responses: {
                    "201": {
                        description: "Empréstimo criado",
                        content: {
                            "application/json": {
                                example: {
                                    data_emprestimo: "2022-10-10",
                                    data_devolucao: "2022-10-17",
                                    livro_id: 1
                                }
                            }
                        }
                    },
                    "400": {
                        description: "Erro de validação",
                        content: {
                            "application/json": {
                                example: {
                                    erro: "Campo 'data_emprestimo' é obrigatório"
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
                                    data_emprestimo: "2022-10-10",
                                    data_devolucao: "2022-10-17",
                                    livro_id: 1
                                }
                            }
                        }
                    }
                },
            }
        },
        "/livros/{id}/emprestimos": {
            get: {
                summary: "Obter empréstimos de um livro",
                parameters: [
                    { name: "id", in: "path", required: true, schema: { type: "string" } }
                ],
                tags: ["Empréstimos"],
                responses: {
                    "200": {
                        description: "Lista de empréstimos",
                        content: {
                            "application/json": {
                                example: {
                                    empréstimos: [{
                                        id: 1,
                                        titulo: "Ainda Estou Aqui",
                                        n_paginas: 300,
                                        autor: "Marcelo Rubens Paiva",
                                    }],
                                    _links: {
                                        self: { href: "/livros/1/emprestimos" },
                                        usuario: { href: "/livros/1" }
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

// endpoint para adicionar uma requisição a fila
app.post("/proxy", async (req, res) => {
    try {
        const channel = await connectRabbitMQ();
        const requestData = JSON.stringify(req.body);

        channel.sendToQueue(QUEUE_NAME, Buffer.from(requestData), { persistent: true });

        res.status(202).json({ status: "Requisição adicionada à fila" });
    } catch (error) {
        console.error("Erro ao enviar para RabbitMQ:", error);
        res.status(500).json({ error: "Erro interno" });
    }
});

// worker
async function startWorker() {
    const channel = await connectRabbitMQ();

    channel.consume(QUEUE_NAME, async (msg) => {
        if (msg !== null) {
            console.log("Processando requisição:", msg.content.toString());
            const data = JSON.parse(msg.content.toString());

            try {
                let response;
                // requisição à api rest
                if (data.type === "REST") {
                    response = await axios.get(data.url, { params: data.params });
                    console.log("Resposta REST:", response.data);
                }
                // requisição à api soap
                else if (data.type === "SOAP") {
                    const soapRequest = `
                        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                            <soapenv:Body>
                                <GetData>
                                    <param>${data.param}</param>
                                </GetData>
                            </soapenv:Body>
                        </soapenv:Envelope>`;

                    const headers = { "Content-Type": "text/xml" };
                    response = await axios.post(data.url, soapRequest, { headers });
                    const parsedResponse = await xml2js.parseStringPromise(response.data);
                    console.log("Resposta SOAP:", parsedResponse);
                }

                channel.ack(msg); // Confirma o processamento da mensagem
            } catch (error) {
                console.error("Erro ao processar requisição:", error);
            }
        }
    });

    console.log("Worker iniciado e aguardando requisições...");
};

app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.listen(3000, () => {
    console.log("🚀 API Gateway rodando em http://localhost:3000");
    console.log("📄 Documentação Swagger disponível em http://localhost:3000/docs");
});


// app.get('/livros', async (req, res) => {
//     await fetch('http://localhost:5000/livros')
//         .then(response => {
//             res.status(200).json(response.json());
//         });
// });

// app.post('/livros', async (req, res) => {
//     await fetch('http://localhost:5000/livros', {
//         method: 'POST',
//         body: JSON.stringify(req.body),
//         headers: { 'Content-Type': 'application/json' }
//     })
//     .then(response => {
//         res.status(201).json(response.json());
//     });
// });

// app.delete('/livros/:id', async (req, res) => {
//     await fetch(`http://localhost:5000/livros/${res.params.id}`, {
//         method: 'DELETE'
//     })
//     .then(response => {
//         res.status(204).json();
//     });
// });

// app.get('/livros/:id', async (req, res) => {
//     await fetch(`http://localhost:5000/livros/${res.params.id}`)
//         .then(response => {
//             res.status(200).json(response.json());
//         });
// });

// app.get('/livros/:id/emprestimos', async (req, res) => {
//     await fetch(`http://localhost:5000/livros/${res.params.id}/emprestimos`)
//         .then(response => {
//             res.status(200).json(response.json());
//         });
// });

// app.get('/emprestimos', async (req, res) => {
//     const envelope = `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
//         xmlns:bib="biblioteca.soap">
//     </soapenv:Envelope>`;
//     await soapRequest({
//         url: 'http://localhost:4000/emprestimos',
//         headers: {
//             'Content-Type': 'text/xml',
//             'charset': 'utf-8'
//         },
//         xml: envelope
//     })
//     .then(response => {
//         res.status(200).json(response.json());
//     });
// });

// app.post('/emprestimos', async (req, res) => {
//     const envelope = `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
//         xmlns:bib="biblioteca.soap">
//         <soapenv:Body>
//             <bib:fazer_emprestimo>
//                 <livro_id>${req.body.livro_id}</livro_id>
//                 <data_emprestimo>${req.body.data_emprestimo}</data_emprestimo>
//                 data_devolucao>${req.body.data_devolucao}</data_devolucao>
//             </bib:fazer_emprestimo>
//         </soapenv:Body>
//     </soapenv:Envelope>`;
//     await soapRequest({
//         url: 'http://localhost:4000/emprestimos',
//         headers: {
//             'Content-Type': 'text/xml',
//             'charset': 'utf-8'
//         },
//         xml: envelope
//     })
//     .then(response => {
//         res.status(201).json(response.json());
//     });
// });

