# Used to get credentials in env
import os
from pathlib import Path
# Used to manipulate dataframes
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv

from utils.data_processing import (
    get_all_saved_tracks,
    get_artist_info,
    get_tracks_info,
    get_albums_info
)

def load_spotify_credentials():
    '''
    Function that returns spotify credential 
    to access spotify API
    '''

    # Load the credentials required to access
    # Spotify API
    env_path = Path("..") / ".env"
    load_dotenv(dotenv_path=env_path)

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")

    if os.path.exists(".cache-my-music-app"):
        os.remove(".cache-my-music-app")

    # Create the OAuth object
    sp_oauth = SpotifyOAuth(
        client_id=client_id,client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=["user-top-read", "user-library-read", "playlist-read-private"],
        cache_path=".cache-my-music-app"
        )
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    return sp

def get_additional_info(data,identifier,client):
    '''
    Function that uses Spotify API to 
    extract additional info: track,album,
    artist
    '''

    additional_info = pd.DataFrame()
    id_lst = []

    if identifier == 'track':
        id_lst  = data['track_id'].unique().tolist()
        additional_info = get_tracks_info(client,id_lst)
    elif identifier == 'album':
        id_lst  = data['album_id'].unique().tolist()
        additional_info = get_albums_info(client,id_lst)
    elif identifier == 'artist':
        additional_info = get_artist_info(client,data)
    else:
        raise ValueError(f'No such identifier: {identifier}!')

    return additional_info

class DataBuilder:
    '''
    Wrapper class that geenrates 
    final dataframes to be used in 
    Dashboard
    '''

    def __init__(self,tracks,albums,artists,client):
        self.tracks = tracks
        self.albums = albums
        self.artists = artists
        self.client = client

    def remove_duplicated_columns(self,data1,data2,column_lst,join_method,suffix = '_dup'):
        '''
        tracks,albums,artists data may have 
        columns that are repeated,suffix
        identifies these duplciates & 
        eliminate repeated information in 
        final dataframe
        '''

        data_cleaned = (
            data1.merge(
                data2,how = join_method,
                on  = column_lst,suffixes=('',suffix)
            )
        )

        data_cleaned = data_cleaned.loc[:,~data_cleaned.columns.str.endswith(suffix)]


        return data_cleaned

    def generate_dashboard_data(self):
        '''
        Function that process available 
        spotify data to create data to 
        be used by dashboard
        '''
        # Get additional info for tracks
        track_info = get_additional_info(self.tracks,'track',self.client)
        track_merged = self.remove_duplicated_columns(self.tracks,track_info,['track_id'],'inner')

        # Get album information
        track_album_merged = self.remove_duplicated_columns(
            track_merged,self.albums,
            ['album_id'],'left'
            )
        
        # Get artist information
        dashboard = self.remove_duplicated_columns(
            track_album_merged,self.artists,
            ['artist_id'],'left'
            )

        return dashboard




if __name__ == '__main__':
    # Generate Spotify Client
    sp_client = load_spotify_credentials()
    # Generate track,album,artist data
    # from user saved songs on Spotify
    track_data = get_all_saved_tracks(sp_client)
    album_data = get_additional_info(track_data,'album',sp_client)
    artist_data = get_additional_info(track_data,'artist',sp_client)

    # Initialize DataBuilder class
    data_builder = DataBuilder(track_data,album_data,artist_data,sp_client)
    dashboard_data = data_builder.generate_dashboard_data()
    dashboard_data.to_csv('results.csv')