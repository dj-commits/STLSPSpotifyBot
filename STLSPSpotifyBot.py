from spotipy import *

def SpotifyAuthentication():
    sp = spotipy.Spotyfy(auth_manager=SpotifyOAuth(scope="user-library-read"))
    return sp