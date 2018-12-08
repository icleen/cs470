import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, utils, datasets
from torch.nn.parameter import Parameter
from torch.distributions import Categorical

import pdb
import numpy as np

from reversi_env import ReversiEnv


class ReversiNet(nn.Module):
  """docstring for ReversiNet."""
  def __init__(self, state_size=(1, 8, 8), hidden_size=128,
                    layers=3, logheat=10.0):
    super(ReversiNet, self).__init__()

    self.state_size = state_size
    self.action_size = state_size[1]*state_size[2]
    self.hidden_size = hidden_size
    self.logheat = logheat

    modules = []
    modules.append(nn.Conv2d(state_size[0], hidden_size,
                  kernel_size=3, stride=1, padding=1))
    modules.append(nn.ReLU())
    for n in range(layers):
      modules.append(nn.Conv2d(hidden_size, hidden_size,
                    kernel_size=3, stride=1, padding=1))
      modules.append(nn.BatchNorm2d(hidden_size))
      modules.append(nn.ReLU())
    self.net = nn.Sequential(*modules)

    self.fc_size = state_size[1]*state_size[2]*hidden_size
    modules = []
    modules.append(nn.Linear(self.fc_size, 1024))
    modules.append(nn.BatchNorm1d(1024))
    modules.append(nn.ReLU())
    modules.append(nn.Linear(1024, 512))
    modules.append(nn.BatchNorm1d(512))
    modules.append(nn.ReLU())
    self.fc = nn.Sequential(*modules)

    self.policy = nn.Linear(512, self.action_size)
    self.value = nn.Linear(512, 1)

    self.softmax = nn.Softmax(dim=1)
    self.tanh = nn.Tanh()


  def forward(self, x):
    x = self.net(x)
    x = x.view(-1, self.fc_size)
    x = self.fc(x)


    p = self.policy(x)
    v = self.value(x)
    p = self.softmax(p)
    v = self.tanh(v)
    return p, v


if __name__ == '__main__':

  env = ReversiEnv()
  state = env.reset()
  action_size = env.action_space()
  print('state: {}, action space: {}'.format(state.shape, len(action_size)))
  net = ReversiNet()
  state = torch.FloatTensor(state).unsqueeze(0).unsqueeze(0)
  p, v = net(state)
  print(p.size(), v.size())
