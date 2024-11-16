import { SendReq } from "../helpers/requests";
import { SERVER_ROUTE } from "../helpers/server";


export class IUserApi {
    isFirstEntryUser(userID){}
    getUserExist(data){}
    RegistrationUser(data){}
}

export class VoidUserApi {
    isFirstEntryUser(userID){
        return true;
    }
    getUserExist(data){
        return [true, 'idblya'];
    }
    RegistrationUser(data){

    }
}

export class RestUserApi extends IUserApi{
    async isFirstEntryUser(userID){
        return await SendReq({url: `${SERVER_ROUTE}/history/is_first_entry`, data: {"user_id": userID}});
    }
    
    async getUserExist(data){
        return await SendReq({url: `${SERVER_ROUTE}/users/is_exist_by_values`, data: data})
    }
    
    async RegistrationUser(data){
        await SendReq({type: "POST", url: `${SERVER_ROUTE}/users/insert`, data: data})
    }
}
