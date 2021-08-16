from input.base import Input
from informer import Status
import docker


class DockerInput(Input):
    _client = None
    name = ""
    platform = None
    image = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._client = docker.from_env()

    def download(self) -> None:
        self._status = Status.IN_PROGRESS
        self.notify()
        self._client.images.pull(self.image, platform=self.platform)
        self._status = Status.DONE
        self.notify()
        self.data["source_name"] = self.image
