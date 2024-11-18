import { SendReq } from "../helpers/requests";
import { SERVER_ROUTE } from "../helpers/server";

export class IMusicApi {
    getAllMusicGenres(userID){}
    getRandomMusic(){}
    getPredictedTrack(){}
}

export class VoidMusicApi extends IMusicApi{
    async getAllMusicGenres(userID){}

    #getRandomInt(max) {
        return Math.floor(Math.random() * max);
    }

    async getRandomMusic(){
        const trackNames = ['Let me hear', 'Юность', 'Aliez', 'Ghosts Again'];
        const trackAuthors = ['Fear and Loathing in Las Vegas', 'Луч', 'Sawano Hiroyuki', 'Deepeche Mode'];

        const randomIndex = this.#getRandomInt(trackNames.length);
        return [trackNames[randomIndex], trackAuthors[randomIndex]];
    }
    async getPredictedTrack(){
        return await this.getRandomMusic();
    }
}

export class RestMusicApi extends IMusicApi{
    async getAllMusicGenres(){
        return await SendReq({url: `${SERVER_ROUTE}/music/select_all_genres`});
    }
    async getRandomMusic(){
        return await SendReq({url: `${SERVER_ROUTE}/music/get_random_music`});
    }
    async getPredictedTrack(){
        return await SendReq({url: `${SERVER_ROUTE}/music/get_predicted_track`});
    }
}