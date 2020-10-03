# This is the Final Version of heybot

# Before running Flask app and Server:
# A. turn on Python virtual environment: source path/to/env../activate
# source /Users/phoebengg/Documents/Web_Dev_Generation/heybot/heybot/env/bin/activate

# B. export these environment variables in the terminal
# 1. export SLACK_BOT_TOKEN='your bot user access token here'
# 2. export SLACK_SIGNING_SECRET='your bot secret token here'
# 3. export AUTHORIZATION_TOKEN='your token to access BambooHR here"
# 4. export COMPANY_DOMAIN='your company domain you used to open BambooHR account'

# After exporting variables:
# C. export FLASK_APP before "flask run"
# export FLASK_APP=<file_name>.py

# D. turn on server with ngrok
# /Users/phoebengg/Downloads/Application/ngrok http 5000
# port number '5000' got after running 'flask run'

# Code starts from here
# import dependencies to obtain the environment variable values
from flask import Flask, request, jsonify
# from urllib.parse import parse_qs

from bamboohr import Bamboohr
from messages import Message
import os
import slack
from slackeventsapi import SlackEventAdapter
import json
import requests
# import re
# import nltk
# nltk.download()

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
    token=os.environ['SLACK_BOT_TOKEN'])


# Get employee directory
bamboohr = Bamboohr()

# Call class Message
msg = Message()

# Handle requests


@ app.route('/', methods=['POST'])
def URL_challenge_reply():
    # print(request.headers)
    # print(request.data)
    # print(request.args)
    # print(request.form)
    # print(request.endpoint)
    # print(request.method)
    # print(request.remote_addr)
    # get ready to receive and respond HTTP POST request from Slack to verify bot's endpoint URL

    challenge_parse = (json.loads(request.data))['challenge']
    # print(challenge_parse)
    # respond URL verification from Slack with 'challenge' value
    response = {"challenge": challenge_parse}
    return response, 200

# When a user sends a DM, the event type will be 'message'.
# Link the message callback to the 'message' event.
# Choose to use Event API (handled by SlackEventAdapter) instead of RTM API. Working with SlackEventAdapter seems easier :)
# Because "The RTM API is only recommended if you're behind a firewall and cannot receive incoming web requests from Slack."


@ slack_events_adapter.on("message")
def reply_user(event_data):
    # print('EVENT_DATA')
    # print(event_data)
    message = event_data['event']
    message_user = message['user']
    message_text = (message.get('text')).lower()
    channel_id = message['channel']
    expected_greetings = ['hello', 'hey', 'heybot',
                          'good day', 'g\'day', 'hi', 'what\'s up', 'morning', 'afternoon', 'good morning', 'good afternoon', 'howdy', 'help']

    # "subtype" in message_text isn't available to filter bot's messages and user's messages
    if message.get('bot_id') is None:
        # check greeting from user
        if any(greeting in message_text for greeting in expected_greetings):
            # prepare block with text and buttons to respond, convert into a JSON
            blocks = json.dumps(msg.understood_greeting(message_user))
            # reply to user
            slack_web_client.chat_postMessage(
                channel=channel_id, blocks=blocks)

        else:
            # text = "Hello <@%s>! Sorry, I'm having trouble understanding you right now." % message['user']
            text = msg.confuse(message_user)
            # reply to user
            slack_web_client.chat_postMessage(channel=channel_id, text=text)

    return "", 200
# Error events


@ slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=5000)


@ app.route('/slack/request_handler', methods=['POST', 'GET'])
def request_handler():
 # Get data from payload
    # Solution 1:
    payload = request.form  # return an ImmutableMultiDict with 1 pair
    a1 = payload['payload']  # get value of key 'payload'
    # Note that if you have single quotes as a part of your keys or values this will fail due to improper character replacement.
    # This solution is only recommended if you have a strong aversion to the eval solution.
    # convert a string (representation of a Dict)) to a Dict
    a2 = json.loads(a1)
    # Get payload type
    payload_type = a2["type"]
    # Initiate channel_id
    channel_id = ""
    # Initiate action_id
    action_id = ""

    if payload_type == "block_actions":
        # get channel_id
        channel_id = a2["channel"]["id"]
        # Get action id to track button action
        actions = a2["actions"][0]
        action_id = actions["action_id"]
    elif payload_type == "view_submission":
        # "private_metadata: {'channel_id': 'D234F5F', 'action_id': 'time_off_balance'}"
        decode_json_private_data = json.loads(a2["view"]["private_metadata"])
        # get channel_id
        channel_id = decode_json_private_data["channel_id"]
        # Get action id to track button action
        action_id = decode_json_private_data["action_id"]

    if payload_type == "block_actions":
        if action_id in ("time_off_balance", "time_off_policy"):
            # Prepare
            view = json.dumps(msg.get_employee_id_modal(channel_id, action_id))

        elif action_id == "time_off_request":
            # Prepare
            view = json.dumps(msg.get_inputs_request(channel_id, action_id))

        # Open a modal when a button is clicked using views.open (https://api.slack.com/block-kit/dialogs-to-modals)
        slack_web_client.views_open(
            view=view, trigger_id=a2["trigger_id"])

    elif payload_type == "view_submission":
        callback_id = a2["view"]["callback_id"]
        if callback_id == "employee_id_modal":
            # collect user's input (employee id)
            submission = a2["view"]["state"]["values"]["employee_id_modal_input"]["employee_id_value"]["value"]
            # validate user input
            # Todo
            report = {}
            blocks = []

            if action_id == "time_off_policy":
                report = bamboohr.time_off_policy()
                blocks = msg.answer_time_off_policy(report)
            elif action_id == "time_off_balance":
                report = bamboohr.time_off_balance(submission)
                blocks = msg.answer_time_off_balance(report)
            # reply user
            slack_web_client.chat_postMessage(
                channel=channel_id, blocks=blocks)

        elif callback_id == "inputs_request_timeoff_modal":
            # employee_id =
            # start_date =
            # end_date =
            # amount =
            # timeOffTypeId =

            # validate user input
            # # Todo
            # report = {}
            # blocks = []
            if action_id == "time_off_request":
                bamboohr.time_off_request(
                    employee_id, start_date, end_date, amount, timeOffTypeId)

                slack_web_client.chat_postMessage(
                    channel=channel_id, text="Service is coming soon")

        # close modal view immediately when user clicked Submit
        # compulsory return an empty HTTP 200 response
        # --Note: This will close the current view only. To close all view, must return ({"response_action": "clear"})
        return ({})
    return {"ok": 200}

    # Get data from payload
    # # Solution 2
    # # # request.get_data() doesnt care about the Content-type, returns a bytestring
    # # # parse_qs() returned a dict from a bytestring. This dict has 1 pair
    # payload_dict = parse_qs(request.get_data())
    # payload_dict_value_arr = payload_dict[b'payload']
    # data = payload_dict_value_arr[0]
    # datajson = json.loads(data)
    # channel = datajson["channel"]
    # print(channel)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
