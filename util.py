from datetime import datetime
import urllib.request
import base64
import json
import time
import os

webui_server_url = os.environ["webui-api"]


def timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")


def encode_file_to_base64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def call_api(api_endpoint, **payload):
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        f'{webui_server_url}/{api_endpoint}',
        headers={'Content-Type': 'application/json'},
        data=data,
    )
    response = urllib.request.urlopen(request)
    return json.loads(response.read().decode('utf-8'))


async def call_txt2img_api(**payload):
    response = call_api('sdapi/v1/txt2img', **payload)
    response2user = []
    res = []
    for index, image in enumerate(response.get('images')):
        res = [f'txt2img-{timestamp()}-{index}.png', base64.b64decode(image)]
        response2user.append([f'txt2img-{timestamp()}-{index}.png', base64.b64decode(image)])
        break
    return res


async def call_img2img_api(**payload):
    response = call_api('sdapi/v1/img2img', **payload)
    response2user = []
    res = []
    for index, image in enumerate(response.get('images')):
        res = [f'txt2img-{timestamp()}-{index}.png', base64.b64decode(image)]
        response2user.append([f'img2img-{timestamp()}-{index}.png', base64.b64decode(image)])
        break
    return res
