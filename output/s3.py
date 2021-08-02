from output.base import Output
from minio import Minio
from pathlib import Path

class S3Output(Output):
    access_key = None
    access_key_secret = None
    endpoint = None
    bucket = None
    secure = True

    def __init__(self, **kwargs):
       self.__dict__.update(kwargs) 

    def upload(self, local_path, remote_prefix) -> None:
        client = Minio(self.endpoint, self.access_key, self.access_key_secret, secure=self.secure)
        found = client.bucket_exists(self.bucket)
        if not found:
            client.make_bucket(self.bucket)
        filename = Path(local_path).name
        remote_path = Path(remote_prefix).joinpath(filename)
        client.fput_object(self.bucket, remote_path.as_posix(), local_path)
