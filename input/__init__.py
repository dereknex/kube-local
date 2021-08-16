from input.http import HTTPInput
from input.base import Input
from input.docker import DockerInput


class Factory(object):
    @staticmethod
    def create(type, config) -> Input:
        if type == "http":
            return HTTPInput(**config)
        elif type == "docker":
            return DockerInput(**config)
        else:
            raise Exception("Unknown input kind: {}".format(type))
