#Jason K on 07/08/22 -- Didn't like iTunes anymore, so I made this! Thought i'd share my beginner spaghetti code.
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# For this to work properly, you will need to create an application at https://developer.spotify.com/dashboard/applications

#From there, you will need to set only one setting within your app for this to work.

# Set Redirect URIs to http://localhost:8888/callback/
#  - This just sets the redirect URI to your local machine, when you first run the python script it will ask you to authenticate your account if you've done everything correct!

cid = '' # Obtain this value from your created App's Client ID field
secret = '' # Obtain this value from your created App's Client Secret field
username = '' # Obtain this under the username field inside your spotify profile at https://www.spotify.com/us/account/overview/
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

song_list = ["Resonance"] 
artist_list = ["Home"]

uri_list = []
failed_songs = []

def querySong(song_name,artist_name):

    results = spotify.search(q="artist:" + artist_name + " track:" + song_name, type="track") # Searches for spotify song with API query

    try: # If there is no error thrown when trying to find the song result, then add to uri list, if not add to failed songs list
        song_uri = results['tracks']['items'][0]['uri']
        uri_list.append(song_uri)
    except:
        failed_songs.append("- "+str(song_name) + " by " + str(artist_name))

for songsIndex in range(0,len(song_list)):
    querySong(song_list[songsIndex],artist_list[songsIndex])
    
    if songsIndex % 100 == 0 and songsIndex != 0: # Had to have a separate spotify request auth, as it is capped at 100 tracks/request
        scope = 'playlist-modify-private'
        token = util.prompt_for_user_token(username, scope,client_id=cid, client_secret=secret,redirect_uri='http://localhost:8888/callback/')

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            new_playlist = sp.user_playlist_create(username,'Imported Playlist ' +str(int(songsIndex/100)),public=False)
            print(str(len(uri_list)) + " songs loaded. ")
            results = sp.user_playlist_add_tracks(username, new_playlist['id'], uri_list)
            uri_list.clear()
        else:
            print("Can't get token for", username)

print("Failed to import following songs: \n")
for failedSong in failed_songs:
    print(failedSong)
