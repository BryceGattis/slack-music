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

## AWS

We're currently using AWS to host our database (for storing Access Tokens) as there is no free database tier on 
DigitalOcean.

To begin, you must set up an AWS configuration file, to set the default region. This file should exist at 
`~/.aws/config`. The file will look something like this:

```angular2html
[default]
region=us-east-1
```

Next, you need to set up the credentials file at `~/.aws/credentials`. The file will look like this.

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

After creating this file, you should be able to interact with our DB instance.

## Spotify

You will need to create an App inside of Spotify as well, so we can make API requests to Spotify.

Note: Auth for this seems rather strange, where you MUST open a link in your browser after attempting a request once?
Could use another look at this.

1. Go to the [Spotify developer dashboard](https://developer.spotify.com/dashboard)
2. Create an app called `Slack Music`.


## Developer Note:

Slash commands require a cloud server to respond to requests (ex. AWS / GCP etc.).

Planning on using on-demand functions for now rather than a full on server.

Going to attempt to use DigitalOcean for now since they have a lot of free resources you can use.

[Apparently](https://www.digitalocean.com/community/questions/do-functions-logging)
DigitalOcean Functions invoked via the web (in our case via Slack) don't keep their activation records.
In order to deal with this, I am currently using Papertrail to keep track of the logs that are produced by the function
invocations.
