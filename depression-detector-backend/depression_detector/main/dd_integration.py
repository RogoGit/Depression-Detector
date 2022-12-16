import requests

URL = ''


def get_depression(data):
    response = requests.post(
        url=URL,
        data=data
    )
    return response
