import requests 
from bs4 import BeautifulSoup
from os import mkdir
from os.path import exists

class SongDownloader:
    LINK = 'https://rus.hitmotop.com/search'
    
    def __init__(self, directory:str):
        self.__directory = directory
        
    def get_filename_track(self, song_name:str, artist:str) -> str:
        return f'{song_name}_{artist}.mp3'

    def download_song(self, song_name:str, artist:str):
        full_song_name = f'{song_name} - {artist}'
        filename = f'{self.__directory}/{full_song_name}.mp3'
        
        if exists(filename): return filename
        
        to_link_name = full_song_name.replace(' ', '+')
        req_url = f'{self.LINK}?q={to_link_name}'
        
        r = requests.get(req_url)
        html = r.content
        soup = BeautifulSoup(html, 'html.parser')
        btns = soup.find_all('a', class_='track__download-btn')
        links = [btn['href'] for btn in btns]
        
        if not links:
            print(req_url) 
            print("Нет треков")
            return None
        
        r = requests.get(links[0])
        
        
        if not exists(self.__directory): mkdir(self.__directory)
        
        with open(filename, 'wb') as f:
            f.write(r.content)
            
        return filename