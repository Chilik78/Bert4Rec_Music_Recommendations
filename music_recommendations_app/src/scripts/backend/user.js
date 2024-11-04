import { SendReq } from "../helpers/requests";
import { SERVER_ROUTE } from "../helpers/server";

export function isFirstEntryUser(userID){
    return true;
}

export async function getUserExist(data){
    return await SendReq({url: `${SERVER_ROUTE}/users/is_exist_by_value`, data: data})
}

export async function RegistrationUser(data){
    await SendReq({type: "POST", url: `${SERVER_ROUTE}/users/insert`, data: data})
}