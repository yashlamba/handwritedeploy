import requests
import cv2
import time

# addr = "http://handwritetest.herokuapp.com"
addr = "http://localhost:5000"
test_url = addr + "/handwrite/test"

content_type = "image/jpeg"
headers = {"content-type": content_type}

img = cv2.imread("excellent2.jpg")
_, img_encoded = cv2.imencode(".jpg", img)

response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
print(response.status_code)
print(response.text)
while True:
    time.sleep(3)
    checkstatus = requests.get(addr + "/handwrite/" + eval(response.text)["path"])
    print(checkstatus.text)
    if checkstatus.text == "Done":
        font = requests.post(addr + "/handwrite/fetch/" + eval(response.text)["path"])
        # print(font.content)
        break

# if response.status_code == 200:
with open("new.ttf", "wb+") as f:
    f.write(font.content)
