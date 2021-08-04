import unittest

from input import http
from pathlib import Path
import requests
import hashlib
import shutil


class TestHTTPInput(unittest.TestCase):
    def test_ensure_local_path(self):
        i = http.HTTPInput()
        # p = i._ensure_local_path(None)
        # self.assertEqual(p, http.default_local_path)
        # Path(p).rmdir()

        p = i._ensure_local_path("test_sync")
        self.assertEqual(p, "test_sync")
        Path(p).rmdir()

    def test_get_filename(self):
        i = http.HTTPInput()
        url = "https://storage.googleapis.com/kubernetes-release/release/v1.21.3/bin/linux/amd64/kubectl"
        resp = requests.Response()
        fname = i._get_filename(url, resp)
        self.assertEqual(fname, "kubectl")
        resp.headers["Content-Disposition"] = "filename=kubectl.tar.gz"
        fname = i._get_filename(url, resp)
        self.assertEqual(fname, "kubectl.tar.gz")

    def test_download(self):
        i = http.HTTPInput()
        checksum = "226ba1072f20e4ff97ee4f94e87bf45538a900a6d9b25399a7ac3dc5a2f3af87"
        url = "https://repo.huaweicloud.com/kubernetes/apt/doc/apt-key.gpg"
        i.url = url
        done = i.download()
        self.assertTrue(done)
        sha256_hash = hashlib.sha256()
        with open("temp/apt-key.gpg", "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            f.close()
        self.assertEqual(sha256_hash.hexdigest(), checksum)
        shutil.rmtree(i.local_path)
