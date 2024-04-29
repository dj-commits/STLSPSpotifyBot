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
    

def AddToPlaylist(link):
    # Check for song, if not in playlist, then add to playlist
    
    sp.playlist_add_items(playlist_ID, link)
    
    
    
sp = SpotifyAuthentication(creds.SP_CLIENT_ID, creds.SP_CLIENT_SECRET)
playlist_ID = r'0L8hjTMfDnWNzW95AhAmt7'
intents = discord.Intents.default()
intents.message_content = True
discordClient = discord.Client(intents=intents)

@discordClient.event
async def on_ready(self):
    print(f'Logged on as {self.user}!')
        
@discordClient.event
async def on_message(message):
    if 'spotify.com' in message.content:
        # breaks if some dumbass only types spotify.com out
        link = []
        if(message.content.count('spotify.com') > 1):
            numberOfLinks = message.content.count('spotify.com')
            while(numberOfLinks > 0):
                print(numberOfLinks)
                beginning = message.content.index('https://')
                end = message.content.index(' ')
                link.append(message.content[beginning:end])
                numberOfLinks -= 1
        else:
            link.append(message.content)
        if(link):
            AddToPlaylist(link)
        



discordClient.run(creds.DC_CLIENT_TOKEN)

