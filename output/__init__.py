from output.s3 import S3Output
from output.base import Output
from output.docker import DockerOutput


class Factory:
    @staticmethod
    def create(kind, config) -> Output:
        if kind == "s3":
            return S3Output(**config)
        elif kind == "docker":
            return DockerOutput(**config)

        raise Exception("Invalid output kind: " + kind)
