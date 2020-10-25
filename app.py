from flask import *
import os
from styleChecker import *

# __name__ references this file
app = Flask(__name__)

# make home page
# define how to access this page by giving it a route
@app.route("/")
def home():
    # looks for index.html in folder named "templates"
    return render_template("index.html")

@app.route("/result")
def result():
    infoPage()
    return render_template("result.html") 

@app.route("/back", methods=['POST'])
def back():
    return redirect("/")

@app.route("/handleUpload", methods = ['POST'])
def handleUpload():
    if(request.files['fileUploaded']):
        file = request.files["fileUploaded"]
        fileName = file.filename
        if(checkFileType(fileName)):
            os.remove("static/uploads/text.txt")
            file.save(os.path.join("static/uploads", "text.txt"))
            return redirect("/result")
        else:
            flash("wrong file type", "warning")
    else:
        flash("No file selected", "warning")
    return redirect("/")

def checkFileType(name):
    fileName = name.split(".")
    if(fileName[1] != "java"):
        return False
    return True

if(__name__ == "__main__"):
    app.debug = True
    app.secret_key = "secret key"
    app.run()
