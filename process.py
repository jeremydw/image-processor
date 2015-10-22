#!/usr/bin/env python

import sys
sys.path.insert(0, 'lib')

from PIL import Image
from psd_tools import PSDImage
import os
import yaml


CONFIG_FILE = 'config.yaml.txt'
CONFIG = yaml.load(open(CONFIG_FILE))
INPUT_PATH = CONFIG['input']
OUT_DIR = CONFIG['out_dir']


def process(rule):
  for fmt in rule['formats']:
    size = rule['size']
    path = os.path.join(OUT_DIR, rule['name'] + '.' + fmt.lower())
    if INPUT_PATH.endswith('psd'):
      psd = PSDImage.load(INPUT_PATH)
      image = psd.as_PIL()
    else:
      image = Image.open(INPUT_PATH)
    image.thumbnail(size, Image.ANTIALIAS)
    background_color = rule.get('background', (255, 255, 255, 1))
    if background_color:
      if rule.get('trim') not in (None, False):
        size = image.size
      else:
        size = size
      background = Image.new('RGBA', size, tuple(background_color))
      offset = (max((size[0] - image.size[0]) / 2, 0), max((size[1] - image.size[1]) / 2, 0))
      image.load()  # Required for split.
      if INPUT_PATH.endswith('png'):
        background.paste(image, offset, mask=image.split()[3])
      else:
        background.paste(image, offset)
      image = background
    image.save(
        path,
        fmt,
        quality=rule.get('quality', 100),
        optimize=True,
        progressive=True)
    print 'Saved: {}'.format(path)


def main():
  if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)
  rules = CONFIG['rules']
  for rule in rules:
    process(rule)


if __name__ == '__main__':
  main()
