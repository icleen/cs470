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
      in_state = torch.FloatTensor(state*turn).unsqueeze(0).unsqueeze(0).to(self.device)
      probs, _ = self.policy_net(in_state)
      probs = probs.squeeze().cpu().detach().numpy()
      action = sample(probs, actions)
      s_prime, turn, reward, done = env.step(action)
      actions = env.action_space()

      rollout.append([state, turn, probs])
      state = s_prime
      if done:
        break
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
