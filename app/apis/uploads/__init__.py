from flask import Blueprint, request
from flask_restful import Api, Resource
from app.services.common import UploadService
import hashlib
from flask_jwt_extended import jwt_required


upload_blueprint = Blueprint("upload_blueprint", __name__, url_prefix="/uploads")
upload_api = Api(upload_blueprint)



class Upload(Resource):
    def __init__(self) -> None:
        self.upload_service = UploadService()


    @jwt_required()
    def post(self):
        files = request.files.getlist('files')
        urls  = []
        errors = []

        for file in files:
            try:
                suffix = self.__create_suffix(file)

                url = self.upload_service.upload_to_s3(file=file, suffix=suffix)

                urls.append(url)

            except Exception as e:
                errors.append(str(e))

        return { 'message': 'File uploaded successfully', 'urls': urls, 'errors': errors }


    def __create_suffix(self, file):
        import datetime

        hash_file = hashlib.md5("{}{}".format(file.read(), datetime.datetime.now()).encode('utf-8')).hexdigest()

        file.seek(0)

        return '/files/{}'.format(hash_file)


upload_api.add_resource(
    Upload, ''
)