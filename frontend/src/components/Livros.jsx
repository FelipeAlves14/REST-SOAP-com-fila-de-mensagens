import axios from "axios";
import { useEffect, useState } from "react";
import { set } from "react-hook-form";

export default function Livros() {
    const [id, setId] = useState("");
    const [livros, setLivros] = useState([]);

    async function loadLivros() {
        await axios.post('http://localhost:3000/proxy', {
            url: 'http://localhost:4000/livros',
            type: 'SOAP',
        })
            .then(response => {
                setLivros(response.data);
            });
    }

    useEffect(() => {
        loadLivros()
    })

    return (
        <>
            {livros.map(livro => (
                <div key={livro.id}>
                    <h3>{livro.titulo} - {livro.autor}</h3>: {livro.n_paginas} páginas
                </div>
            ))}
        </>
    )
}