import json
import logging
import os
from typing import Dict, Optional

import boto3
import spotipy
from spotipy.cache_handler import CacheHandler
from spotipy.oauth2 import SpotifyOAuth

LOG = logging.getLogger(__name__)
OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"


class DynamoCacheHandler(CacheHandler):
    def __init__(self, workspace_id: int):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('slack_music_access_tokens')
        self.workspace_id = workspace_id

    def get_cached_token(self):
        resp = self.table.get_item(
            Key={
                "workspace_id": self.workspace_id
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
                "workspace_id": self.workspace_id
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


def get_current_playlist_id() -> Optional[str]:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('slack_music_current_playlists')

    spotify_client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    resp = table.get_item(
        Key={
            "client_secret": spotify_client_secret
        }
    )
    found_entry = resp.get('Item', None)
    playlist_id = None
    if found_entry:
        playlist_id = found_entry.get('playlist_id', None)
    return playlist_id


def main(event):
    logging.basicConfig(level=logging.INFO)
    payload_str = event['payload']
    payload = json.loads(payload_str)
    workspace_id = payload['team']['id']
    actions = payload['actions']

    cache_handler = DynamoCacheHandler(workspace_id=workspace_id)
    scope = "playlist-modify-public,playlist-modify-private"
    auth_manager = SpotifyOAuth(open_browser=False, scope=scope, cache_handler=cache_handler)
    spotipy_client = spotipy.Spotify(auth_manager=auth_manager)
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
    playlist_id = get_current_playlist_id()
    if playlist_id is None:
        return {
            "statusCode": 400
        }
    spotipy_client.playlist_add_items(playlist_id, track_uris)

    return {
        "statusCode": 200,
    }
