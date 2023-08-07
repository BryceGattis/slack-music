import logging

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

LOG = logging.getLogger(__name__)


def main(event):
    logging.basicConfig(level=logging.INFO)
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    resp = sp.search(event['text'], type="track", limit=3)
    if resp.get('error'):
        return {
            "body": {
                "statusCode": resp['error']['status'],
                "text": resp['error']['message']
            }
        }
    track_infos = []
    for track in resp['tracks']['items']:
        track_info = dict()
        track_info['track_id'] = track['id']
        track_info['track_name'] = track['name']
        track_info['album_name'] = track['album']['name']
        track_info['thumbnail'] = track['album']['images'][0]
        track_info['artist'] = track['artists'][0]['name']
        track_infos.append(track_info)
    blocks = []
    for track_info in track_infos:
        text = f"*{track_info['track_name']}*\n"
        text += f"*Artist:* {track_info['artist']}\n"
        text += f"*Album:* {track_info['album_name']}"
        track_section = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            },
            "accessory": {
                "type": "image",
                "image_url": track_info['thumbnail']['url'],
                "alt_text": "Album Thumbnail"
            }
        }
        blocks.append(track_section)
        add_button_section = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Add to playlist"
                    },
                    "style": "primary",
                    "value": track_info['track_id'],
                    "action_id": "add_song_to_playlist"
                },
            ]
        }
        blocks.append(add_button_section)
    return {
        "body": {
            "text": "Hello World",
            "blocks": blocks,
            "response_type": "ephemeral",
        },
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        }
    }
