from informer import Informer


class Output(Informer):
    def set_local_path(self, path: str) -> None:
        raise NotImplementedError()

    def upload(self) -> None:
        raise NotImplementedError()
