from input.base import Input
from pathlib import Path
import requests
import validators
import re
import hashlib

default_local_path = "temp/"
chunk_size = 128


class HTTPInput(Input):
    local_path = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def _ensure_local_path(path) -> str:
        if path is None or path == "":
            path = default_local_path
        Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def _get_filename(self, url, resp) -> str:
        fheader = "Content-Disposition"
        if fheader in resp.headers:
            d = resp.headers[fheader]
            if d is not None:
                filename = re.findall("filename=(.+)", d)[0]
            if filename is not None and filename != "":
                return filename
        return url.split("/")[-1]

    def download(self, url, sha256sum=None) -> bool:
        if not validators.url(url):
            raise ValueError(url)
        self.local_path = HTTPInput._ensure_local_path(self.local_path)
        r = requests.get(url, stream=True)
        fname = self._get_filename(url, r)
        p = Path(self.local_path).joinpath(fname)
        if sha256sum is not None:
            sha256_hash = hashlib.sha256()
        with open(p, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                if sha256sum is not None:
                    sha256_hash.update(chunk)
            f.close()
        return sha256sum == None or sha256_hash.hexdigest() == sha256sum
