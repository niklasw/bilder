from pathlib import Path
from datetime import datetime
import imghdr
import sys, os
from itertools import cycle
from collections import UserList

class Image_display_container(UserList):
    '''A list of 3 image paths, previous, current and next'''

    def __init__(self, *args):
        super().__init__(*args)
        for i in range(len(self)):
            self[i] = Path(self[i])

nxti = lambda n,i: 0 if i>n-2 else i+1
prvi = lambda n,i: n if i<0 else i-1

class directory:

    def __init__(self, path, config):
        self.ignored = config.get.photos.ignore
        self.extensions = config.get.photos.extensions
        self.conf = config
        self.cd(path)

    def cd(self, path):
        self.path=Path(path)
        self.folders = sorted(self.get_folders())
        self.images = sorted(self.get_images())

    def lcd(self, name):
        target = Path(self.path, name)
        if target.is_dir():
            self.cd(target.resolve())

    def get_folders(self):
        dir_iter = (f for f in self.path.iterdir() if f.is_dir())
        for f in dir_iter:
            if f.name not in self.ignored:
                yield f

    def get_images(self):
        file_iter = (f for f in self.path.iterdir() if f.is_file())
        for f in file_iter:
            if imghdr.what(f) in self.extensions:
                yield f

    def get_relative_path(self, path):
        return Path(path).relative_to(self.conf.get.photos.root)

    def get_thumb_path(self, path):
        return Path(self.conf.get.thumbs.root,self.get_relative_path(path))

    def generate_thumbs(self, height=300, force=False):
        for img in self.images:
            thumb = self.get_thumb_path(img)
            if thumb.exists() and not force:
                print(f'Already got thumb {thumb}')
            else:
                if not thumb.parent.exists():
                    thumb.parent.mkdir(parents=True, exist_ok=True)
                make_thumb(img, thumb, height)

    @staticmethod
    def index(name, collection, default=0):
        if name in collection:
            return collection.index(name)
        else:
            return default

    def index_of_image(self, image_name, default=-1):
        return self.index(image_name, self.images, default=default)
    
    def index_of_folder(self, folder_name, default=-1):
        return self.index(folder_name, self.folders, default=default)

    def image_neighbours(self, current_image):
        n_photos = len(self.images)
        index = self.index_of_image(current_image)
        if index < 0:
            return '/static/images/not_found.jpg'
        nexti = index + 1 if index < n_photos - 1 else 0
        previ = index - 1 if index > 0 else n_photos - 1
        return (self.images[previ], self.images[nexti])
   
from PIL import Image, ImageOps
def make_thumb(img, thumb_path, height=300, failedImage=None):
    try:
        image = Image.open(img)
        image = ImageOps.exif_transpose(image)
    except:
        print(f'Warning: Could not generate thumb for {{img}}')
        image = Image.new('RGB', (300,300), (3,3,3))
    w,h = image.size
    aspect = w/h
    width = int(aspect*height)
    thumbnail = image.resize((width, height))
    print(f'generating thumb {thumb_path} from {img}. '
          f'Size: {(w,h)} -> {(width, height)}')
    # Some images have .THM extension, but are jpegs.
    if thumb_path.suffix.upper() == '.THM':
        thumb_path = thumb_path.with_suffix('.jpg')
    thumbnail.save(thumb_path)

def test1():
    from config import Config
    if not Path('config.json').exists():
        print('No config.json found. Run this from correct dir')
    
    cfg = Config('config.json')
    curdir = directory(cfg.get.photos.root, cfg)
    print(curdir.path)
    curdir.lcd('piasFjallnas')
    print(curdir.path)
    for item in curdir.get_folders():
        print(item)
    for item in curdir.get_images():
        print(item)



def make_thumbs():
    from config import Config

    if not Path('config.json').exists():
        print('No config.json found. Run this from correct dir')
    
    cfg = Config('config.json')
    curdir = directory(cfg.get.photos.root, cfg)
    curdir.generate_thumbs(force=False)

    for item in Path(cfg.get.photos.root).rglob('*'):
        if item.is_dir() and item.name not in cfg.get.photos.ignore:
            curdir.cd(item)
            print('Entering folder', item)
            curdir.generate_thumbs(force=False)

def list_folders():
    from config import Config

    if not Path('config.json').exists():
        print('No config.json found. Run this from correct dir')
    
    cfg = Config('config.json')
    curdir = directory(cfg.get.photos.root, cfg)

    for folder in curdir.folders:
        print(folder)
 
def count_images():
    from config import Config

    if not Path('config.json').exists():
        print('No config.json found. Run this from correct dir')
    
    cfg = Config('config.json')
    curdir = directory(cfg.get.photos.root, cfg)

    nImages = 0

    for folder in curdir.folders:
        for item in (f for f in folder.rglob('*') if f.is_dir()):
            curdir.cd(item)
            nImages += len(curdir.images)
    print(nImages)



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'thumbs':
            make_thumbs()
        elif sys.argv[1] == 'folders':
            list_folders()
        elif sys.argv[1] == 'count':
            count_images()
    else:
        test1()


