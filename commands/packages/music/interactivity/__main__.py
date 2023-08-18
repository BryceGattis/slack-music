import json
import logging
import os
from typing import Dict

import boto3
import spotipy
from spotipy.cache_handler import CacheHandler
from spotipy.oauth2 import SpotifyOAuth

LOG = logging.getLogger(__name__)
OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"


class DynamoCacheHandler(CacheHandler):
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('slack_music_access_tokens')
        self.spotify_client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    def get_cached_token(self):
        resp = self.table.get_item(
            Key={
                "client_secret": self.spotify_client_secret
            }
        )
        found_entry = resp.get('Item', None)
        token_info = None
        if found_entry:
            token_info = found_entry.get('token_info', None)
        return token_info

    def save_token_to_cache(self, token_info: Dict[str, str]):
        self.table.update_item(
            Key={
                "client_secret": self.spotify_client_secret
            },
            UpdateExpression='SET #access_token=:access_token, #expires_at=:expires_at, #expires_in=:expires_in, #refresh_token=:refresh_token, #scope=:scope, #token_type=:token_type',
            ExpressionAttributeNames={
                "#access_token": "token_info.access_token",
                "#expires_at": "token_info.expires_at",
                "#expires_in": "token_info.expires_in",
                "#refresh_token": "token_info.refresh_token",
                "#scope": "token_info.scope",
                "#token_type": "token_info.token_type"
            },
            ExpressionAttributeValues={
                ':access_token': token_info['access_token'],
                ':expires_at': token_info['expires_at'],
                ':expires_in': token_info['expires_in'],
                ':refresh_token': token_info['refresh_token'],
                ':scope': token_info['scope'],
                ':token_type': token_info['token_type']
            }
        )


def main(event):
    logging.basicConfig(level=logging.INFO)
    payload_str = event['payload']
    payload = json.loads(payload_str)
    actions = payload['actions']
    scope = "playlist-modify-public,playlist-modify-private"
    auth_manager = SpotifyOAuth(open_browser=False, scope=scope, cache_handler=DynamoCacheHandler())
    sp = spotipy.Spotify(auth_manager=auth_manager)
    track_ids_to_add = []
    for action in actions:
        if action['action_id'] != 'add_song_to_playlist':
            continue
        track_id = action['value']
        track_ids_to_add.append(track_id)
    track_uris = []
    for track_id in track_ids_to_add:
        track_uri = f'spotify:track:{track_id}'
        track_uris.append(track_uri)
    sp.playlist_add_items('<Playlist ID>', track_uris)
    return {
        "statusCode": 200,
    }