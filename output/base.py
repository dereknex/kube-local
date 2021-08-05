from informer import Informer


class Output(Informer):
    def upload(self) -> None:
        raise NotImplementedError()
