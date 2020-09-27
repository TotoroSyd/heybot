# This is sample payloads

# payload from button clicked
{
    "type": "block_actions",
    "user": {
        "id": "U01AZ88AQQ4",
        "username": "phoebe.ngsyd",
        "name": "phoebe.ngsyd",
        "team_id": "T01B5M3VC1X"
    },
    "api_app_id": "A01BGTV24LQ",
    "token": "RFEwDETALFMJkphCasIfOUZT",
    "container": {
        "type": "message",
        "message_ts": "1600857119.015400",
        "channel_id": "D01ACC2E8S3",
        "is_ephemeral": False
    },
    "trigger_id": "1388105719492.1379717998065.9bc163894734c1f415a2c504e81dec91",
    "team": {
        "id": "T01B5M3VC1X",
        "domain": "heybot-workspace"
    },
    "channel": {
        "id": "D01ACC2E8S3",
        "name": "directmessage"
    },
    "message": {
        "bot_id": "B01AQ1SN737",
        "type": "message",
        "text": "This content can't be displayed.",
        "user": "U01BGV723R6",
        "ts": "1600857119.015400",
        "team": "T01B5M3VC1X",
        "blocks": [
            {
                "type": "section",
                "block_id": "XTkTR",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hello! <@U01AZ88AQQ4> :tada:. How can I help you.",
                    "verbatim": False
                }
            },
            {
                "type": "actions",
                "block_id": "request_timeoff",
                "elements": [
                    {
                        "type": "button",
                        "action_id": "time_off_balance",
                        "text": {"type": "plain_text", "text": "Check time off balance", "emoji": True},
                        "value": "Check time off balance"
                    },
                    {
                        "type": "button",
                        "action_id": "time_off_request",
                        "text": {"type": "plain_text", "text": "Request time off", "emoji": True},
                        "value": "Request time off"
                    },
                    {
                        "type": "button",
                        "action_id": "time_off_policy",
                        "text": {"type": "plain_text", "text": "Get time off policy", "emoji": True},
                        "value": "Get time off policy"
                    }
                ]
            }
        ]
    },
    "response_url": "https:\/\/hooks.slack.com\/actions\/T01B5M3VC1X\/1394543744577\/NIyyQSrf1FF0R7KPv7VbbjrC",
    "actions": [
        {
            "action_id": "time_off_balance",
            "block_id": "request_timeoff",
            "text":
            {
                "type": "plain_text", "text": "Check time off balance", "emoji": True
            },
            "value": "Check time off balance",
            "type": "button",
            "action_ts": "1600857126.868122"
        }
    ]
}

# payload from modal submission (used views.open method).
{
    "type": "view_submission",
    "team": {"id": "T01B5M3VC1X", "domain": "heybot-workspace"},
    "user": {"id": "U01AZ88AQQ4", "username": "phoebe.ngsyd", "name": "phoebe.ngsyd", "team_id": "T01B5M3VC1X"},
    "api_app_id": "A01BGTV24LQ",
    "token": "RFEwDETALFMJkphCasIfOUZT",
    "trigger_id": "1410876803872.1379717998065.6a115a24993a3a4faefd03f2d2a736c3",
    "view":
    {
        "id": "V01BK6M75U4",
        "team_id": "T01B5M3VC1X",
        "type": "modal",
        "blocks":
        [
            {
                "type": "input",
                "block_id": "employee_id_modal_input",
                "label":
                {
                    "type": "plain_text",
                    "text": "Please provide your employee ID",
                    "emoji": True
                },
                "element":
                {
                    "type": "plain_text_input",
                    "action_id": "employee_id_value",
                    "placeholder":
                    {
                        "type": "plain_text",
                        "text": "e.g 123",
                        "emoji": True
                    }
                }
            }
        ],
        "private_metadata": "{\"channel_id\": \"D01ACC2E8S3\", \"action_id\": \"time_off_policy\"}",
        "callback_id": "employee_id_modal",
        "state":
        {
            "values":
            {
                "employee_id_modal_input":
                {
                    "employee_id_value":
                    {
                        "type": "plain_text_input",
                        "value": "check callback"
                    }
                }
            }
        },
        "hash": "1601009219.3NRSqpiD",
        "title":
        {
            "type": "plain_text",
            "text": "Request Employee ID",
            "emoji": True
        },
        "clear_on_close": True,  # when modal closes, fiels are clear
        "notify_on_close": False,
        "close":
        {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "submit":
        {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "previous_view_id": null,
        "root_view_id": "V01BK6M75U4",
        "app_id": "A01BGTV24LQ",
        "external_id": "",
        "app_installed_team_id": "T01B5M3VC1X",
        "bot_id": "B01AQ1SN737"
    },
    "response_urls": []
}
