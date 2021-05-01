from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def render():
    return "teszt"

if __name__ == "__main__":
    app.run(port=5000)