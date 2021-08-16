import unittest
from output.docker import DockerOutput
import docker


class TestDocker(unittest.TestCase):
    def test_upload(self):
        client = docker.from_env()
        client.images.pull("alpine:3", platform="amd64")
        o = DockerOutput()
        o.source_name = "alpine:3"
        o.image = "localhost:5000/alpine:3"
        o.platform = "amd64"
        o.upload()
        remote_image = client.images.get_registry_data("localhost:5000/alpine:3")
        self.assertIsNotNone(remote_image)
