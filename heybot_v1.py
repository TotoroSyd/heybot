# This is the Hello World version

# Before running Flask app and Server:
# A. turn on Python virtual environment: source path/to/env../activate
# source /Users/phoebengg/Documents/Web_Dev_Generation/heybot/heybot/env/bin/activate

# B. export these environment variables in the terminal
# 1. export SLACK_BOT_TOKEN='your bot user access token here'
# 2. export SLACK_SIGNING_SECRET='your bot secret token here'

# After exporting variables:
# C. export FLASK_APP before "flask run"
# export FLASK_APP=<file_name>.py

# D. turn on server with ngrok
# /Users/phoebengg/Downloads/Application/ngrok http 5000
# port number '5000' got after running 'flask run'

# Code starts from here
# import dependencies to obtain the environment variable values
import os
import slack
from slackeventsapi import SlackEventAdapter
import json
from flask import Flask, request, jsonify

# Import environment var by retrieving exported token https://slack.dev/python-slackclient/auth.html
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

# create the Flask server
app = Flask(__name__)

# Initialize a Slack Event Adapter for receiving actions via the Events API
slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, '/slack/events', app)

# Instantiate a Web API client
slack_web_client = slack.WebClient(
    token=os.environ['SLACK_BOT_TOKEN'], timeout=30)

# Routing


@app.route('/', methods=['POST', 'GET'])
def reply():
    # print(request.headers)
    # print(request.data)
    # print(request.args)
    # print(request.form)
    # print(request.endpoint)
    # print(request.method)
    # print(request.remote_addr)
    # get ready to receive and respond HTTP POST request from Slack to verify bot's endpoint URL
    if request.method == 'POST':
        challenge_parse = (json.loads(request.data))['challenge']
        # print(challenge_parse)
        # respond URL verification from Slack with 'challenge' value
        response = {"challenge": challenge_parse}
        return response, 200

# When a user sends a DM, the event type will be 'message'.
# Link the message callback to the 'message' event.
# Choose to use Event API (handled by SlackEventAdapter) instead of RTM API. Working with SlackEventAdapter seems easier :)
# Because "The RTM API is only recommended if you're behind a firewall and cannot receive incoming web requests from Slack."


@slack_events_adapter.on("message")
def say_hello(event_data):
    print('EVENT_DATA')
    print(event_data)
    message = event_data['event']

    # if the incoming message contains "hello" NOT CASE SENSITIVE, then respond with a designed message
    # "subtype" doesnt help to filter bot's message event and user's message event
    if message.get('bot_id') is None and 'hello' in ((message.get('text')).lower()):
        channel_id = message['channel']
        user = message['user']
        message = "Hello <@%s>! :tada:" % user
        slack_web_client.chat_postMessage(channel=channel_id, text=message)
    else:
        return


# Error events


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=5000)
