from flask import Flask, Response
import sqlite3

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

app = Flask(__name__)

@app.route('/')
def get_wsdl():
    wsdl = """<?xml version="1.0" encoding="UTF-8"?>
                <definitions xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
                    xmlns:web="http://www.example.com/webservice"
                    xmlns="http://schemas.xmlsoap.org/wsdl/"
                    targetNamespace="http://www.example.com/webservice"
                    name="LivrosService">
                    <types>
                        <xsd:schema targetNamespace="http://www.example.com/webservice">
                            <xsd:element name="livrosRequest" type="xsd:anyType"/>
                            <xsd:element name="livrosResponse">
                                <xsd:complexType>
                                    <xsd:sequence>
                                        <xsd:element name="items" minOccurs="0" maxOccurs="unbounded">
                                            <xsd:complexType>
                                                <xsd:sequence>
                                                    <xsd:element name="id" type="xsd:int"/>
                                                    <xsd:element name="titulo" type="xsd:string"/>
                                                    <xsd:element name="autor" type="xsd:string"/>
                                                    <xsd:element name="n_paginas" type="xsd:int"/>
                                                    <xsd:element name="_links">
                                                        <xsd:complexType>
                                                            <xsd:sequence>
                                                                <xsd:element name="self" type="xsd:string"/>
                                                            </xsd:sequence>
                                                        </xsd:complexType>
                                                    </xsd:element>
                                                </xsd:sequence>
                                            </xsd:complexType>
                                        </xsd:element>
                                    </xsd:sequence>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:schema>
                    </types>
                    <message name="livrosRequest">
                        <part name="parameters" element="web:livrosRequest"/>
                    </message>
                    <message name="livrosResponse">
                        <part name="parameters" element="web:livrosResponse"/>
                    </message>
                    <portType name="LivrosPortType">
                        <operation name="livros">
                            <input message="web:livrosRequest"/>
                            <output message="web:livrosResponse"/>
                        </operation>
                    </portType>
                    <binding name="LivrosBinding" type="web:LivrosPortType">
                        <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
                        <operation name="livros">
                            <soap:operation soapAction="http://www.example.com/webservice/livros"/>
                            <input>
                                <soap:body use="literal"/>
                            </input>
                            <output>
                                <soap:body use="literal"/>
                            </output>
                        </operation>
                    </binding>
                    <service name="LivrosService">
                        <port name="LivrosPort" binding="web:LivrosBinding">
                            <soap:address location="http://localhost:4000/livros"/>
                        </port>
                    </service>
                </definitions>
    """
    return Response(wsdl, content_type="application/xml")

@app.route("/livros", methods=["POST"])
def livros():
    conn = sqlite3.connect("livros.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros;")
    livros = "".join([f"""<web:item>
        <web:id>{row[0]}</web:id>
        <web:titulo>{row[1]}</web:titulo>
        <web:autor>{row[2]}</web:autor>
        <web:n_paginas>{row[3]}</web:n_paginas>
        <web:_links>
            <web:self>/livros/{row[0]}</web:self>
        </web:_links>
    </web:item>"""
        for row in cursor.fetchall()])
    conn.close()

    soap_response = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:web="http://www.example.com/webservice">
                <soapenv:Header/>
                <soapenv:Body>
                   <web:livrosResponse>
                      <web:items>
                      {livros}
                      </web:items>
                   </web:livrosResponse>
                </soapenv:Body>
                </soapenv:Envelope>"""

    return Response(soap_response, content_type='text/xml;charset=utf-8')

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=4000)

# @app.route('/emprestimos', methods=['POST'])
# def fazer_emprestimo():
#     data = request.json
#     livro_id = data['livro_id']
#     data_devolucao = data['data_devolucao']
#     data_emprestimo = data['data_emprestimo']
#     soap_response = f"""<?xml version="1.0" encoding="UTF-8"?>
#     <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
#                       xmlns:web="http://www.example.com/soap">
#         <soapenv:Header/>
#         <soapenv:Body>
#             <web:fazerEmprestimoResponse>
#                 <web:mensagem>Empréstimo válido até {data_devolucao}</web:mensagem>
#             </web:fazerEmprestimoResponse>
#         </soapenv:Body>
#     </soapenv:Envelope>
#     """
#     return Response(soap_response, content_type='text/xml;charset=utf-8')