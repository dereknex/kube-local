from informer import Informer


class Input(Informer):
    name = ""

    data = {}

    def download(self) -> None:
        raise NotImplementedError()
