from flask import render_template,request,redirect
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone
from config import S3_BUCKET,S3_LOCATION,app
from upload import upload_file_to_s3,allowed_file,ALLOWED_EXTENSIONS

#connecting with database
client = MongoClient("mongodb://65.2.151.220:27017")

#getting the table (collection)
#format is client.<data-base-name>.<collection-name>
collection=client.userdb.user_collection

#get_data = lambda x : request.args.get(x)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload",methods=["POST"])
def upload_file():
    Name=request.form.get("Name")
    Email_ID=request.form.get("Email-ID")
    file=request.files["user_file"]

    if "user_file" not in request.files:
        return "No user_file key in request.files"
    
    elif file.filename=="":
        return "<br /><br /><center><h2><b><u>Please select a file</u></b></h2></center>"

    elif file and allowed_file(file.filename):
        file.filename=secure_filename(file.filename)
        IST = timezone('Asia/Kolkata')
        date_time=datetime.now(IST).strftime("%d-%m-%Y_%I:%M:%S_%p")
        file_name=file.filename.split(".")
        file_name[0]=file_name[0] + "_" + f"{date_time}"
        file.filename=file_name[0] + "." + file_name[1]
        output=upload_file_to_s3(file,app.config["S3_BUCKET"])
        s3_url=f"{app.config['S3_LOCATION']}{file.filename}"
        doc={
              "Name": Name,
              "Email-ID": Email_ID,
              "Resume": s3_url
             }

        collection.insert_one(doc)
        return f"""<br /><center><h1><u>Your File has <b>Succesfully</b> been Uploaded to <b>S3</b>...</u><h1></center> <br />\
            <a href="{s3_url}">\
            <center><b><h2>click here...<h2></b></center></a>"""
        #return str(output)

    else:
        return redirect("/")

if __name__=="__main__":
    app.run(host = "0.0.0.0", port = 5000)
