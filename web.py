from flask import *

app = Flask(__name__)

@app.route("/")
def render():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=1414)