from flask import Flask, redirect, request
# from flask_cors import CORS
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


from services.playlists import Playlists


app = Flask(__name__)
# CORS(app, origins='http://localhost:3000')
app.secret_key = os.urandom(24)

load_dotenv()

sp = Spotify(auth_manager=SpotifyOAuth(client_id = os.getenv("CLIENT_ID"),
                                    client_secret = os.getenv("CLIENT_SECRET"),
                                    redirect_uri = 'http://localhost:5000/callback',
                                    scope = 'user-library-read playlist-read-private'))
library = Playlists(sp)


@app.route('/')
def index():
    '''
    Redirect the user to the Spotify Login of not logged in
    '''
    authURL = sp.auth_manager.get_authorize_url()
    return redirect(authURL)


@app.route('/callback')
def callback():
    '''
    Handle the callback URL after user authentication
    '''
    sp.auth_manager.get_access_token(request.args.get('code'))
    return 'Authenticated! You can now close this window.'


@app.route('/api/playlists', methods=['GET'])
def playlists():
    '''
    Return JSON response to front end
    '''
    # library.processPlaylist('4Okw19lawtHb5lNZkATOfr')
    return library.displayPlaylists()


if __name__ == '__main__':
    app.run()