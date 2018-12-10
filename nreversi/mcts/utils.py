import torch
import numpy as np

def sample(dist, actions):
  # zero out invalid actions
  dist = dist * actions
  # normalize
  dist = dist / dist.sum()
  # random sample
  action = np.random.choice(dist.shape[0], p=dist)
  return action

def loss_pi(targets, outputs):
  return -torch.sum(targets*outputs)/targets.size()[0]

def loss_v(targets, outputs):
  return torch.sum((targets-outputs.view(-1))**2)/targets.size()[0]

def multinomial_likelihood(dist, idx):
  return dist[range(dist.shape[0]), idx.long()[:, 0]].unsqueeze(1)


def _prepare_numpy(ndarray, device):
    return torch.from_numpy(ndarray).float().unsqueeze(0).to(device)


def _prepare_tensor_batch(tensor, device):
    return tensor.detach().float().to(device)

def prepare_board(board, turn):
  return torch.FloatTensor(board*turn).unsqueeze(0).unsqueeze(0)

def moves_from_tuples(moves, size):
  actions = np.zeros(size*size)
  for mov in moves:
    actions[mov[0]*size+mov[1]] = 1
  return actions
