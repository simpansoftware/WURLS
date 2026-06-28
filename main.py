from flask import Flask, request, render_template, redirect, send_file
from waitress import serve
import json
import random
import string
import os
import validators
import io
import qrcode
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    with open("urls.json", "r") as f:
        data = json.load(f)
    return render_template('index.html', count=len(data))

@app.route('/usage', methods=['GET'])
def usage():
    origin = request.host_url.rstrip("/")
    return render_template("usage.html", origin=origin)

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form['url']
    custom = request.form.get("custom", "").strip().upper()
    origin = request.host_url.rstrip("/")
    if validators.url(url) != True:
        return render_template("error.html", error="Invalid URL (maybe you forgot to put https:// before it?)"), 404
    else:
        with open("urls.json", "r") as f:
            data = json.load(f)
            for short, info in data.items():
                if info["long"] == url:
                    return render_template("shorten.html", count=len(data), exists=short, origin=origin)
            if custom:
                if not re.fullmatch(r"[A-Z0-9]{1,20}", custom):
                    return render_template("error.html", error="Shortened URL not valid"), 409
                else:
                    shortened = custom
                    if shortened in data:
                        return render_template("error.html", error="Shortened URL already taken"), 409

            else:
                shortened = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                while shortened in data:
                    shortened = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            data[shortened] = {"long": url, "visits": 0}
            with open("urls.json", "w") as f:
                json.dump(data, f, indent=4)

            return render_template("shorten.html", count=len(data), shortened=shortened, origin=origin)

@app.route('/l', methods=['GET'])
def getlink():
    shortthing = request.args.get("url")
    with open("urls.json", "r") as f:
        data = json.load(f)

    if shortthing not in data:
        return render_template("error.html", error="Shortened URL not found"), 404

    data[shortthing]["visits"] = data[shortthing].get("visits", 0) + 1
    with open("urls.json", "w") as f:
        json.dump(data, f, indent=4)
    return redirect(data[shortthing]["long"])

@app.route('/g', methods=['GET'])
def getshort():
    longthing = request.args.get("url")
    origin = request.host_url.rstrip("/")
    with open("urls.json", "r") as f:
        data = json.load(f)

        for short, info in data.items():
            if info["long"] == longthing:
                return render_template("goto.html", origin=origin, url=longthing, short=short)
        
        return render_template("error.html", error="Shortened URL not found"), 404

@app.route('/stats', methods=['GET'])
def stats():
    thing = request.args.get("url")
    if thing is None:
        with open("urls.json", "r") as f:
            data = json.load(f)
        return render_template("statthing.html", count=len(data))
    else:
        origin = request.host_url.rstrip("/")
        with open("urls.json", "r") as f:
            data = json.load(f)

            if thing in data:
                short = thing
            else:
                short = None
                for code, info in data.items():
                    if info["long"] == thing:
                        short = code
                        break
                    
            if short is None:
                return render_template("error.html", error="Shortened URL not found"), 404
            
            longthing = data[short]["long"]
            visits = data[short].get("visits", 0)

            return render_template("stats.html", origin=origin, url=longthing, short=short, visits=visits)

@app.route('/qr', methods=['GET'])
def qr():
    qrinput = request.args.get("url")
    origin = request.host_url.rstrip("/")
    buffer = io.BytesIO()
    with open("urls.json", "r") as f:
        data = json.load(f)

    if qrinput not in data:
        return render_template("error.html", error="Shortened URL not found"), 404

    url = f"{origin}/l?url={qrinput}"
    img = qrcode.make(url)
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")

if __name__ == '__main__':
    try:
        with open("urls.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        with open("urls.json", "w") as f:
            f.write("""{
    "GOOGLE": {
        "long": "https://google.com",
        "visits": 0
    }
}""")
    app.run(host="0.0.0.0", port=5000)