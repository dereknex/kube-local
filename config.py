import yaml

class Configuration(yaml.YAMLObject):

    
    auto_clean = True
    local_path = 'temp/'
    inputs = []
    outputs = []
    tasks = []
    
    def __init__(self, yaml_data):
        d = yaml.loader.construct_mapping(
        