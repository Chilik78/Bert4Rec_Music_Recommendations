import { SendReq } from "../helpers/requests";
import { SERVER_ROUTE } from "../helpers/server";

export async function getAllMusicGenres(){
    return await SendReq({url: `${SERVER_ROUTE}/music/select_all_genres`});
}