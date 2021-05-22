import os
from flask import Flask

S3_BUCKET=os.environ.get("S3_BUCKET_NAME")
S3_LOCATION=f"http://{S3_BUCKET}.s3.amazonaws.com/"

app=Flask(__name__)
app.config.from_object("config")

DEBUG=True
