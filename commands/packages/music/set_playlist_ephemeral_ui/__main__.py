import logging
from typing import Dict, List

import requests

LOG = logging.getLogger(__name__)


def _get_missing_playlist_blocks() -> List[Dict[str, str]]:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Playlist not specified for current workspace. Please specify the playlist ID below and click 'Done'."
            }
        },
        {
            "type": "input",
            "block_id": "playlist_setter_block",
            "element": {
                "type": "plain_text_input",
                "action_id": "playlist_id"
            },
            "label": {
                "type": "plain_text",
                "text": "Playlist ID",
                "emoji": False
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Done"
                    },
                    "style": "primary",
                    "action_id": "set_workspace_playlist"
                },
            ]
        }
    ]
    return blocks


def main(event):
    logging.basicConfig(level=logging.INFO)
    response_url = event['response_url']
    blocks = _get_missing_playlist_blocks()
    data = {
        "text": "UI to provide playlist name.",
        "blocks": blocks
    }
    requests.post(url=response_url, json=data)

    return {
        "body": {
            "text": f"Blocks sent to URL: {response_url}"
        },
        "statusCode": 200,
    }
