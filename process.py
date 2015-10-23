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


def _get_image():
  if INPUT_PATH.endswith('psd'):
    psd = PSDImage.load(INPUT_PATH)
    return psd.as_PIL()
  else:
    return Image.open(INPUT_PATH)


def _get_size(image, rule):
  if rule.get('trim') not in (None, False):
    return image.size
  return rule['size']


def _get_offset(image, size):
  return (max((size[0] - image.size[0]) / 2, 0),
          max((size[1] - image.size[1]) / 2, 0))


def process(rule):
  for fmt in rule['formats']:
    size = rule['size']
    path = os.path.join(OUT_DIR, rule['name'] + '.' + fmt.lower())
    image = _get_image()
    image.thumbnail(size, Image.ANTIALIAS)
    size = _get_size(image, rule)
    offset = _get_offset(image, size)
    background_color = rule.get('background', (255, 255, 255, 1))
    background = Image.new('RGBA', size, tuple(background_color))
    image.load()  # Required for split.
    mask = image.split()[-1]
    background.paste(image, offset, mask=mask)
    background.save(
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
