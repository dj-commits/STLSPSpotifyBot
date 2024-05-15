from math import e
from tkinter.messagebox import CANCEL
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import creds
import discord


        

def SpotifyAuthentication(id, secret):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= id, client_secret=secret, redirect_uri='http://127.0.0.0:9090', scope="playlist-modify-public playlist-modify-private"))
    return sp


def CreatePlaylist(sp, title):
    user_id = sp.me()['id']
    return sp.user_playlist_create(user_id, title)['id']
    

def AddToPlaylist(track):
    # Check for song, if not in playlist, then add to playlist
    
    if(CheckIfExistsInPlaylist(track)):
        sp.playlist_add_items(playlist_ID,  [track['uri']])
        
def CheckIfExistsInPlaylist(track):
    items = sp.playlist_items(playlist_ID)
    track = sp.track(track['id'])
    for i in items['items']:
        if i['track']['uri'] == track['uri']:
            return False
    return True
    
    
sp = SpotifyAuthentication(creds.SP_CLIENT_ID, creds.SP_CLIENT_SECRET)
playlist_ID = r'0L8hjTMfDnWNzW95AhAmt7'
message_check = ':banger:'
intents = discord.Intents.default()
intents.message_content = True
discordClient = discord.Client(intents=intents)
messages = {}
playlist_titles = {"January" : "STLSP January 2025 Playlist",
                   "February" : "STLSP February 2025 Playlist",
                   "March" : "STLSP March 2025 Playlist",
                   "April" : "STLSP April 2025 Playlist",
                   "May" : "STLSP May 2024 Playlist",
                   "June" : "STLSP June 2024 Playlist",
                   "July" : "STLSP July 2024 Playlist",
                   "August" : "STLSP August 2024 Playlist",
                   "September" : "STLSP September 2024 Playlist",
                   "October" : "STLSP October 2024 Playlist",
                   "November" : "STLSP November 2024 Playlist",
                   "December" : "STLSP December 2024 Playlist",}


@discordClient.event
async def on_ready(self):
    print(f'Logged on as {self.user}!')
        
@discordClient.event
async def on_message(message):
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

