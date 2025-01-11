import os
from flask import Flask
from flask import render_template

app = Flask(__name__,
                  static_url_path="",
                  static_folder="web/static",
                  template_folder="web/templates")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

def create_app():
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
