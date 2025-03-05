import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import addLivroCss from '../assets/css/adicionarLivro.module.css';
import axios from "axios";
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useForm } from 'react-hook-form';
import Livros from './Livros';

function AdicionarLivro() {
    const schema = yup.object().shape({
        titulo: yup.string().required(),
        autor: yup.string().required(),
        n_paginas: yup.number().required()
    })

    const { handleSubmit, register, formState: { errors } } = useForm({
        resolver: yupResolver(schema)
    });

    const submitBook = async (data) => {
        await axios.post('http://localhost:3000/proxy', {
            url: 'http://localhost:5000/livros',
            type: 'REST',
            method: 'POST',
            infos: {
                titulo: data.titulo,
                n_paginas: data.n_paginas,
                autor: data.autor
            }
        });
    }

    return (
        <>
            <form onSubmit={handleSubmit(submitBook)} action="POST" className={addLivroCss.formulario}>
                <h1>Adicionar livro</h1>
                <InputText type="text" placeholder="Título" name="titulo" {...register("titulo")} />
                {errors.titulo && <p>{errors.titulo.message}</p>}
                <InputText type="number" placeholder="Número de páginas" name="n_paginas" {...register("n_paginas")} />
                {errors.n_paginas && <p>{errors.n_paginas.message}</p>}
                <InputText type="text" placeholder="Autor" name="autor" {...register("autor")} />
                {errors.autor && <p>{errors.autor.message}</p>}
                <Button label="Adicionar livro" type='submit' />
            </form>
        </>
    )
}

export default AdicionarLivro;