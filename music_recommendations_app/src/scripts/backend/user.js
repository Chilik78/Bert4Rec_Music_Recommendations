import { SendReq } from "../helpers/requests";
import { SERVER_ROUTE } from "../helpers/server";

export async function isFirstEntryUser(userID){
    return await SendReq({url: `${SERVER_ROUTE}/history/is_first_entry`, data: {"user_id": userID}});
}

export async function getUserExist(data){
    return await SendReq({url: `${SERVER_ROUTE}/users/is_exist_by_values`, data: data})
}

export async function RegistrationUser(data){
    await SendReq({type: "POST", url: `${SERVER_ROUTE}/users/insert`, data: data})
}