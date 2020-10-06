# Instruction


import requests
import json
import os
import datetime
import calendar
import urllib
from flask import Flask, request, jsonify


class Bamboohr:
    def __init__(self):
        self.companyDomain = os.environ['COMPANY_DOMAIN']
        self.AUTHORIZATION_TOKEN = os.environ['AUTHORIZATION_TOKEN']
        self.status = {
            'approve': 'approved',
            'decline': 'declined',
            'request': 'requested'
        }

    # Get time of balance
    def time_off_balance(self, employee_id):
        url = f"https://api.bamboohr.com/api/gateway.php/{self.companyDomain}/v1/employees/{employee_id}/time_off/calculator"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.AUTHORIZATION_TOKEN}"
        }
        response = requests.request(
            "GET", url, headers=headers)

        # Solution2 : use urllib.parse.parse_qs

        # Solution1: step by step
        # parse JSON response.text, return type 'list'
        response_parse_tolist = json.loads(response.text)
        # convert a list of dictionaries into a dict
        response_todict = {}
        for item in response_parse_tolist:
            # remove and return the name field to use as a key
            name = item.pop("name")
            # add new key:value to response_todict Dict
            response_todict[name] = item

        # Expected: "time off type": {'balance': '..', 'usedYearToDate': '..', 'end': '...'}
        answer = {}
        # collect all keys from response_todict ("Vacation", "Sick", "COVID-19 Related Absence", "Bereavement", "Comp/In Lieu Time", "FMLA")
        keys = response_todict.keys()
        info_needed = ("balance", "usedYearToDate", "end")
        # Go to (e.g) "Vacation":{'timeOffType': '78', 'units': 'hours', 'balance': '0.0', 'end': '2020-09-24', 'policyType': 'discretionary', 'usedYearToDate': '32.0'}
        for key in keys:
            sub_answer = {}
            # Check if the element is info_needed
            # For each element in value of key "Vaction"
            for el in response_todict[key]:
                # Create a sub-dict inside answer Dict  {'Vacation': {}, 'Sick': {}, ...}
                if el in info_needed:
                    # add el key:value to sub_answer dict
                    # 'Vacation': {'balance': '0.0', 'end': '2020-09-24'...}
                    sub_answer[el] = response_todict[key][el]
            # add sub_answer Dict to answer Dict
            # {'Vacation': {'balance': '0.0', 'end': '2020-09-24', 'usedYearToDate': '0.0'}, 'Sick': {'balance': '0.0', 'end': '2020-09-24', 'usedYearToDate': '0.0'}, ...}
            answer[key] = sub_answer

        # return result to answer user
        if response.status_code == 200:
            # sample answer
            # {'Vacation': {'balance': '81.0', 'end': '2020-09-26', 'usedYearToDate': '144.0'},...}
            return answer
        else:
            return answer

    # Get time off policies
    def time_off_policy(self):
        url = f"https://api.bamboohr.com/api/gateway.php/{self.companyDomain}/v1/meta/time_off/policies/"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.AUTHORIZATION_TOKEN}"}
        response = requests.request("GET", url, headers=headers)
        # parse JSON response.text, return a list of dictionaries
        response_parse_tolist = json.loads(response.text)

        # convert a list of dictionaries into a dict
        response_todict = {}
        for item in response_parse_tolist:
            # remove and return the name field to use as a key
            name = item.pop("name")
            # add new key:value to response_todict Dict
            response_todict[name] = item

        # Expected: collect "policy'": {'id': '..', 'effectiveDate': '..'}
        answer = {}
        # collect all keys from response_todict ("BambooHR Manual Policy", "Vacation Full-Time", ..)
        keys = response_todict.keys()
        info_needed = ("id", "effectiveDate")

        # Go to (e.g) 'BambooHR Manual Policy': {'id': '82', 'timeOffTypeId': '82', 'effectiveDate': None, 'type': 'manual'}
        for key in keys:
            # Create a sub-dict inside answer Dict  {"BambooHR Manual Policy": {}, "Vacation Full-Time": {}, ...}
            sub_answer = {}
            # For each element in value of key "BambooHR Manual Policy"
            for el in response_todict[key]:
                # Check if the element is info_needed
                if el in info_needed:
                    # add el key:value to sub_answer dict
                    # 'BambooHR Manual Policy': {'id': '..', 'effectiveDate': '..'}
                    sub_answer[el] = response_todict[key][el]
            # add sub_answer Dict to answer Dict
            # {'BambooHR Manual Policy': {'id': '..', 'effectiveDate': '..'}, ...}
            answer[key] = sub_answer

        if response.status_code == 200:
            # answer sample
            # {'BambooHR Manual Policy': {'id': '81', 'effectiveDate': None},.....}
            return answer
        else:
            return {}

    # Request time off

    def time_off_request(self, employee_id, start_date, end_date, amount, timeOffTypeId, note):
        # convert amount in str to float or int
        if float(amount):
            amount = float(amount)
        else:
            amount = int(amount)
        # convert amount in days into hours
        half_day_to_hours = 4
        full_day_to_hours = 8
        amount_in_hours = 0
        if isinstance(amount, int):
            amount_in_hours = amount * full_day_to_hours
        elif isinstance(amount, float):
            amount_in_hours = (
                (amount-0.5) * full_day_to_hours) + half_day_to_hours
        else:
            print("ERROR: wrong type `amount`")
        # print("----------")
        # print("input to make request")
        # print(employee_id)
        # print(start_date)
        # print(end_date)
        # print(amount)
        # print(amount_in_hours)
        # print(timeOffTypeId)
        # print(note)

        url = f"https://api.bamboohr.com/api/gateway.php/{self.companyDomain}/v1/employees/{employee_id}/time_off/request"
        headers = {
            "content-type": "application/json",
            "authorization": f"Basic {self.AUTHORIZATION_TOKEN}"
        }
        payload = {
            "notes": [
                {
                    "from": "employee",
                    "note": f"{note}"
                }
            ],
            "status": f"{self.status['request']}",
            "start": f"{start_date}",
            "end": f"{end_date}",
            "timeOffTypeId": f"{timeOffTypeId}",
            "amount": f"{amount_in_hours}"
        }
        response = requests.request("PUT", url, json=payload, headers=headers)
        # print(response.status_code)
        if response.status_code == 201:
            return "requested"

    def get_request_receipt(self, employee_id, amount):
        amount_in_days = amount
        start = datetime.date.today()
        end = self.get_month_day_range(start)
        url = f"https://api.bamboohr.com/api/gateway.php/{self.companyDomain}/v1/time_off/requests/"

        querystring = {"employeeId": f"{employee_id}", "start": f"{start}",
                       "end": f"{end}", "status": "requested"}
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.AUTHORIZATION_TOKEN}"
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        response_text = json.loads(response.text)
        receipt = {
            "id": response_text[-1]["id"],
            "type": response_text[-1]["type"]["name"],
            "amount_in_days": amount_in_days,
            "amount_in_hours": response_text[-1]["amount"]["amount"],
            "start": response_text[-1]["start"],
            "end": response_text[-1]["end"]
        }

        return receipt

    # https://gist.github.com/waynemoore/1109153
    def get_month_day_range(self, date):
        # For a date 'date' returns the start and end date for the month of 'date'.

        # Month with 31 days:
        # >>> date = datetime.date(2011, 7, 27)
        # >>> get_month_day_range(date)
        # (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))

        # Month with 28 days:
        # >>> date = datetime.date(2011, 2, 15)
        # >>> get_month_day_range(date)
        # (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))

        # first_day = date.replace(day=1)
        last_day = date.replace(
            day=calendar.monthrange(date.year, date.month)[1])
        return last_day


# Instantiate class Bamboohr
bamboohr = Bamboohr()

if __name__ == "__main__":
    # bamboohr.time_off_request(
    #     108, "2020-10-12", "2020-10-14", 2.5, 78, "hello")
    bamboohr.get_request_receipt(108, 2.5)
