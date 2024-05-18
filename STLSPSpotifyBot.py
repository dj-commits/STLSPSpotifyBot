from datetime import date
from math import e
from tkinter.messagebox import CANCEL
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import creds
import discord


    

def SpotifyAuthentication(id, secret):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= id, client_secret=secret, redirect_uri='http://127.0.0.0:9090', scope="playlist-modify-public playlist-modify-private"))
    return sp

# variables  
sp = SpotifyAuthentication(creds.SP_CLIENT_ID, creds.SP_CLIENT_SECRET)
playlist_ID = ""
message_check = ':banger:'
intents = discord.Intents.default()
intents.message_content = True
discordClient = discord.Client(intents=intents)
messages = {}
month = date.month
year = date.year

def CreatePlaylist(sp, title):
    current_playlists = sp.user_playlists(sp.me()['id'], fields="name")
    for i in current_playlists:
        if i["name"] == f"STLSP {month} {year} Playlist":
            return i['id']
        else:
            user_id = sp.me()['id']
            return sp.user_playlist_create(user_id, title)['id']
        
    
    

def AddToPlaylist(track):
    # Check that playlist exists, if so, check if duplicate, if not, add to playlist
    
    if(CheckIfExistsInPlaylist(track)):
        sp.playlist_add_items(playlist_ID,  [track['uri']])
        
def CheckIfExistsInPlaylist(track):
    items = sp.playlist_items(playlist_ID)
    track = sp.track(track['id'])
    for i in items['items']:
        if i['track']['uri'] == track['uri']:
            return False
    return True
    


@discordClient.event
async def on_ready(self):
    print(f'Logged on as {self.user}!')
        
@discordClient.event
async def on_message(message):
    global playlist_ID
    if playlist_ID == "":
        playlist_ID = CreatePlaylist(sp, f"STLSP {month} {year} Playlist" )
    if 'spotify.com' in message.content:
        link = []
        for word in message.content.split():
            if 'spotify.com' in word:
                link.append(word)
        if(link):
            for i in link:
                message_track = sp.track(i)
                messages[f'{message.id}'] = message_track


@discordClient.event
async def on_reaction_add(reaction, user):
    if message_check in str(reaction):
        for i in messages:
            if i == str(reaction.message.id):
                AddToPlaylist(messages[i])
               



#TODO: handle removal of banger emoji, archival and creation of playlist
        

discordClient.run(creds.DC_CLIENT_TOKEN)


