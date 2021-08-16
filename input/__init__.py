from input.http import HTTPInput
from input.base import Input
from input.docker import DockerInput


class Factory(object):
    @staticmethod
    def create(kind, config) -> Input:
        if kind == "http":
            return HTTPInput(**config)
        elif kind == "docker":
            return DockerInput(**config)
        raise Exception("Unknown input kind: {}".format(kind))
