import Form from "./components/Form";

export function Registration(){
    return (
        <>
            <Form 
            className={'registration'} 
            inputsInfo={
                [
                    {
                        id: 0,
                        type: 'text',
                        hintText: 'Имя пользователя',
                    },
                    {
                        id: 1,
                        type: 'email',
                        hintText: 'Почта',
                    },
                    {
                        id: 2,
                        type: 'tel',
                        hintText: 'Номер телефона',
                    },
                    {
                        id: 3,
                        type: 'password',
                        hintText: 'Пароль',
                    },
                ]} 
            />
        </>
    );
}