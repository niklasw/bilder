import json2
from pathlib import Path
from dotted.collection import DottedCollection

class Config:

    def __init__(self, config_file):
        self.file_name = config_file
        with open(config_file,'rb') as fp:
            self.get = DottedCollection.factory(json2.load(fp))

    def root(self):
        return Path(self.get.photos.root)

if __name__ == '__main__':
    C = Config('config.json')

    print(C.root())
    print(C.get.photos.root)


