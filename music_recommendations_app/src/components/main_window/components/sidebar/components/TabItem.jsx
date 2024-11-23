export function TabItem({id, logo, text, selected, onClick}){


    const getClassName = () => {
        if(selected)
            return "tab-item-selected";

        return "tab-item";
    };


    return (
        <div onClick={() => onClick(id)} className={getClassName()}>   
            <div className='tab-item-icon'>
                {logo}
            </div>
            <h1>{text}</h1>
        </div>
    );
}