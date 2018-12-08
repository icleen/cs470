import sys
import os
from os.path import join as opjoin
import json
import gc
import numpy as np
from random import randint

import torch

from tqdm import tqdm
import matplotlib.pyplot as plt

from dataset import ExperienceDataset
from model import ReversiNet
from reversi_env import ReversiEnv
from rollout_factory import RolloutFactory
from trainer import Trainer


def main():
  if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' config')
    exit(0)

  itr = None
  if len(sys.argv) > 2:
    itr = int(sys.argv[2])

  config = sys.argv[1]
  tester = Trainer(config)
  tester.read_in(itr)
  acc = tester.test()
  print('Win rate:', acc)

if __name__ == '__main__':
  main()
