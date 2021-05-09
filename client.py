import requests
import json
import cv2

addr = "http://localhost:5000"
test_url = addr + "/handwrite/test"

content_type = "image/jpeg"
headers = {"content-type": content_type}

img = cv2.imread("excellent2.jpg")
_, img_encoded = cv2.imencode(".jpg", img)

response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

with open("new.ttf", "wb+") as f:
    f.write(response.content)
