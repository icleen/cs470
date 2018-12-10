import torch
import numpy as np
import gc

from reversi_env import ReversiEnv
from model import ReversiNet
from utils import *

class RolloutFactory(object):
  """docstring for RolloutFactory."""
  def __init__(self, policy_net, env_samples, gamma=0.9):
    super(RolloutFactory, self).__init__()
    self.env = ReversiEnv()
    self.policy_net = policy_net
    self.env_samples = env_samples
    self.gamma = gamma
    self.device = torch.device("cpu")
    if torch.cuda.is_available():
      self.device = torch.device("cuda")


  def get_rollouts(self):
    rollouts = []
    self.policy_net.eval()
    for _ in range(self.env_samples):
      rollout = self.run_episode()
      rollouts.append(rollout)
      gc.collect()
    return rollouts

  def run_episode(self):
    # don't forget to reset the environment at the beginning of each episode!
    # rollout for a certain number of steps!
    env = self.env
    rounds = env.length()
    rollout = []
    state, turn = env.reset()
    actions = env.action_space()
    done = False
    for i in range(rounds):
      in_state = prepare_board(state, 1).to(self.device)
      probs, _ = self.policy_net(in_state)
      probs = probs.squeeze().cpu().detach().numpy()
      action = sample(probs, actions)
      s_prime, t_prime, reward = env.step(action)
      actions = env.action_space()
      if reward != 0:
        done = True

      rollout.append([state, turn, probs])
      state, turn = s_prime, t_prime
      # print(state)
      # input('waiting')
      if done:
        break
    print('winner: {}'.format(reward))
    # calculate returns
    value = 0.0
    for i in range(len(rollout)):
      state, turn, probs = rollout[i]
      rollout[i] = [state*turn, probs, reward*turn]
    return rollout

if __name__ == '__main__':

  net = ReversiNet()
  factory = RolloutFactory(net, 1)
  rolls = factory.get_rollouts()
  for r in rolls[0]:
    print(r[-1])
  print(rolls[0][-1][0])
