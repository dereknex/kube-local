from input import Input
from pathlib import Path
import requests
import validators
import re

default_local_path = "temp/"
chunk_size = 128

class HTTPInput(Input):
    local_path = None

    def _ensure_local_path(self, path) -> str:
        if path is None or path == "":
            path = default_local_path
        Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def _get_filename(self, url, resp) -> str:
        fheader = 'Content-Disposition'
        if fheader in resp.headers:
            d = resp.headers[fheader]
            if d is not None:
                filename = re.findall("filename=(.+)", d)[0]
            if filename is not None and filename != "":
                return filename
        return url.split("/")[-1]

        

    def download(self, url) -> None:
        if not validators.url(url):
            raise ValueError(url)
        self.local_path = self._ensure_local_path(self.local_path)
        r = requests.get(url, stream=True)
        fname = self._get_filename(url, r)
        p = Path(self.local_path).joinpath(fname)
        with open(p, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
            f.close()


        

