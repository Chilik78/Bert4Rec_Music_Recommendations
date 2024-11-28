import { SendReq, GetUrlToDownload } from "../helpers/requests";
import { SERVER_ROUTE } from "../helpers/server";

export class IMusicApi {
    getAllMusicGenres(){}
    getRandomMusic(){}
    getPredictedTrack(){}
}

export class VoidMusicApi extends IMusicApi{
    async getAllMusicGenres(){
        return ['rock','pop','folk','dance','rusrap','world','electronic','alternative',
            'children','rnb','hip','jazz','postrock','latin','classical','metal',
            'ruspop','reggae','tatar','blues','instrumental','rusrock','dnb','türk',
            'post','country','psychedelic','conjazz','indie','posthardcore','local',
            'avantgarde','punk','videogame','christmas','melodic','caucasian',
            'reggaeton','soundtrack','singer','ska','shanson','ambient','film',
            'western','rap','beats', "hard'n'heavy", 'progmetal','minimal',
            'contemporary','new','soul','holiday','german','techno','tropical',
            'fairytail','spiritual','urban','house','gospel','nujazz','folkmetal',
            'trance','miscellaneous','anime','hardcore','progressive','chanson',
            'numetal','vocal','estrada','dubstep','club','deep','southern','black',
            'folkrock','fitness','french','disco','religious','hiphop','drum',
            'extrememetal','türkçe','experimental','russian','easy','metalcore',
            'modern','argentinetango','old','breaks','eurofolk','stonerrock',
            'industrial','funk','jpop','middle','variété','other','adult','christian',
            'gothic','international','muslim','relax','schlager','caribbean',
            'ukrrock','nu','breakbeat','comedy','chill','newage','specialty','uzbek',
            'k-pop','balkan','chinese','meditative','dub','classicmetal','power',
            'death','grime','arabesk','romance','flamenco','leftfield','european',
            'tech','newwave','dancehall','mpb','piano','top','bigroom','opera',
            'celtic','tradjazz','acoustic','epicmetal','historisch','downbeat',
            'africa','audiobook','jewish','deutschrock','eastern','action','folklore',
            'bollywood','marschmusik','rnr','karaoke','downtempo','indian',
            'rancheras','электроника','afrikaans','tango','rhythm','sound',
            'deutschspr','trip','lovers','choral','dancepop','podcasts','future',
            'retro','smooth','mexican','brazilian','mood','surf','gangsta','triphop',
            'inspirational','idm','ethnic','bluegrass','broadway','animated',
            'americana','karadeniz','rockabilly','colombian','self','synthrock',
            'sertanejo','japanese','canzone','swing','lounge','sport','korean',
            'ragga','traditional','gitarre','frankreich','alternativepunk','emo',
            'laiko','cantopop','electropop','glitch','documentary','rockalternative',
            'thrash','hymn','oceania','rockother','dark','vi','grunge','hardstyle',
            'samba','garage','soft','art','folktronica','entehno','mediterranean',
            'chamber','cuban','taraftar','rockindie','gypsy','hardtechno',
            'shoegazing','skarock','bossa','salsa','latino','worldbeat','malaysian',
            'baile','loungeelectronic','arabic','acid','kayokyoku','neoklassik',
            'tribal','tanzorchester','native','independent','cantautori','poprussian',
            'punjabi','synthpop','rave','französisch','quebecois','speech','teen',
            'jam','soulful','horror','orchestral','neue','roots','slow','jungle',
            'indipop','axé','fado','showtunes','arena','irish','ram','mandopop',
            'forró','popdance','regional'];
    }

    #getRandomInt(max) {
        return Math.floor(Math.random() * max);
    }

    async getRandomMusic(){
        const trackNames = ['Let me hear', 'Юность', 'Aliez', 'Ghosts Again'];
        const trackAuthors = ['Fear and Loathing in Las Vegas', 'Луч', 'Sawano Hiroyuki', 'Deepeche Mode'];

        const randomIndex = this.#getRandomInt(trackNames.length);
        return [trackNames[randomIndex], trackAuthors[randomIndex]];
    }

    async getPredictedTrack(history){
        return await this.getRandomMusic();
    }
    async getTrackFile(music){
        return 'files/Animal - The YD.mp3'
    }
}

export class RestMusicApi extends IMusicApi{
    async getAllMusicGenres(){
        return await SendReq({url: `${SERVER_ROUTE}/music/select_all_genres`});
    }
    async getRandomMusic(){
        if(!this.genres) this.genres = await this.getAllMusicGenres()
        return await SendReq({url: `${SERVER_ROUTE}/music/get_random_music`, data: this.genres, type: 'POST'});
    }
    async getPredictedTrack(user_id){
        return await SendReq({url: `${SERVER_ROUTE}/music/get_predicted_track`, type: 'POST', data: {user_id: user_id}});
    }
    async getTrackFile(music){
        const url = await GetUrlToDownload({url: `${SERVER_ROUTE}/service/get_track_file/`, file: `${music.trackName} - ${music.trackAuthor}`});
        return url
    }
    async getAllTracksUserHistory(user_id){
        return await SendReq({url: `${SERVER_ROUTE}/history/get_all_tracks_user_history`, type: 'POST', data: {user_id: user_id}});
    }
}