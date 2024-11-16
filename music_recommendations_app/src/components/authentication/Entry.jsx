import Form from "./components/Form";
import {VoidUserApi} from "../../scripts/backend/user";

export function Entry(){
    return (
        <>
            <Form 
            userApi={new VoidUserApi()}
            className={'entry'} 
            inputsInfo={
                [
                    {
                        id: 0,
                        type: 'email',
                        hintText: 'Email',
                    },
                    {
                        id: 1,
                        type: 'tel',
                        hintText: 'Телефон',
                    },
                    {
                        id: 2,
                        type: 'password',
                        hintText: 'Пароль',
                    },
                ]} 
            />
        </>
    );
}