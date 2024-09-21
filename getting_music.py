import requests 
from bs4 import BeautifulSoup
from os import mkdir
from os.path import exists

def download_song(song_name:str, artist:str, directory:str):
    LINK = 'https://rus.hitmotop.com/search'
    
    full_song_name = f'{song_name} - {artist}'
    to_link_name = full_song_name.replace(' ', '+')
    req_url = f'{LINK}?q={to_link_name}'
    
    r = requests.get(req_url)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    btns = soup.find_all('a', class_='track__download-btn')
    links = [btn['href'] for btn in btns]
    
    if not links:
        print(req_url) 
        print("Нет треков")
        return

    r = requests.get(links[0])
    filename = f'{directory}/{full_song_name}.mp3'
    
    if not exists(directory): mkdir(directory)
    
    with open(filename, 'wb') as f:
        f.write(r.content)
        
if __name__ == '__main__':
    song_name = 'Delayed Because of Accident'
    artist = 'Andreas Rönnberg'
    directory = 'musics'
    download_song(song_name, artist, directory)