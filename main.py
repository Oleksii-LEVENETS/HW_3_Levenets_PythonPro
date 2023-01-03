from flask import *

app = Flask(__name__)


@app.get("/start/")
@app.get("/")
def start():
    return "Start Page"


if __name__ == '__main__':
    app.run(port=5002, host="0.0.0.0", debug=True)
