
export function Circle({size, zIndex='0', margin='0 0 0 0'}){
    return (
        <div className="Circle" 
        style={{width: size, height: size, zIndex:zIndex, margin: margin, position: 'absolute',
        borderRadius: '50%', backgroundColor: '#c115aa'}}>
        </div>
    )
}