from informer import Status
import docker
from output.base import Output


class DockerOutput(Output):
    source_name = None
    image = None
    platform = None
    name = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.client = docker.from_env()

    def upload(self) -> None:
        self._status = Status.IN_PROGRESS
        self._progress = 0
        self.notify()
        source_image = self.client.images.get(self.source_name)
        source_image.platform = self.platform
        target_registry, tag = self.image.rsplit(":", 1)
        source_image.tag(target_registry, tag=tag)
        self.client.images.push(self.image)
        self._status = Status.DONE
        self._progress = 100
        self.notify()
