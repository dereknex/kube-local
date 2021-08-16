from output.s3 import S3Output
from output.base import Output
from output.docker import DockerOutput


class Factory:
    @staticmethod
    def create(type, config):
        if type == "s3":
            return S3Output(**config)
        elif type == "docker":
            return DockerOutput(**config)
        else:
            raise Exception("Invalid output kind: " + type)
