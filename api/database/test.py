from Bridge import Bridge
brdg = Bridge()

res = brdg.getAllHistory()
print(res)
print('------------------------------------')
res = brdg.getUserHistory("fcdf7d44-8d05-4489-a0f5-624695a6ca9a")
print(res)


