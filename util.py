from datetime import datetime
import urllib.request
import aiohttp
import base64
import json
import time
import os
import asyncio
from dotenv import load_dotenv


load_dotenv()
webui_server_url = os.environ["webui-api"]
port = 0


def timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")


async def call_api(api_endpoint, **payload):
    global port
    port = (port + 1) % 8
    data = json.dumps(payload).encode('utf-8')

    async with aiohttp.ClientSession() as session:
        url = f'{webui_server_url + str(port)}/{api_endpoint}'
        headers = {'Content-Type': 'application/json'}
        async with session.post(url, data=data, headers=headers) as response:
            response_data = await response.text()
            return json.loads(response_data)


async def call_txt2img_api(**payload):
    response = await call_api('sdapi/v1/txt2img', **payload)
    response2user = []
    res = []
    for index, image in enumerate(response.get('images')):
        res = [f'txt2img-{timestamp()}-{index}.png', base64.b64decode(image)]
        response2user.append([f'txt2img-{timestamp()}-{index}.png', base64.b64decode(image)])
        break
    return res


async def call_img2img_api(**payload):
    response = await call_api('sdapi/v1/img2img', **payload)
    response2user = []
    res = []
    for index, image in enumerate(response.get('images')):
        res = [f'txt2img-{timestamp()}-{index}.png', base64.b64decode(image)]
        response2user.append([f'img2img-{timestamp()}-{index}.png', base64.b64decode(image)])
        break
    return res
