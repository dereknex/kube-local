from input.base import Input
from pathlib import Path
import requests
import validators
import re
import hashlib
from urllib.parse import urlparse


default_save_dir = "temp/"
chunk_size = 4096


class HTTPInput(Input):
    save_dir = None
    url = None
    sha256sum = None
    _total_size = 0
    _download_size = 0

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def _ensure_save_dir(self, path) -> str:
        if path is None or path == "":
            path = default_save_dir
        self.save_dir = path
        u = urlparse(self.url)
        prefix = str(u.path).rsplit("/", 1)[0]
        prefix = prefix.strip("/")
        full_path = Path(self.save_dir).joinpath(prefix)
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path

    def _get_filename(self, url, resp) -> str:
        fheader = "Content-Disposition"
        if fheader in resp.headers:
            d = resp.headers[fheader]
            if d is not None:
                filename = re.findall("filename=(.+)", d)[0]
            if filename is not None and filename != "":
                return filename
        return url.split("/")[-1]

    def _get_content_length(self, resp) -> int:
        fheader = "content-length"
        if fheader in resp.headers:
            d = resp.headers[fheader]
            if d is not None:
                return int(d)
        return 0

    def get_save_path(self):
        r = requests.get(self.url, stream=True)
        fname = self._get_filename(self.url, r)
        r.close()

        return Path(self._ensure_save_dir(self.save_dir)).joinpath(fname)

    def download(self) -> bool:
        if not validators.url(self.url):
            raise ValueError(self.url)
        p = self.get_save_path()
        r = requests.get(self.url, stream=True)
        self._total_size = self._get_content_length(r)
        if self.sha256sum is not None:
            sha256_hash = hashlib.sha256()
        with open(p, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                if self.sha256sum is not None:
                    sha256_hash.update(chunk)
                if self._total_size > 0:
                    self._download_size += len(chunk)
                    progress = int(self._download_size * 100 / self._total_size)
                    if self.progress != progress:
                        self.progress = progress
                        self.notify()

            f.close()
        r.close()
        return self.sha256sum == None or sha256_hash.hexdigest() == self.sha256sum
