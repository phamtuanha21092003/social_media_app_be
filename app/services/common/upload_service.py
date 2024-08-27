import os
import boto3
from app.common.errors import UBadRequest



class UploadService():
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF", "WEBP", "JP2"]
    CDN = os.getenv('S3_CDN')
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
    S3_KEY = os.getenv('S3_KEY')
    S3_SECRET = os.getenv('S3_SECRET')
    S3_BUCKET = os.getenv('S3_BUCKET')


    def upload_to_s3(self, file, suffix: str) -> str:
        if file.filename == "":
            raise UBadRequest("No filename")

        if not ("." in file.filename):
            raise UBadRequest("File extension not found")

        extension = file.filename.rsplit(".", 1)[1]

        if not self.__allowed_image(extension):
            raise UBadRequest("That file extension is not allowed")

        s3 = boto3.client('s3', endpoint_url=UploadService.S3_ENDPOINT_URL, aws_access_key_id=UploadService.S3_KEY, aws_secret_access_key=UploadService.S3_SECRET)

        s3.upload_fileobj(file, UploadService.S3_BUCKET, f"{suffix}.{extension}", ExtraArgs={ "ACL": "public-read", "ContentType": file.content_type, "CacheControl": "max-age=31536000" })

        return f"{UploadService.CDN}{suffix}.{extension}"


    def __allowed_image(self, extension: str) -> bool:
        return extension.upper() in UploadService.ALLOWED_IMAGE_EXTENSIONS


