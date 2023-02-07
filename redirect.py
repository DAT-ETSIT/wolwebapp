from flask import Flask, redirect, request
import os

app = Flask(__name__)

@app.before_request
def before_request():
    if os.environ.get('ENV') != "development":
        if not request.is_secure:
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

if __name__ == '__main__':
    app.run()