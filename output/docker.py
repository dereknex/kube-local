from informer import Status
import docker
from output.base import Output
import json


class DockerOutput(Output):
    source_name = None
    image = None
    platform = None
    name = None
    username = None
    password = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.client = docker.from_env()

    def _parse_response(self, response):
        if not isinstance(response, dict):
            response = json.loads(response)

        if "error" in response:
            self._status = Status.ERROR
            self._message = response["error"]
            self.notify()
            return
        if "progressDetail" in response:
            if "current" in response["progressDetail"]:
                self._status = Status.IN_PROGRESS
                current = response["progressDetail"]["current"]
                total = response["progressDetail"]["total"]
                self._progress = int(current / total * 100)
                self.notify()

    def upload(self) -> None:
        self._status = Status.IN_PROGRESS
        self._progress = 0
        self.notify()

        source_image = self.client.images.get(self.source_name)
        source_image.platform = self.platform
        target_registry, tag = self.image.rsplit(":", 1)
        source_image.tag(target_registry, tag=tag)
        for line in self.client.images.push(
            self.image, stream=True, decode=True, auth_config={"username": self.username, "password": self.password}
        ):
            self._parse_response(line)
        self._status = Status.DONE
        self._progress = 100
        self.notify()
