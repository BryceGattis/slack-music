import logging

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

LOG = logging.getLogger(__name__)


def main(args):
    logging.basicConfig(level=logging.INFO)
    LOG.info(args)
    LOG.info(type(args))
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    resp = sp.search("A song name", type="track", limit=1)
    if resp.get('error'):
        return {
            "body": {
                "statusCode": resp['error']['status'],
                "text": resp['error']['message']
            }
        }
    song_names = []
    for track in resp['tracks']['items']:
        song_names.append(track['name'])
    blocks_data = []
    for song_name in song_names:
        block_data = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": song_name
            }
        }
        blocks_data.append(block_data)
    return {
        "body": {
            "text": "Hello World",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*It's 80 degrees right now.*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Partly cloudy today and tomorrow"
                    }
                }
            ],
            "response_type": "ephemeral",
        },
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        }
    }
