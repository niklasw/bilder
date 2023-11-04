import json2
from pathlib import Path

class Config(dict):

    def __init__(self, config_file):
        self.file_name = config_file
        with open(config_file, 'r') as fp:
            super().__init__(json2.load(fp))

    def path(self, path: str):
        path = path.strip('/')
        elements = path.split('/')
        value = self.get(elements[0])
        for item in elements[1:]:
            value = value.get(item)
        return value

    def root(self):
        return Path(self.path('photos/root'))

if __name__ == '__main__':
    C = Config('config.json')
    print(C.path('/photos/ignore/'))
    print(C.root())

    # print(C.root())
    # print(C.get.photos.root)


