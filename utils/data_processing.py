'''
Manipulate data in dataframes for analysis
'''
import pandas as pd

def extract_top_tracks_data(spotify_client,time_range)->pd.DataFrame:
    '''
    Convert JSON file extracted from spotify 
    to dataframe for analysis
    '''
    top_tracks_json = spotify_client.current_user_top_tracks(limit=50, time_range=time_range)
    track_list = []

    for item in top_tracks_json['items']:
        track_info = {
            'track_name':item['name'],
            'artist_name': item['artists'][0]['name'],
            'album_name': item['album']['name'],
            'album_id': item['album']['id'],
            'release_date': item['album']['release_date'],
            'popularity': item['popularity'],
            'duration_ms': item['duration_ms'],
            'explicit':item['explicit'],
            'track_id': item['id']
        }
        track_list.append(track_info)

    data = pd.DataFrame(track_list)
    data['duration_min'] = data['duration_ms']/60000
    data['release_date'] = pd.to_datetime(data['release_date'])

    return data

def extract_top_artist_data(spotify_client,time_range)->pd.DataFrame:
    '''
    Convert JSON file extracted from Spotify
    to dataframe for analysis
    '''
    top_artist_json = spotify_client.current_user_top_artists(limit = 50,time_range = time_range)
    artist_list = []
    for item in top_artist_json['items']:
        artist_info = {
            'artist_name':item['name'],
            'popularity':item['popularity'],
            'genres': ', '.join(item['genres']),
            'artist_id': item['id'],
            'followers': item['followers']['total'],
            # Gets the largest image if exists
            'image_url': item['images'][0]['url'] if item['images'] else None
        }
        artist_list.append(artist_info)
    data = pd.DataFrame(artist_list)
    return data

def get_albums_info(spotify_client,album_ids)->pd.DataFrame:
    '''
    Extract album information from top songs 
    '''
    album_data = []

    for i in range(0,len(album_ids),20):
        # Spotify API limit requests to 20 albums per call
        batch = album_ids[i:i+20]
        albums = spotify_client.albums(batch)['albums']
        for album in albums:
            album_info = {
        'album_id': album['id'],
        'album_name': album['name'],
        'release_date': album['release_date'],
        'total_tracks': album['total_tracks'],
        'label': album.get('label', ''),
        'popularity': album.get('popularity'),
        'album_type': album['album_type'],
        'external_url': album['external_urls']['spotify'],
        'album_uri': album['uri'],
        'release_date_precision': album['release_date_precision'],
        # List of images with varying sizes
        'images': [image['url'] for image in album['images']] if album['images'] else [],
        # If else is used to check if genres is not blank
        'genres': ', '.join(album['genres']) if 'genres' in album else '',
        # Add artist names
        'artists': ', '.join([artist['name'] for artist in album['artists']]),
        # Extract track IDs
        'track_ids': [track['id'] for track in album['tracks']['items']],  # Extract track IDs
        # Get available markets for the album
        'available_markets': album.get('available_markets', []),
        }
            album_data.append(album_info)
    data = pd.DataFrame(album_data)
    return data

def get_tracks_info(spotify_client,track_ids)->pd.DataFrame:
    '''
    Extract additional information on top tracks
    '''
    track_data = []

    for i in range(0,len(track_ids),50):
        batch = track_ids[i:i+50]
        tracks = spotify_client.tracks(batch)['tracks']
        for track in tracks:
            track_info = {
                'track_id':track['id'],
                'track_name':track['name'],
                'popularity':track['popularity'],
                'explicit':track['explicit'],
                'artist_id':track['artists'][0]['id'],
                'album_id':track['album']['id'],
                # URL provide 30s preview of track
                'preview_url':track.get('preview_url',''),
                # URL of track page in spotify
                'track_url':track['external_urls']['spotify'],
                # External Identifier to track songs globally
                'track_external_id':track['external_ids'].get('isrc',''),
                # Check whether track saved in user device
                'is_local':track['is_local'],
            }
            track_data.append(track_info)

    track_data = pd.DataFrame(track_data)
    return track_data
