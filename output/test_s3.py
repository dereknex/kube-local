import unittest
from output.s3 import S3Output
from pathlib import Path


class TestS3Output(unittest.TestCase):
    def test_upload(self):
        o = S3Output()
        o.endpoint = "localhost:9000"
        o.access_key = "minioadmin"
        o.access_key_secret = "minioadmin"
        o.bucket = "test"
        o.secure = False
        p = Path("bar.txt")
        p.write_text('Text file contents')
        local_path = p.absolute().as_posix()
        o.upload(local_path, "foo/")
        p.unlink()
