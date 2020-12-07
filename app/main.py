from fastapi import FastAPI, File,UploadFile
from typing import Optional
from pydantic import BaseModel
import os
import cv2
import numpy as np

from .image_background_remove_tool import run
from PIL import Image
import base64
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
# import sys
# sys.path.append("../")
# import download_models


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://romantic-torvalds-fd4d67.netlify.app"
]

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


def filter_image(image):
    img = run.process(input_path=image, output_path='filtered_image_path.png', model_name="u2netp",model_dir='app/image_background_remove_tool/models',
            preprocessing_method_name=None, postprocessing_method_name="rtb-bnb")
    return img

class HealthResponse(BaseModel):
    api_version: str = "0.1"
    description: str = "Background removal api"


@app.get("/health")
async def health():
    resp = HealthResponse()
    return resp

@app.post("/predict")
async def create_upload_file(file : UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = Image.fromarray(image)
    # image = Image.fromarray(nparr)
    filtered_image = filter_image(image)
    filtered_image = np.asarray(filtered_image)
    _, encoded_img = cv2.imencode('.PNG', filtered_image)
    encoded_img = base64.b64encode(encoded_img)
    return {"filename" : file.filename, "file" : encoded_img}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8080)