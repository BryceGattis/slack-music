import json
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

LOG = logging.getLogger(__name__)


def main(event):
    logging.basicConfig(level=logging.INFO)
    payload_str = event['payload']
    payload = json.loads(payload_str)
    actions = payload['actions']
    scope = "playlist-modify-public,playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(open_browser=False, scope=scope))
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
    sp.playlist_add_items('<playlist_id>', track_uris)
    return {
        "statusCode": 200,
    }
