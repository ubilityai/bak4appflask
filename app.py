from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/app/hello_world", methods=["GET"])
def hello_world():
    return "hello from flaskapptest"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
