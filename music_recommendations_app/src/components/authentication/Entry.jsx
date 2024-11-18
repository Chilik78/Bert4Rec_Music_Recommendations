import Form from "./components/Form";
import DI from "../../scripts/backend/di";

export function Entry(){
    return (
        <>
            <Form 
            userApi={DI.userApi}
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