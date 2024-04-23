from flask import Flask, render_template, send_file
import cv2
import threading
import time
import pytesseract
import uuid
from dip import cv2_chi_jadu
from eg2 import func

app = Flask(__name__)
fields = ["Class", "DOB", "Mobile", "Blood group", "Name", "PRN"]
details = {field: "Please wait!" for field in fields}
print(id(details), "meow")
i = 0
t = threading.Thread(target=cv2_chi_jadu, args=(details, fields))
# t = threading.Thread(target=func, args=(details, ))
t.start()


@app.get("/")
def root():
    return render_template("index.html")


@app.get("/img")
def img():
    return send_file("./cap.jpg")


@app.get("/imgcomp")
def imgcomp():
    return render_template("img.html", addend=str(uuid.uuid1()).replace("-", ""))


@app.get("/infocomp")
def infocomp():
    return render_template("info.html", details=sorted(details.items()))


@app.get("/info")
def info():
    global i
    i += 1
    print(i)
    return details
