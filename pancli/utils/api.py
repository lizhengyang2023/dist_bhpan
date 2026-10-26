

import requests
import json
import time

# Use Requests default CA verification, including REQUESTS_CA_BUNDLE.

class ApiException(Exception):

    def __init__(self, err, *args: object) -> None:
        super().__init__(*args)
        self.err = err


def post_json(url: str, json_obj, tokenid: str=None, *, session: requests.Session=None):
    # print(url)
    j = json.dumps(json_obj)
    headers = {
        'Content-Type': 'application/json',
    }
    if (tokenid is not None):
        headers['Authorization'] = 'Bearer ' + tokenid
    for retry in range(10):
        if (session is not None):
            requests_ = session
        else:
            requests_ = requests
        try:
            r = requests_.post(url, headers=headers, data=j, verify=True)
            if (r.status_code != 503):
                break
            else:
                print('503 server busy, retry:', retry+1)
                time.sleep(1)
        except requests.exceptions.ConnectionError as e:
            # since v7 the server will occasionally not respond
            print('requests.exceptions.ConnectionError, retry:', retry+1)
            time.sleep(1)
    if (r.status_code not in (200, 201)):
        j = None
        try:
            j = r.json()
        except:
            pass
        raise ApiException(j, 'api returned HTTP %s\n%s' % (r.status_code, r.text))
    if (r.text == ''):
        return None
    res = r.json()
    return res


def get_url(url: str, tokenid: str=None):
    headers = dict()
    if (tokenid is not None):
        headers['Authorization'] = 'Bearer ' + tokenid
    for retry in range(10):
        r = requests.get(url, headers=headers, verify=True)
        if (r.status_code != 503):
            break
        else:
            print('503 server busy, retry:', retry+1)
            time.sleep(1)
    if (r.status_code != 200):
        j = None
        try:
            j = r.json()
        except:
            pass
        raise ApiException(j, 'api returned HTTP %s\n%s' % (r.status_code, r.text))
    if (r.text == ''):
        return None
    res = r.json()
    return res


def put_file(url: str, headers: dict, content: bytes):
    for retry in range(10):
        try:
            r = requests.put(url, headers=headers, data=content, verify=True)
            break
        except requests.exceptions.ConnectionError as e:
            print('requests.exceptions.ConnectionError, retry:', retry+1)
            time.sleep(1)

def put_file_stream(url: str, headers: dict, content_stream):
    r = requests.put(url, headers=headers, data=content_stream, verify=True)


def get_file(url: str):
    r = requests.get(url, verify=True)
    return r.content

def get_file_stream(url: str):
    r = requests.get(url, stream=True, verify=True)
    return r

