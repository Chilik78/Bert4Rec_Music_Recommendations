import Form from "./components/Form";

export function Entry(){
    return (
        <>
            <Form 
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
                ]} 
            />
        </>
    );
}