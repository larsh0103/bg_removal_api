from fastapi import FastAPI, File,UploadFile
from typing import Optional
import os
import cv2
import numpy as np

from image_background_remove_tool import run
from PIL import Image
import base64


app = FastAPI()


def filter_image(image):
    # dir_path = os.path.dirname(image_path)
    # filename = os.path.basename(image_path).split(".")[0] +'_filtered.png'
    # filtered_image_path = (os.path.join(dir_path,filename))
    img = run.process(input_path=image, output_path='filtered_image_path.png', model_name="u2net",model_dir='image_background_remove_tool/models',
            preprocessing_method_name="bbd-fastrcnn", postprocessing_method_name="rtb-bnb")
    return img

# filter_iamge("scratch/000001.png")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/filter")


@app.post("/uploadfile")
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
