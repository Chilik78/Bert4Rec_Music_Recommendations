export function TabItem({logo, text}){
    return (
        <div className="tab-item">   
            <div className='tab-item-icon'>
                {logo}
            </div>
            <h1>{text}</h1>
        </div>
    );
}