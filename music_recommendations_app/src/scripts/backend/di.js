import { VoidMusicApi } from "./music";
import { VoidUserApi } from "./user";

const DI = {
    userApi: new VoidUserApi(),
    musicApi: new VoidMusicApi()
}

export default DI;