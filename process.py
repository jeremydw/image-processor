#!/usr/bin/env python

import sys
sys.path.insert(0, 'lib')

from PIL import Image
import os
import yaml


CONFIG_FILE = 'config.yaml'
CONFIG = yaml.load(open(CONFIG_FILE))
INPUT_PATH = CONFIG['input']
OUT_DIR = CONFIG['out_dir']


def process(rule):
  pass


def main():
  if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)
  rules = CONFIG['rules']
  for rule in rules:
    process(rule)


if __name__ == '__main__':
  main()
