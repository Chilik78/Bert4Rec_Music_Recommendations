
export async function SendReq({type="GET", url="/", data=undefined}){
    
    console.log(`TYPE: ${type}`);
    console.log(`URL: ${url}`);
    console.log("INPUT DATA:");
    console.log(data);
    
    let response;

    if(type === "GET"){
        data = typeof data === "undefined" ? "" : "?" + ConvertDataToString(data);
        response = await fetch(url + data, {method: type});
    }
    else if(type === "POST"){
        response = await fetch(
            url, 
            {
                //mode: 'no-cors',
                method: type, 
                body: JSON.stringify(data), 
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }
        );
    }

    if (response.ok) {
        let json = await response.json();
        //console.log("Ответ сервера:")
        //console.log(json);
        return json; 
    } else {
        //alert("Ошибка HTTP: " + response.status);
        console.warn("Response not ok")
    }

    // const Http = new XMLHttpRequest();

    // Http.open(type, url + data, true);

    // Http.onreadystatechange = (e) => {
    //     if(Http.readyState === XMLHttpRequest.DONE){
    //         console.log("Ответ сервера:")
    //         console.log(Http.responseText); 
    //         return Http.responseText;
    //     } 
    // }

    // Http.onerror = (e) =>{
    //     console.log("Ошибка при отправлении запроса");
    //     console.log(`${data}`);
    // }

    // Http.send();

    
}

export async function GetUrlToDownload({url="/", file=undefined}){
    
        let response = await fetch(
            url+file, 
            {
                method: 'POST', 
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }
        );
        
    if (response.ok) {
        const blob = await response.blob();
        return URL.createObjectURL(blob); 
    } else {
        alert("Ошибка HTTP: " + response.status);
    }

    // const Http = new XMLHttpRequest();

    // Http.open(type, url + data, true);

    // Http.onreadystatechange = (e) => {
    //     if(Http.readyState === XMLHttpRequest.DONE){
    //         console.log("Ответ сервера:")
    //         console.log(Http.responseText); 
    //         return Http.responseText;
    //     } 
    // }

    // Http.onerror = (e) =>{
    //     console.log("Ошибка при отправлении запроса");
    //     console.log(`${data}`);
    // }

    // Http.send();

    
}

function ConvertDataToString(data){
    let keys = Object.keys(data);
    let result = "";

    keys.forEach(key => {
        result += `${key}=${data[key]}&`;
    });

    result = result.slice(0, -1);

    return result;
}