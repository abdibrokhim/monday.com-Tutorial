import requests
import os
import json


def get_truck_files_count():

    url = "https://api.monday.com/v2"

    payload = json.dumps({
        "query": "query { boards(ids: 468543117) { items_count } }"
    })
    headers = {
        'Authorization': f'{os.getenv("MONDAY_API_TOKEN")}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        print('response:', response)

        count = json.loads(response.text)['data']['boards'][0]['items_count']

        return count
    except Exception as e:
        print(e)
        
        return ""
    


def get_truck_files(limit: int = 25):

    url = "https://api.monday.com/v2"

    payload = json.dumps({
        "query": "query { boards(ids: 468543117) { " + f"items (limit: {limit})" + "{ id name column_values { title text } } } }"
    })
    headers = {
        'Authorization': f'{os.getenv("MONDAY_API_TOKEN")}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        print('response:', response)

        data = json.loads(response.text)['data']['boards'][0]['items']

        return data
    except Exception as e:
        print(e)
        
        return ""


def get_truck_files_by_id(id: int,):

    url = "https://api.monday.com/v2"

    payload = json.dumps({
        "query": "query { boards(ids: 468543117) { " + f"items (ids: {id})" + "{ id name column_values { title text } } } }"
    })
    headers = {
        'Authorization': f'{os.getenv("MONDAY_API_TOKEN")}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        print('response:', response)

        files = json.loads(response.text)['data']['boards'][0]['items'][0]['column_values'][16]['text'].split(',')

        return files
    except Exception as e:
        print(e)
        
        return ""