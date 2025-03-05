// rodar comando "sudo rabbitmqctl purge_queue request_queue" para apagar as mensagens da fila
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const amqp = require("amqplib");
const axios = require("axios");
const cors = require('cors');
const xml2js = require('xml2js');

const app = express();
app.use(cors());
app.use(express.json()); // Permite processar JSON no body
app.use(express.urlencoded({ extended: true })); // Permite processar form-urlencoded

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
                                        self: { href: "/livros/1" }
                                    }
                                }
                            }
                        }
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
                                    _links: {
                                        self: { href: "/livros/1" }
                                    }
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
                                    _links: {
                                        self: { href: "/livros/1" }
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        description: "Erro de validação",
                        content: {
                            "application/json": {
                                example: {
                                    erro: "Todos os campos são obrigatórios"
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
    }
};

// conexão com o sistema de mensageria (RabbitMQ)
async function connectRabbitMQ() {
    const connection = await amqp.connect("amqp://localhost:5672");
    const channel = await connection.createChannel();
    await channel.assertQueue("request_queue", { durable: true });
    return channel;
};

// endpoint para adicionar uma requisição a fila
app.post("/proxy", async (req, res) => {
    try {
        const response = await startWorker();
        const channel = await connectRabbitMQ();
        const requestData = JSON.stringify(req.body);

        channel.sendToQueue("request_queue", Buffer.from(requestData), { persistent: true });
        res.status(200).json({ response: response });
    } catch (error) {
        console.error("Erro ao enviar para RabbitMQ.");
        res.status(500).json({ error: "Erro interno" });
    }
});

// worker
async function startWorker() {
    const channel = await connectRabbitMQ();

    channel.consume("request_queue", async (msg) => {
        if (msg !== null) {
            const data = JSON.parse(msg.content.toString());

            try {
                let response;

                // requisição à api rest
                if (data.type === "REST") {
                    switch (data.method) {
                        case "GET":
                            response = await axios.get(data.url, { infos: data.infos });
                            currentResponse = response.data;
                            break;
                        case "POST":
                            response = await axios.post(data.url, { infos: data.infos });
                            currentResponse = response.data;
                            break;
                        case "DELETE":
                            response = await axios.delete(data.url, { infos: data.infos });
                            currentResponse = response.data;
                            break;
                    }
                }

                // requisição à api soap
                else if (data.type === "SOAP") {
                    const getSoap = `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                                        xmlns:web="http://www.example.com/webservice">
                                        <soapenv:Header/>
                                        <soapenv:Body>
                                            <web:emprestimos/>
                                        </soapenv:Body>
                                    </soapenv:Envelope>
                                `;

                    const headers = { "Content-Type": "text/xml" };
                    response = await axios.post(data.url, getSoap, { headers });
                    response = response.data;
                    response = response.replace(/\\n/g, " ");
                    console.log("Resposta SOAP:", response);

                    const parser = new xml2js.Parser();
                    parser.parseString(response, (err, result) => {
                        if (err)
                            console.error("Erro ao converter XML:", err);
                        else
                            return JSON.stringify(result, null, 2);
                    });
                }

                channel.ack(msg); // Confirma o processamento da mensagem
            } catch (error) {
                console.error("Erro ao processar requisição");
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