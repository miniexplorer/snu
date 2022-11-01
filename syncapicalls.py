from parameters import *
import requests

import json
from rich import print
from rich.json import JSON
from rich import print_json
from DataUtil import *

def users_id_accessories_get(id: int):
    url = base_url + "/api/v1/users/" + str(id) + "/accessories"
    response = requests.get(url, headers=headers)
    return response

def accessories_id_checkedout_get(id: int):
    url = base_url + "/api/v1/accessories/" + str(id) + "/checkedout"
    response = requests.get(url, headers=headers)
    return response

def users_id_get(id: int):
    url = base_url + f"/api/v1/users/{id}"
    response = requests.get(url, headers=headers)
    return response

def accessories_id_get(id: int):
    url = base_url + f"/api/v1/accessories/{id}"
    response = requests.get(url, headers=headers)
    return response

def accessories_id_checkout(id: int, assigned_to: int, note: str):
    url = base_url + f"/api/v1/accessories/{str(id)}/checkout"
    payload = {
        "assigned_to": str(assigned_to),
        "note": note
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

def reports_activity_get(search: str, action_type: str = "checkout"):
    url = base_url \
        + "/api/v1/reports/activity?limit=200&offset=0" \
        + "&search=" + search \
        + "&action_type=" + action_type

    response = requests.get(url, headers=headers)
    print(response.text)  # print(response.text.encode("utf-8"))
""" def reports_activity_get(limit: int, offset:
                         int, search: str,
                         target_type: str,
                         target_id: int,
                         item_type: str,
                         item_id: int,
                         action_type: str):
    url = base_url \
        + "/api/v1/reports/activity?" \
        + "limit=limit" \
        + "&offset=offset" \
        + "&search=search" \
        + "&target_type=target_type" \
        + "&target_id=target_id" \
        + "&item_type=item_type" \
        + "&item_id=item_id" \
        + "&action_type=action_type"
    response = requests.get(url, headers=headers)
    print(response.text) """

# Custom
def get_user_name(id: int) -> str:
    response = users_id_get(id)
    jsondata = getjson(response.content)
    return jsondata["name"]

def get_acessory_name(id: int) -> str:
    response = accessories_id_get(id)
    jsondata = getjson(response.content)
    return jsondata["name"]

def get_acessory_remaining_qty(id: int) -> int:
    response = accessories_id_get(id)
    jsondata = getjson(response.content)
    return int(jsondata["remaining_qty"])

def users_id_accessories_get_rows(id: int):
    response = users_id_accessories_get(id)
    jsondata = getjson(response.content)
    return jsondata["rows"]

def accessories_id_checkedout_get_rows(id: int):
    response = accessories_id_checkedout_get(id)
    jsondata = getjson(response.content)
    acc_rows = jsondata["rows"]
    for row in acc_rows:
        row["accessory_id"] = id
    return jsondata["rows"]