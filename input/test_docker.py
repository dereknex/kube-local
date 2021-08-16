from input.docker import DockerInput
import unittest
import docker


class TestDocker(unittest.TestCase):
    def test_download(self):
        i = DockerInput()
        i.image = "k8s.gcr.io/kube-proxy:v1.21.4"
        i.platform = "amd64"
        i.download()
        c = docker.client.from_env()
        images = c.images.list("k8s.gcr.io/kube-proxy:v1.21.4")
        self.assertTrue(len(images) > 0)
