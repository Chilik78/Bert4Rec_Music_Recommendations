from fastapi import APIRouter
from fastapi.responses import FileResponse
from server.api_models.music import DownloadMusic
from services import db, gd, rs, sd

service_router = APIRouter()

@service_router.post('/get_track_file/{name_file}')
def get_track_file(name_file: str) -> FileResponse:
    track = name_file.split(' - ')
    track_path = sd.download_song(track[0], track[1])
    if not track_path: return
    return FileResponse(path=track_path, filename=sd.get_filename_track(track[0], track[1]), headers={'Access-Control-Allow-Origin': '*'})

@service_router.post('/relearn_net')
def relearn_net_route(num_train_steps = None) -> bool:
    data = db.getAllRecordsTable('convhistory')
    
    user_ids = []
    list_music_ids = []
    
    for item in data:
        if item[0] not in user_ids:
            user_ids.append(item[0])
    
    for user_id in user_ids:
        music_ids = []
        for item in data:
            if item[0] == user_id:
                music_ids.append(item[2])
        list_music_ids.append(music_ids)
    try:
        gd.change_train(user_ids, list_music_ids)
        gd.gen_files_for_train()
        rs.do_train(num_train_steps=num_train_steps)
        return True
    except Exception as e:
        print(e)
        return False