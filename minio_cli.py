from minio import Minio
import enum
from os import getenv

MINIO_ENDPOINT = getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = getenv('MINIO_SECRET_KEY')

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


class BucketName(enum.Enum):
    Code = 'code'


for e in BucketName:
    found = client.bucket_exists(e.value)
    if not found:
        client.make_bucket(e.value)


class MinioClient:

    @staticmethod
    def upload(file_id, file, bucket_name) -> bool:
        content = ContentFile(file.read())
        try:
            client.put_object(
                bucket_name, f'compiled/{file_id}.zip', content, length=len(content)
            )
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_file(file_id, bucket_name):
        try:
            response = client.get_object(bucket_name, f'{file_id}.zip')
            return response.data
        except:
            return None
