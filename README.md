# slack-music
Slack music bot that requires unanimous decisions

## Requirements

- Python 3.11.x
- doctl (Digital Ocean CLI)

## Environment Setup

1. Install the above requirements.
2. Create a virtual environment and install requirements.txt.

## Digital Ocean

We will be using the doctl command line interface with DigitalOcean, so we can upload our commands to Digital Ocean and
test them easily.

1. Go to the [Digital Ocean Token Page](https://cloud.digitalocean.com/account/api/tokens) and set up a Personal Access
   Token. I'm currently setting the token to have no expiry date. I *think* we need write permissions for this token?
2. `doctl auth init` to connect doctl to your Digital Ocean account.
3. `doctl serverless init` to prepare the ./commands directory for deployment to Digital Ocean.
4. `doctrl serverless install` to support deploying to serverless Digital Ocean instance.
5. `doctrl serverless connect` to connect to a functions namespace.
6. `doctl serverless deploy --remote-build D:/Code/slack-music/commands` to deploy to Digital Ocean.

## Spotify

You will need to create an App inside of Spotify as well, so we can make API requests to Spotify.

Note: Auth for this seems rather strange, where you MUST open a link in your browser after attempting a request once?
Could use another look at this.

1. Go to the [Spotify developer dashboard](https://developer.spotify.com/dashboard)
2. Create an app called `Slack Music`.


## Developer Note:

Slash commands require a cloud server to respond to requests (ex. AWS / GCP etc.).

Planning on using on-demand functions for now rather than a full on server.

Going to attempt to use DigitialOcean for now since they have a lot of free resources you can use.
