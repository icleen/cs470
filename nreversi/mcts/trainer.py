import sys
import os
from os.path import join as opjoin
import json
import gc
import numpy as np
from random import randint

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.utils import save_image

from tqdm import tqdm
import matplotlib.pyplot as plt

from dataset import ExperienceDataset
from model import ReversiNet
from reversi_env import ReversiEnv
from rollout_factory import RolloutFactory
from utils import *


class Trainer():
  """docstring for Trainer."""
  def __init__(self, config):
    with open(config, 'r') as f:
      config = json.load(f)

    self.epochs = config['train']['epochs']
    self.policy_epochs = config['train']['policy_epochs']
    self.test_iters = config['test']['iters']

    layers = config['model']['layers']
    conv_size = config['model']['conv_size']
    logheat = config['model']['logheat']
    self.net = ReversiNet(hidden_size=conv_size, layers=layers, logheat=logheat)

    env_samples = config['train']['env_samples']
    self.factory = RolloutFactory(self.net, env_samples)

    self.value_loss = nn.MSELoss()

    epsilon = config['train']['epsilon']
    self.ppo_low_bnd = 1 - epsilon
    self.ppo_up_bnd = 1 + epsilon

    lr = config['train']['lr']
    weight_decay = config['train']['weight_decay']
    self.optim = optim.Adam(self.net.parameters(), lr=lr, weight_decay=weight_decay)

    self.plosses = []
    self.vlosses = []
    self.avg_wins = []
    self.stand_time = []

    if torch.cuda.is_available():
      torch.cuda.set_device(1)
      self.net.cuda()
      self.device = torch.device("cuda")
      print("Using GPU")
    else:
      self.device = torch.device("cpu")
      print("No GPU detected")

    self.write_interval = config['model']['write_interval']
    self.train_info_path = config['model']['trainer_save_path']
    self.policy_path = config['model']['policy_save_path'].split('.pt')[0]
    self.graph_path = config['model']['graph_save_path'].split('.png')[0]


  def train(self, itr=0):
    acc = self.test()
    for i in range(self.epochs):
      avg_policy_loss = 0
      avg_val_loss = 0

      rollouts = self.factory.get_rollouts()

      # Update the policy
      experience_dataset = ExperienceDataset(rollouts)
      data_loader = DataLoader(experience_dataset,
                              batch_size=256,
                              shuffle=True,
                              pin_memory=True)
      self.net.train()
      for _ in range(self.policy_epochs):
        avg_policy_loss = 0
        avg_val_loss = 0
        for state, aprob, value in data_loader:
          state = _prepare_tensor_batch(state, self.device).unsqueeze(1)
          aprob = _prepare_tensor_batch(aprob, self.device)
          value = _prepare_tensor_batch(value, self.device).unsqueeze(1)

          # Calculate the ratio term
          pdist, pval = self.net(state)
          policy_loss = loss_pi(aprob, pdist)
          val_loss = loss_v(value, pval)

          # For logging
          avg_val_loss += val_loss.item()
          avg_policy_loss += policy_loss.item()

          # Backpropagate
          self.optim.zero_grad()
          loss = policy_loss + val_loss
          loss.backward()
          self.optim.step()

      # Log info
      avg_val_loss /= len(data_loader)
      avg_val_loss /= self.policy_epochs
      avg_policy_loss /= len(data_loader)
      avg_policy_loss /= self.policy_epochs
      self.vlosses.append(avg_val_loss)
      self.plosses.append(avg_policy_loss)

      if (itr+i) % self.write_interval == 0:
        acc = self.test()
        self.avg_wins.append(acc)
        print(
'itr: % i, avg wins: % 6.2f, value loss: % 6.2f, policy loss: % 6.2f' \
% ((itr+i), acc, avg_val_loss, avg_policy_loss) )
        self.write_out(itr+i)


  def test(self):
    self.net.eval()
    env = ReversiEnv()
    rounds = env.length()//2
    tot_rew = 0
    tot_wins = 0
    runs = self.test_iters

    for _ in range(runs):
      state, turn = env.reset()
      actions = env.action_space()
      done = False
      for i in range(rounds):
        in_state = torch.FloatTensor(state).unsqueeze(0).unsqueeze(0).to(self.device)
        probs, _ = self.net(in_state)
        probs = probs.squeeze().cpu().detach().numpy()
        action = sample(probs, actions)
        state, turn, reward, done = env.step(action)
        actions = env.action_space()
        # print('end p1')
        if done:
          break

        probs = np.ones(actions.shape[0])
        action = sample(probs, actions)
        state, turn, reward, done = env.step(action)
        actions = env.action_space()
        # print('end p2')
        if done:
          break

      # print(reward)
      tot_rew += reward
      if reward > 0:
        tot_wins += 1
      # elif reward == 0:
      #   tot_wins += 1
    tot_rew /= runs
    # print('Avg reward over {} runs: {}'.format(runs, tot_rew))
    # print('Wins: {}/{}: {}'.format(tot_wins, runs, tot_wins/runs))
    return tot_wins/runs

  def read_in(self, itr=None):
    train_info = {}
    train_info = torch.load(self.train_info_path)
    if itr is None:
      itr = train_info['iter']
    self.plosses = train_info['plosses']
    self.vlosses = train_info['vlosses']
    self.avg_wins = train_info['avg_wins']
    self.optim = train_info['optimizer']

    self.net.load_state_dict(torch.load(
      str(self.policy_path + '_' + str(itr) + '.pt') ))
    print('loaded: ' + str(self.policy_path + '_' + str(itr) + '.pt'))

    self.epochs += itr
    return itr

  def write_out(self, itr):
    train_info = {}
    train_info['iter'] = itr
    train_info['plosses'] = self.plosses
    train_info['vlosses'] = self.vlosses
    train_info['avg_wins'] = self.avg_wins
    train_info['optimizer'] = self.optim
    torch.save( train_info, self.train_info_path )

    torch.save( self.net.state_dict(),
      str(self.policy_path + '_' + str(itr) + '.pt') )

    if itr > 2:
      plt.plot(self.vlosses, label='value loss')
      plt.plot(self.plosses, label='policy loss')
      plt.legend()
      plt.xlabel('epochs')
      plt.ylabel('loss')
      plt.savefig(str(self.graph_path + '_loss.png'))
      plt.clf()

      plt.plot(self.avg_wins, label='avg wins')
      plt.legend()
      plt.xlabel('epochs')
      plt.ylabel('rewards')
      plt.savefig(str(self.graph_path + '_wins.png'))
      plt.clf()


  def run(self, cont=False):
    # check to see if we should continue from an existing checkpoint
    # otherwise start from scratch
    if cont:
      itr = self.read_in()
      print('continuing')
      self.train(itr)
    else:
      self.train()

def main():
  if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' config')
    exit(0)

  cont = False
  if len(sys.argv) > 2:
    info = sys.argv[2]
    if info == 'cont':
      cont = True

  config = sys.argv[1]
  trainer = Trainer(config)
  trainer.run(cont=cont)

if __name__ == '__main__':
  main()
