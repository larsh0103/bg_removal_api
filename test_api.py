from fastapi.testclient import TestClient
from fastapi import FastAPI, File,UploadFile ,Form
from app import app
from PIL import Image
import base64
import requests 
import numpy as np
import cv2

client = TestClient(app)




def test_read_root():
    response = client.get("/")
    assert response.status_code ==200

def test_filter_image(image_path = "scratch/000001.png"):

    response = client.post(
        "/uploadfile", files={"file": ("filename", open(image_path, "rb"), "image/jpeg")}
    )

    assert response.status_code == 200
    im_bytes = base64.b64decode(response.json()['file'])
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    cv2.imwrite("test_cv2.png",img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img.save('test.png')

test_filter_image()