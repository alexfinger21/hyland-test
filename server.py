from flask import Flask
from flask import render_template, request
from flask_cors import CORS

app = Flask(
    __name__,
    static_url_path="",
    static_folder="web/static",
    template_folder="web/templates",
)

@app.route("/upload-photo", methods=["POST"])
def process_photo():
    image = request.files.get("image", "")
    image.save("./test.jpg")
    



    return 
    

@app.route("/", methods=["GET"])
def getTemplate1():
    return render_template('template-1.html')
@app.route("/app", methods=["GET"])
def getTemplate2():
    return render_template('template-2.html')

def create_app():
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
