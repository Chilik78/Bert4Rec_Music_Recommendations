import { SendReq } from "../helpers/requests";
import { SERVER_ROUTE } from "../helpers/server";

export function getAllMusicGenres(){
    SendReq({url: `${SERVER_ROUTE}/music/select_all_genres`});
}