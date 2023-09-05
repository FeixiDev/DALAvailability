import yaml

class YamlRead:
    def __init__(self):
        self.yaml_info = self.yaml_read()

    def yaml_read(self):
        with open('../config.yaml') as f:
            config = yaml.safe_load(f)
        return config