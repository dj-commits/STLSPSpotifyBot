import asyncio
import datetime
from platform import java_ver
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
playlist_link = ""
message_check = ':banger:'
intents = discord.Intents.default()
intents.message_content = True
discordClient = discord.Client(intents=intents)
messages = {}
today = datetime.date.today()
month = today.strftime("%B")
year = today.strftime("%Y")
me = creds.SP_USER_ID
message_counter = 0


def UpdateCurrentPlaylist(this_sp):
    global month
    new_today = datetime.date.today()
    if(new_today.strftime("%B") != month):
        today = datetime.date.today()
        month = today.strftime("%B")
        year = today.strftime("%Y")
        playlist_ID = CreatePlaylist(sp, f"STLSP {month} {year} Playlist")
    


def CreatePlaylist(sp, title):
    global playlist_link
    global me
    current_playlists = sp.user_playlists(sp.me()['id'])
    for i in current_playlists["items"]:
        if f"STLSP {month} {year} Playlist" in i["name"]:
            playlist_link = i['external_urls']['spotify']
            print("I just created a playlist")
            return i['id']
    user_id = sp.me()['id']
    new_playlist = sp.user_playlist_create(user_id, title)
    playlist_link = new_playlist['external_urls']['spotify']
    print("I just created a playlist")
    return new_playlist['id']
        
    
    

def AddToPlaylist(track):    
    if(CheckIfExistsInPlaylist(track)):
        sp.playlist_add_items(playlist_ID,  [track['uri']])
        print("I just added a song")
        
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
    global message_counter
    global playlist_link
    if playlist_ID == "":
        playlist_ID = CreatePlaylist(sp, f"STLSP {month} {year} Playlist" )
    if message_counter >= 50:
        message_counter = 0
        async with asyncio.timeout(10):
            await message.channel.send(f"STLSP's {month} {year} Playlist is available here: \n {playlist_link} \n")
    if f"{playlist_link}" in message.content:
        print("This is how I stop looping over myself.")
    elif 'spotify.com' in message.content:
        link = []
        for word in message.content.split():
            if 'spotify.com' in word:
                link.append(word)
        if(link):
            message_counter += 1
            for i in link:
                message_track = sp.track(i)
                messages[f'{message.id}'] = message_track


@discordClient.event
async def on_reaction_add(reaction, user):
    global sp
    global playlist_
    UpdateCurrentPlaylist(sp)
    if message_check in str(reaction):
        for i in messages:
            if f"STLSP's {month} {year} Playlist is available here: \n {playlist_link} \n" in reaction.message.content:
                break
            if i == str(reaction.message.id):
                AddToPlaylist(messages[i])
               



#TODO: handle removal of banger emoji
        

discordClient.run(creds.DC_CLIENT_TOKEN)


