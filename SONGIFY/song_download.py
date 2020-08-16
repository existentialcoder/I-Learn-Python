import requests
import os.path
import webbrowser
import time
import tkinter as tk
from functools import partial
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class SONG_DOWNLOAD:
    def __init__(self):
        window_root = self.initialize_window()
        self.render_logo_and_greeting(window_root)
        self.render_song_search(window_root)
        window_root.mainloop() 

    def render_song_search(self, window_root):
        song_name = tk.Entry(window_root,
              width = 25,
              bg = 'white', 
              fg = 'black',
              border=0,
              font = 'Verdana 13')

        song_name.pack()
        download_button = tk.Button(window_root,
                                text='DOWNLOAD',
                                border=0,
                                highlightbackground='blue',
                                command=lambda:self.download_user_song(song_name, window_root)
                            )

        download_button.place(x = 160, y = 250)

    def display_label(self, window_root, message, side="bottom", size = 15, isBold = True):
        tk.Label(window_root, 
                    justify=tk.LEFT,
                    padx = 10, 
                    text=message.upper(),
                    font = 'Verdana {} bold'.format(size) if isBold 
                            else 'Verdana {}'.format(size),
                    fg='white',
                    bg='tomato').pack(side=side)
        
    
    def render_logo_and_greeting(self, window_root):
        self.logo = tk.PhotoImage(file="music_cutie.gif")
        tk.Label(window_root, image = self.logo ).pack(side = 'top')
        app_text = 'Download any song in seconds...'
        self.display_label(window_root, app_text, 'top')
        
    
    def initialize_window(self):
        root = tk.Tk() 
        root.title('SONGIFY')
        root.geometry('400x400')
        root.resizable(0, 0)
        root.configure(background = 'tomato')
        return root

    def get_song_name(self):
        song_name = input('Enter a song name: ')
        return song_name

    def retrieve_song_results(self, song_name):
        song_results = requests.get('https://youtube.com/results?search_query=' + song_name)
        song_results = song_results.content
        return song_results


    def retrieve_target_song(self, song_results):
        soup = BeautifulSoup(song_results, 'html.parser')
        songs = soup.findAll('div', {'class': 'yt-lockup-video'})
        song = songs[0].contents[0].contents[0].contents[0]
        return song


    def initialise_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        bot = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        return bot

    def run_chrome_driver(self, bot, target_song):
        song_link = 'https://www.youtube.com' + target_song['href']
        youtube_to_mp3 = 'https://ytmp3.cc/'
        
        bot.get(youtube_to_mp3)
        search_box = bot.find_elements_by_id('input')[0]
        search_box.send_keys(song_link)
        search_box.send_keys(Keys.RETURN)

    def complete_download(self, bot, window_root):
        time.sleep(2)
        links = bot.find_elements_by_tag_name('a')
        for i in links:
            if i.get_attribute('text') == 'Download':
                try:
                    webbrowser.open(i.get_attribute('href'))
                    time.sleep(3)
                    return bot.quit()
                except:
                    return bot.quit()

    
    def download_user_song(self, song_name, window_root):
        if len(song_name.get()) == 0:
            return self.display_label(window_root, 'Please enter a valid song',
             'bottom', 10, False)
        song_results = self.retrieve_song_results(song_name.get())
        target_song = self.retrieve_target_song(song_results)
        bot = self.initialise_chrome_driver()
        self.run_chrome_driver(bot, target_song)
        self.complete_download(bot, window_root)

song_download = SONG_DOWNLOAD()
