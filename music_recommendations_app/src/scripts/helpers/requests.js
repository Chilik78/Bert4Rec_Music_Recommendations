function sendGetReq(url){
    const Http = new XMLHttpRequest();
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        console.log(Http.responseText); 
    }
}


function sendPostReq(url, data){
    const Http = new XMLHttpRequest();
    Http.open("POST", url);
    Http.send(JSON.stringify(data));
}