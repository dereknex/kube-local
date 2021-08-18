from input.base import Input
from informer import Status
import docker


class DockerInput(Input):
    _client = None
    name = ""
    platform = None
    image = None
    username = None
    password = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._client = docker.from_env()

    def download(self) -> None:
        self._status = Status.IN_PROGRESS
        self._progress = 0
        self.notify()
        self._client.images.pull(
            self.image, platform=self.platform, auth_config={"username": self.username, "password": self.password}
        )
        self._status = Status.DONE
        self._progress = 100
        self.notify()
        self.data["source_name"] = self.image
