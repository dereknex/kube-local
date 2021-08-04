import unittest
from output.s3 import S3Output
import tempfile

class TestS3Output(unittest.TestCase):
    def test_upload(self):
        o = S3Output()
        o.endpoint = "localhost:9000"
        o.access_key = "dev_stack"
        o.access_key_secret = "dev_stack"
        o.bucket = "test"
        o.secure = False
        f = tempfile.NamedTemporaryFile()
        f.write(b'Text file contents')
        f.flush()
        o.remote_prefix = "foo/"
        o.local_path = f.name
        o.upload()