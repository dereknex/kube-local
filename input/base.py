from informer import Informer
class Input(Informer):
    name = ""

    def download(self) -> None:
        raise NotImplementedError()
