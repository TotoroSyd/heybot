from bamboohr import Bamboohr
import json


class Message:
    def __init__(self):
        self.icon_emoji = ":robot_face:"
        self.bamboohr = Bamboohr()

    # blocks
    def understood_greeting(self, user):
        return ([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hello! <@%s> :tada:. How can I help you." % user
                }
            },
            {
                "type": "actions",
                "block_id": "request_timeoff",
                "elements": [
                        {
                            "type": "button",
                            "text": {
                                    "type": "plain_text",
                                "text": "Check Time Off Balances",
                                        "emoji": True
                            },
                            "value": "Check time off balances",
                            "action_id": "time_off_balance"
                        },
                    {
                            "type": "button",
                            "text": {
                                    "type": "plain_text",
                                    "text": "Request Time Off",
                                    "emoji": True
                            },
                            "value": "Request time off",
                            "action_id": "time_off_request"
                    },
                    {
                            "type": "button",
                            "text": {
                                    "type": "plain_text",
                                    "text": "Get Time Off Policies",
                                    "emoji": True
                            },
                            "value": "Get time off policy",
                            "action_id": "time_off_policy"
                    }
                ]
            }
        ])

    def confuse(self, user):
        return "Hello <@%s>! Sorry, I'm having trouble understanding you right now." % user

   # build view payload
    def get_employee_id_modal(self, channel_id, action_id):
        private_metadata = {
            "channel_id": channel_id,
            "action_id": action_id
        }
        # jsonify a dict into a string (required type for private_metadata)
        json_private_metadata = json.dumps(private_metadata)
        return ({
            "type": "modal",
            "private_metadata": json_private_metadata,
            "callback_id": "employee_id_modal",
            "title": {
                "type": "plain_text",
                "text": "Request Employee ID",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "clear_on_close": True,
            "notify_on_close": False,
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "employee_id_modal_input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "employee_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "e.g 123"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Please provide your employee ID"
                    }
                }
            ]
        }
        )

    def answer_time_off_balance(self, report):
        report = report
        # get all keys aka time off types from report
        time_off_types = report.keys()
        # initiate text_assembly variable
        text_assembly = ""
        # for each time of type, call needed vaues
        for time_off_type in time_off_types:
            balance = report[time_off_type]["balance"]
            end = report[time_off_type]["end"]
            usedYearToDate = report[time_off_type]["usedYearToDate"]
            # build individual block for each time off type
            answer = "*%s*: \n• Balance: %s \n• Used To Date: %s \n" % (
                time_off_type, balance, usedYearToDate)
            # concatinate each individual block together
            text_assembly += answer
        # attach text_assembly to the official message block that will be used by chat_postMessage in heybot_v[#].py
        block_message = [
            {
                "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Your anticipated time off balance on %s is here! :ghost:" % (end),
                            "emoji": True
                        }
            },
            {
                "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": text_assembly
                        }
            }
        ]

        return (block_message)

    def answer_time_off_policy(self, report):
        report = report
        # get all keys aka policy from report
        policies = report.keys()
        # initiate text_assembly variable
        text_assembly = ""
        # for each policy, call needed vaues
        for policy in policies:
            policy_id = report[policy]["id"]
            effectiveDate = report[policy]["effectiveDate"]
            # build individual block for each policy
            answer = "*%s*: \n• Policy ID: %s \n• EffectiveDate: %s \n" % (
                policy, policy_id, effectiveDate)
            # concatinate each individual block together
            text_assembly += answer
        # attach text_assembly to the official message block that will be used by chat_postMessage in heybot_v[#].py
        block_message = [
            {
                "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Here you are! :ghost:",
                            "emoji": True
                        }
            },
            {
                "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": text_assembly
                        }
            }
        ]

        return (block_message)
