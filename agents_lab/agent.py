import os
import sys
import numpy as np


"""
There are three true states of the world, {s1, s2, s3}.
s1 is defined as there being water are location one
and not at location two or three.  s2 and s3 are defined similarly.

The actions each agent can make are defined as {a1, a2, a3}.
a1 is defined as an agent going to location 1 to get water.
"""

class Agent(object):
  """
  confidence denotes the confidence the agent has in the other agents
  aqual denotes the quality of the agent's information; it is a tuple
  denoting which state is correct and how high the probability
  should be that the agent has that state as it's highest probability
  """
  def __init__(self, conf=0.9, aqual=(1, 0.75), utils=[1, 1, 1]):
    super(Agent, self).__init__()

    states = [0, 1, 2]
    actions = [0, 1, 2]
    self.states = states
    self.actions = actions

    doubt = (1-conf)/(len(states)-1)
    likel = np.zeros((len(actions), len(states)))
    for i in range(len(actions)):
      for j in range(len(states)):
        if i == j:
          likel[i,j] = conf
        else:
          likel[i,j] = doubt
    self.likel = likel

    priors = np.random.rand(len(actions))
    priors[aqual[0]] = aqual[1]
    priors /= np.sum(priors)
    self.priors = priors

    self.utils = np.array(utils)

  def action(self, prev_actions=[]):
    if prev_actions == []:
      # print('posterior: {}'.format(self.priors))
      return np.argmax( [self.priors[s] for s in self.states] )

    # post = 0
    posts = self.priors
    utils = []
    action = 0
    for a in prev_actions:
      posts = np.array([self.likel[a, s] * posts[s] for s in self.states])
      posts /= np.sum(posts)
      utils = self.utils * posts
      action = np.argmax(utils)
      # post = posts[action]

    # print('posterior: {}'.format(posts))
    return action
