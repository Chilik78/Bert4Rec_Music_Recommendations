import hashlib
from Bridge import Bridge
import base64
from Database import Database
brdg = Bridge()
db = Database()
# res = brdg.getAllHistory()
# print(res)
# print('------------------------------------')
# res = brdg.getUserHistory("0cd0eda4-9dd7-4adf-be49-82b242811a53")
# print(res)


res = brdg.convertAllMusicId()
#res = brdg.convertAllHistory()
print(res)