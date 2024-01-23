from datetime import datetime
import urllib.request
import base64
import json
import time
import os
from dotenv import load_dotenv
import requests
import logging


load_dotenv()
webui_server_url = os.environ["webui-api"]
port = 0

API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"


class RemoveBg(object):

    def __init__(self, api_key, error_log_file):
        self.__api_key = api_key
        logging.basicConfig(filename=error_log_file)

    async def remove_background_from_base64_img(self, base64_img, size="regular", new_file_name="no-bg.png", bg_color=None):
        """
        Removes the background given a base64 image string and outputs the file as the given new file name.
        :param base64_img: the base64 image string
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        :param new_file_name: the new file name of the image with the background removed
        """
        response = requests.post(
            API_ENDPOINT,
            data={
                'image_file_b64': base64_img,
                'size': size,
                'bg_color': bg_color
            },
            headers={'X-Api-Key': self.__api_key}
        )
        response.raise_for_status()
        return self.__output_file__(response, new_file_name)

    def __output_file__(self, response, new_file_name):
        # If successful, write out the file
        if response.status_code == requests.codes.ok:
            return response.content
        # Otherwise, print out the error
        else:
            error_reason = response.json()["errors"][0]["title"].lower()
            logging.error("Unable to save %s due to %s", new_file_name, error_reason)


def timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")


def encode_file_to_base64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def call_api(api_endpoint, **payload):
    global port
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        f'{webui_server_url+str(port)}/{api_endpoint}',
        headers={'Content-Type': 'application/json'},
        data=data,
    )
    port = (port + 1) % 8
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
        res = [f'txt2img-{timestamp()}-{index}.png', image]
        response2user.append([f'img2img-{timestamp()}-{index}.png', image])
        break
    return res
