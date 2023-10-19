from flask import jsonify, request
from spotipy import Spotify
import numpy as np
from sklearn.cluster import KMeans


class Playlists:
    def __init__(self, sp: Spotify):
        self.sp = sp


    def displayPlaylists(self):
        '''
        Retrieves user's playlists from Spotify API
        '''
        page = request.args.get('page', default=0, type=int)
        displayLimit = 3
        playlists = self.sp.current_user_playlists(limit=displayLimit, offset=page * displayLimit)

        total = len(playlists['items'])
        results = {'playlists': [], 'total': total}

        for n in range(total):
            playlist = {'id': playlists['items'][n]['id'],
                        'name': playlists['items'][n]['name'],
                        'image': playlists['items'][n]['images'][0]['url']}
            
            results['playlists'].append(playlist)

        return jsonify(results)
    

    def processPlaylist(self, playlistID: str):
        '''
        Acquire the audio features of all the tracks in a given playlist
        '''
        playlist = self.sp.playlist(playlistID)

        audioFeatures = self.sp.audio_features(tracks=[t['track']['id'] for t in playlist['tracks']['items']])
        features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']
        
        return np.array([[audio[f] for f in features] for audio in audioFeatures])
    



    def categorizeTracks(self, vectorArray):
        '''
        Organize the array of audio-feature vectors into clusters
        '''
        kVals = [2, 4, 6, 8, 10]

        features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']
        return