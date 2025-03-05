import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Calendar } from 'primereact/calendar';
import { useState } from 'react';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useForm } from 'react-hook-form';
import axios from 'axios';


function AdicionarEmprestimo() {
    const schema = yup.object().shape({
        id_livro: yup.string().required(),
        data_emprestimo: yup.date().required(),
        data_devolucao: yup.date().nullable()
    })

    const [date, setDate] = useState("01/01/2000");
    const [devolutionDate, setDevolutionDate] = useState("01/01/2000");

    const { handleSubmit, register, formState: { errors } } = useForm({
        resolver: yupResolver(schema)
    });

    const submitEmprestimo = async (data) => {
        await axios.post('http://localhost:3000/proxy', {
            url: 'http://localhost:5000/emprestimos',
            type: 'SOUP',
            method: 'POST',
            infos: {
                id_livro: data.id_livro,
                data_emprestimo: data.data_emprestimo,
                data_devolucao: data.data_devolucao || null
            }
        })
    }

    return(
        <>
            <h1>Realizar empréstimo</h1>
            <form onSubmit={handleSubmit(submitEmprestimo)} >
                <Calendar value={date} onChange={(e) => {setDate(e.value); setValue('data_emprestimo', e.value);}} dateFormat="dd/mm/yy" placeholder='Data do empréstimo' {...register("data_emprestimo")}/>
                <Calendar value={devolutionDate} onChange={(e) => setDevolutionDate(e.value)} dateFormat="dd/mm/yy" placeholder='Data de devolução'  {...register("data_devolucao")}/>
                <InputText type='text' placeholder='Id do livro' {...register("id_livro")} />
                <Button label='Emprestar livro' type='submit'/>
            </form>
        </>
    )
}