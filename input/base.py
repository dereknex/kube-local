from informer import Informer


class Input(Informer):
    name = ""

    def get_download_path(self):
        raise NotImplementedError()

    def download(self) -> None:
        raise NotImplementedError()
