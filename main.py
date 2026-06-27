from flask import Flask, request, render_template, redirect
import json
import random
import string
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    with open("urls.json", "r") as f:
        data = json.load(f)
    return render_template('index.html', count=len(data))

@app.route('/usage', methods=['GET'])
def usage():
    origin = request.headers.get("Origin") or request.host_url
    return render_template("usage.html", origin=origin)

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form['url']
    origin = request.headers.get("Origin") or request.host_url
    with open("urls.json", "r") as f:
        data = json.load(f)
        for short, info in data.items():
            if info["long"] == url:
                return render_template("shorten.html", count=len(data), exists=short, origin=origin)
        shortened = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        while shortened in data:
            shortened = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        data[shortened] = {"long": url}
        with open("urls.json", "w") as f:
            json.dump(data, f, indent=4)

        return render_template("shorten.html", count=len(data), shortened=shortened, origin=origin)

@app.route('/l', methods=['GET'])
def getlink():
    shortthing = request.args.get("url")
    with open("urls.json", "r") as f:
        data = json.load(f)

    if shortthing not in data:
        return "short url not found", 404

    return redirect(data[shortthing]["long"])

@app.route('/g', methods=['GET'])
def getshort():
    longthing = request.args.get("url")
    origin = request.headers.get("Origin") or request.host_url
    with open("urls.json", "r") as f:
        data = json.load(f)

        for short, info in data.items():
            if info["long"] == longthing:
                return render_template("goto.html", origin=origin, url=longthing, short=short)
        
        if longthing not in data:
            return "short url not found", 404

if __name__ == '__main__':
    try:
        with open("urls.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        with open("urls.json", "w") as f:
            f.write("""{
    "NZPDI": {
        "long": "https://google.com"
    }
}""")
    app.run(debug=True)