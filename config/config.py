import yaml

# from input import HTTPInput, DockerInput
# from output import S3Output, DockerOutput

# _inputs = {"http": HTTPInput, "docker": DockerInput}
_inputs = ["http", "docker"]
# _outputs = {"s3": S3Output, "docker": DockerOutput}
_outputs = ["s3", "docker"]


class Configuration:

    auto_clean = True
    local_path = "temp/"
    inputs = {}
    outputs = {}
    tasks = []
    _dict = {}

    def __init__(self, filename):
        with open(filename, encoding="UTF-8") as yaml_file:
            self._dict = yaml.safe_load(yaml_file)
            yaml_file.close()
        if self._dict is None:
            raise ValueError("%s is invaild", filename)
        if "auto_clean" in self._dict:
            self.auto_clean = self._dict["auto_clean"]
        if "local_path" in self._dict:
            self.local_path = self._dict["local_path"]
        if "inputs" in self._dict:
            self._load_inputs(self._dict["inputs"])
        if "outputs" in self._dict:
            self._load_outpus(self._dict["outputs"])
        if "tasks" in self._dict:
            self._load_tasks(self._dict["tasks"])

    def _load_inputs(self, node):
        if node is None:
            return
        for n in node:
            if n["kind"] not in _inputs:
                raise ValueError("%s is not supported", n["kind"])
            # c = _inputs[i["kind"]]
            # i = c(**i)
            self.inputs[n["name"]] = n

    def _load_outpus(self, node):
        if node is None:
            return
        for n in node:
            # c = _outputs[i["kind"]]
            # o = c(**i)
            if n["kind"] not in _outputs:
                raise ValueError("%s is not supported", n["kind"])
            self.outputs[n["name"]] = n

    def _load_tasks(self, node):
        if node is None:
            return
        self.tasks = node
