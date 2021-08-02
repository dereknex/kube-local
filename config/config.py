import yaml
from input import HTTPInput
from output import S3Output

_inputs = {'http':HTTPInput}
_outputs = {'s3': S3Output}

class Configuration:

    auto_clean = True
    local_path = "temp/"
    inputs = []
    outputs = []
    tasks = []
    _dict = {}

    def __init__(self, filename):
        self._dict = yaml.safe_load(open(filename, "r"))
        if self._dict is None:
            raise ValueError("%s is invaild", filename)
        if "auto_clean" in self._dict:
            self.auto_clean = self._dict["auto_clean"]
        if "local_path" in self._dict:
            self.local_path = self._dict["local_path"]
        if "inputs" in self._dict:
            self._load_inputs(self._dict["inputs"])
        if 'outputs' in self._dict:
            self._load_outpus(self._dict['outputs'])

    def _load_inputs(self, node):
        if node is None:
            return
        for i in node:
            c = _inputs[i['type']]
            i = c(**i)
            self.inputs.append(i)

    def _load_outpus(self, node):
        if node is None:
            return
        for i in node:
            c = _outputs[i['type']]
            o = c(**i)
            self.outputs.append(o)
