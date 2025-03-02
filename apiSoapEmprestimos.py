from flask import Flask, request, Response
from lxml import etree

app = Flask(__name__)

def create_soap_response(livro_id, usuario):
    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:web="http://www.example.com/soap">
        <soapenv:Header/>
        <soapenv:Body>
            <web:emprestimosResponse>
                <web:mensagem>Livro {livro_id} emprestado para {usuario}</web:mensagem>
            </web:emprestimosResponse>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    return envelope

@app.route('/')
def get_wsdl():
    wsdl = """<?xml version="1.0" encoding="UTF-8"?>
    <definitions xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                 xmlns:web="http://www.example.com/soap"
                 xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
                 targetNamespace="http://www.example.com/soap">
        <wsdl:types>
            <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
                       targetNamespace="http://www.example.com/soap">
                <xs:element name="fazerEmprestimo">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="livro_id" type="xs:int"/>
                            <xs:element name="usuario" type="xs:string"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="fazerEmprestimoResponse">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="mensagem" type="xs:string"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
            </xs:schema>
        </wsdl:types>
        <wsdl:message name="fazerEmprestimoRequest">
            <wsdl:part name="parameters" element="web:fazerEmprestimo"/>
        </wsdl:message>
        <wsdl:message name="fazerEmprestimoResponse">
            <wsdl:part name="parameters" element="web:fazerEmprestimoResponse"/>
        </wsdl:message>
        <wsdl:portType name="BibliotecaService">
            <wsdl:operation name="fazerEmprestimo">
                <wsdl:input message="web:fazerEmprestimoRequest"/>
                <wsdl:output message="web:fazerEmprestimoResponse"/>
            </wsdl:operation>
        </wsdl:portType>
        <wsdl:binding name="BibliotecaBinding" type="web:BibliotecaService">
            <soapenv:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
            <wsdl:operation name="fazerEmprestimo">
                <soapenv:operation soapAction="http://www.example.com/soap/fazerEmprestimo"/>
                <wsdl:input>
                    <soapenv:body use="literal"/>
                </wsdl:input>
                <wsdl:output>
                    <soapenv:body use="literal"/>
                </wsdl:output>
            </wsdl:operation>
        </wsdl:binding>
        <wsdl:service name="BibliotecaService">
            <wsdl:port name="BibliotecaPort" binding="web:BibliotecaBinding">
                <soapenv:address location="http://localhost:8000/emprestimo"/>
            </wsdl:port>
        </wsdl:service>
    </definitions>
    """
    return Response(wsdl, content_type="application/xml")

@app.route("/emprestimo", methods=["GET"])
def emprestimos():
    soap_response = create_soap_response(1, "João")
    return Response(soap_response, content_type='text/xml;charset=utf-8')

if __name__ == "__main__":
    app.run(debug=True, port=4000)

@app.route('/emprestimo', methods=['POST'])
def fazer_emprestimo():
    data = request.json
    livro_id = data['livro_id']
    data_devolucao = data['data_devolucao']
    data_emprestimo = data['data_emprestimo']
    soap_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:web="http://www.example.com/soap">
        <soapenv:Header/>
        <soapenv:Body>
            <web:fazerEmprestimoResponse>
                <web:mensagem>Empréstimo válido até {data_devolucao}</web:mensagem>
            </web:fazerEmprestimoResponse>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    return Response(soap_response, content_type='text/xml;charset=utf-8')