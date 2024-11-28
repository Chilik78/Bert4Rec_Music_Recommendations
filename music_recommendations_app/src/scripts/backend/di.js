import { VoidMusicApi, RestMusicApi } from "./music";
import { VoidUserApi } from "./user";

const DI = {
    userApi: new VoidUserApi(),
    musicApi: new RestMusicApi()
}

export default DI;