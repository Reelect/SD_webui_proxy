import base64

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response

from util import call_txt2img_api, call_img2img_api

app = FastAPI()


@app.get("/txt2img")
async def txt2img(prompt: str = "disney character style, pixar, cute, petit, male, asian, 3D"):
    payload = {
        "prompt": prompt,
        "negative_prompt": "ugly, extra fingers, deformed hands, mutant hands, fusioned hands, deformed, mutant, bad "
                           "anatomy, letter",
        "seed": 256660272,
        "steps": 80,
        "width": 512,
        "height": 512,
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M Karras",
        "n_iter": 1,
        "batch_size": 1,

        # example args for x/y/z plot
        # "script_name": "x/y/z plot",
        # "script_args": [
        #     1,
        #     "10,20",
        #     [],
        #     0,
        #     "",
        #     [],
        #     0,
        #     "",
        #     [],
        #     True,
        #     True,
        #     False,
        #     False,
        #     0,
        #     False
        # ],

        # example args for Refiner and ControlNet
        "alwayson_scripts": {
            "Refiner": {
                "args": [
                    True,
                    "sd_xl_refiner_1.0",
                    0.8
                ]
            }
        },
        # "override_settings": {
        #     'sd_model_checkpoint': "sd_xl_base_1.0",  # this can use to switch sd model
        # },
    }
    res = await call_txt2img_api(**payload)
    return Response(content=res[1], media_type="image/png")


@app.post("/img2img")
async def img2img(init_image: UploadFile(...) = File()):
    payload = {
        "prompt": "disney character style, pixar, cute, petit, male, asian, 3D",
        "negative_prompt": "ugly, extra fingers, deformed hands, mutant hands, fusioned hands, deformed, mutant, bad "
                           "anatomy, letter",
        "seed": 256660272,
        "steps": 80,
        "width": 960,
        "height": 960,
        "cfg_scale": 15,
        "sampler_name": "DPM++ 2M Karras",
        "denoising_strength": 0.72,
        "batch_size": 1,
        "resize_mode": 1,

        # example args for x/y/z plot
        # "script_name": "x/y/z plot",
        # "script_args": [
        #     1,
        #     "10,20",
        #     [],
        #     0,
        #     "",
        #     [],
        #     0,
        #     "",
        #     [],
        #     True,
        #     True,
        #     False,
        #     False,
        #     0,
        #     False
        # ],
        "init_images": [base64.b64encode(init_image.file.read()).decode('utf-8')],
        # example args for Refiner and ControlNet
        "alwayson_scripts": {
            "Refiner": {
                "args": [
                    True,
                    "sd_xl_refiner_1.0.safetensors",
                    0.5
                ]
            }
        },
        # "override_settings": {
        #     'sd_model_checkpoint': "sd_xl_base_1.0",  # this can use to switch sd model
        # },
    }
    res = await call_img2img_api(**payload)
    return Response(content=res[1], media_type="image/png")
