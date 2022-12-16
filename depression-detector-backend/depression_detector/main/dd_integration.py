import requests

# model endpoint url
URL = ''
HEADERS = {'content-type': 'application/json'}


def get_depression(data):
    response = requests.post(
        url=URL,
        json={ "text": data },
        headers=HEADERS
    )
    return response.json()