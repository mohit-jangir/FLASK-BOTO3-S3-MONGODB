from connect import s3

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file,bucket_name,acl="public-read"):
    try:
        s3.upload_fileobj(
                file,
                bucket_name,
                file.filename,
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file.content_type
                    }
                )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ",e)
        return e

