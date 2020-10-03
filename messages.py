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
                "block_id": "say_hello_msg",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hello! <@{user}> :tada:. How can I help you."
                }
            },
            {
                "type": "actions",
                "block_id": "timeoff_action_buttons",
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
        return f"Hello <@{user}>! Sorry, I'm having trouble understanding you right now."

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

    # build view payload
    def get_inputs_request(self, channel_id, action_id):
        private_metadata = {
            "channel_id": channel_id,
            "action_id": action_id
        }
        # jsonify a dict into a string (required type for private_metadata)
        json_private_metadata = json.dumps(private_metadata)
        return (
            {
                "type": "modal",
                "private_metadata": json_private_metadata,
                "callback_id": "inputs_request_timeoff_modal",
                "title": {
                    "type": "plain_text",
                    "text": "Time Off Request"
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Submit"
                },
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "inputs_request_timeoff_input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "employee_id_value",
                            "placeholder": {
                                    "type": "plain_text",
                                    "text": "Please provide your employee ID"
                            }
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Employee ID"
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "time_off_type",
                        "element": {
                            "type": "static_select",
                            "action_id": "time_off_type_value",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Time off Type",
                                "emoji": True
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Bereauvement",
                                        "emoji": True
                                    },
                                    "value": "77"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Vacation",
                                        "emoji": True
                                    },
                                    "value": "78"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Sick",
                                        "emoji": True
                                    },
                                    "value": "79"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "FMLA",
                                        "emoji": True
                                    },
                                    "value": "80"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Comp/In Lieu Time",
                                        "emoji": True
                                    },
                                    "value": "81"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "COVID-19 Related Absence",
                                        "emoji": True
                                    },
                                    "value": "82"
                                }
                            ]
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Time Off Type",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "start_date",
                        "element": {
                            "type": "datepicker",
                            "action_id": "start_date_value",
                            "initial_date": "2020-01-01",
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "Start Date",
                                    "emoji": True
                                }
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Start Date",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "end_date",
                        "element": {
                            "type": "datepicker",
                            "action_id": "end_date_value",
                            "initial_date": "2020-01-01",
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "End Date",
                                    "emoji": True
                                }
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "End Date",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "amount_in_days",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "amount_in_days_value",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "0.5, 1, ... , 3.5, 5"
                            }
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Amount in Days",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "note",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "note_value",
                            "multiline": True
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Note",
                            "emoji": True
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
            answer = f"*{time_off_type}*: \n• Balance: {balance} \n• Used To Date: {usedYearToDate} \n"
            # concatinate each individual block together
            text_assembly += answer
        # attach text_assembly to the official message block that will be used by chat_postMessage in heybot_v[#].py
        block_message = [
            {
                "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"Your anticipated time off balance on {end} is here! :ghost:",
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
            answer = f"*{policy}*: \n• Policy ID: {policy_id} \n• EffectiveDate: {effectiveDate} \n"
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
