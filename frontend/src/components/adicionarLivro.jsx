import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import addLivroCss from '../assets/css/adicionarLivro.module.css';

function AdicionarLivro(){
    return(
        <>
            <form action="" className={addLivroCss.formulario}>
                <h1>Adicionar livro</h1>
                <InputText type="text" placeholder="Título"/>
                <InputText type="text" placeholder="Autor"/>
                <Button label="Adicionar livro" />
            </form>
        </>
    )
}

export default AdicionarLivro;