from threading import Thread
from output.base import Output
from minio import Minio

from pathlib import Path
from informer import Informer


class Progress(Thread):
    def __init__(self, handle):
        Thread.__init__(self)
        self.total_length = 0
        self.object_name = None
        self.handle = handle

        self.current_size = 0

    def set_meta(self, total_length, object_name):
        """
        Metadata settings for the object. This method called before uploading
        object
        :param total_length: Total length of object.
        :param object_name: Object name to be showed.
        """
        self.total_length = total_length
        self.object_name = object_name

    def update(self, size):
        """
        Update object size to be showed. This method called while uploading
        :param size: Object size to be showed. The object size should be in
                     bytes.
        """
        if not isinstance(size, int):
            raise ValueError("{} type can not be displayed. " "Please change it to Int.".format(type(size)))
        if self.handle is None:
            return
        self.current_size += size
        if self.total_length > 0:
            progress = int(self.current_size * 100 / self.total_length)
            if progress != self.handle.progress:
                self.handle.progress = progress


class S3Output(Output):
    access_key = None
    access_key_secret = None
    endpoint = None
    bucket = None
    secure = True

    local_path = None
    remote_prefix = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def upload(self) -> None:
        client = Minio(self.endpoint, self.access_key, self.access_key_secret, secure=self.secure)
        found = client.bucket_exists(self.bucket)
        if not found:
            client.make_bucket(self.bucket)
        filename = Path(self.local_path).name
        remote_path = Path(self.remote_prefix).joinpath(filename)
        progress = None
        if len(self._observers) > 0:
            progress = Progress(self)

        client.fput_object(self.bucket, remote_path.as_posix(), self.local_path, progress=progress)
