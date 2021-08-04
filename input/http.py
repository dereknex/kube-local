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
    url = None
    sha256sum = None

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

    def download(self) -> bool:
        if not validators.url(self.url):
            raise ValueError(self.url)
        self.local_path = HTTPInput._ensure_local_path(self.local_path)
        r = requests.get(self.url, stream=True)
        fname = self._get_filename(self.url, r)
        p = Path(self.local_path).joinpath(fname)
        if self.sha256sum is not None:
            sha256_hash = hashlib.sha256()
        with open(p, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                if self.sha256sum is not None:
                    sha256_hash.update(chunk)
            f.close()
        return self.sha256sum == None or sha256_hash.hexdigest() == self.sha256sum
