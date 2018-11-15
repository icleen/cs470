import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from agent import Agent


def test_priors(agents, correct_state):
  actions = [agent.action() for agent in agents]
  asum = np.sum([1 for act in actions if act == correct_state])
  return actions, asum


def test_agents(agents, correct_state):
  actions = []
  for agent in agents:
    actions.append(agent.action(actions))

  asum = np.sum([1 for act in actions if act == correct_state])
  return actions, asum


def test_conf(conf=0.9):
  # print('conf: {}'.format(conf))
  correct_state = 1
  good = 0.9
  moderate = 0.75
  bad = 0.4

  n_agents = 10
  good_agents = [Agent(conf=conf, aqual=(correct_state, good)) for n in range(n_agents)]
  mod_agents = [Agent(conf=conf, aqual=(correct_state, moderate)) for n in range(n_agents)]
  bad_agents = [Agent(conf=conf, aqual=(correct_state, bad)) for n in range(n_agents)]

  """test for each agent just choosing based on their own priors"""
  good_actions, good_sum = test_priors(good_agents, correct_state)
  mod_actions, mod_sum = test_priors(mod_agents, correct_state)
  bad_actions, bad_sum = test_priors(bad_agents, correct_state)
  # print('Choosing just based on on priors:')
  # print('good: {}, mod: {}, bad: {}'.format(good_actions, mod_actions, bad_actions))
  # print('good: {}, mod: {}, bad: {}'.format(good_sum, mod_sum, bad_sum))

  """test for each agent in information cascade"""
  good_actions, good_sum = test_agents(good_agents, correct_state)
  mod_actions, mod_sum = test_agents(mod_agents, correct_state)
  bad_actions, bad_sum = test_agents(bad_agents, correct_state)
  # print('Information Cascade (conf: {}):'.format(conf))
  # print('good: {}, mod: {}, bad: {}'.format(good_actions, mod_actions, bad_actions))
  # print('good: {}, mod: {}, bad: {}'.format(good_sum, mod_sum, bad_sum))

  # print()
  return np.array([float(good_sum)/n_agents, float(mod_sum)/n_agents, float(bad_sum)/n_agents])


def test_mixed(conf=0.5):
  # print('conf: {}'.format(conf))
  correct_state = 1
  good = 0.9
  moderate = 0.75
  bad = 0.4

  n_agents = 10
  good_agents = [Agent(conf=conf, aqual=(correct_state, good)) for n in range(2)]
  good_agents += [Agent(conf=conf, aqual=(correct_state, bad)) for n in range(n_agents-2)]

  mod_agents = [Agent(conf=conf, aqual=(correct_state, moderate)) for n in range(2)]
  mod_agents += [Agent(conf=conf, aqual=(correct_state, bad)) for n in range(n_agents-2)]

  mod2_agents = [Agent(conf=conf, aqual=(correct_state, moderate)) for n in range(2)]
  mod2_agents += [Agent(conf=conf, aqual=(correct_state, good)) for n in range(n_agents-2)]

  bad_agents = [Agent(conf=conf, aqual=(correct_state, bad)) for n in range(2)]
  bad_agents += [Agent(conf=conf, aqual=(correct_state, good)) for n in range(n_agents-2)]

  """test for each agent just choosing based on their own priors"""
  good_actions, good_sum = test_priors(good_agents, correct_state)
  mod_actions, mod_sum = test_priors(mod_agents, correct_state)
  mod2_actions, mod2_sum = test_priors(mod2_agents, correct_state)
  bad_actions, bad_sum = test_priors(bad_agents, correct_state)
  # print('Choosing just based on on priors:')
  # print('good: {}, mod: {}, mod with good: {}, bad: {}'
    # .format(good_actions, mod_actions, mod2_actions, bad_actions))
  # print('good: {}, mod: {}, mod with good: {}, bad: {}'
    # .format(good_sum, mod_sum, mod2_sum, bad_sum))

  """test for each agent in information cascade"""
  good_actions, good_sum = test_agents(good_agents, correct_state)
  mod_actions, mod_sum = test_agents(mod_agents, correct_state)
  mod2_actions, mod2_sum = test_agents(mod2_agents, correct_state)
  bad_actions, bad_sum = test_agents(bad_agents, correct_state)
  # print('information Cascade:')
  # print('good: {}, mod: {}, mod with good: {}, bad: {}'
    # .format(good_actions, mod_actions, mod2_actions, bad_actions))
  # print('good: {}, mod: {}, mod with good: {}, bad: {}'
    # .format(good_sum, mod_sum, mod2_sum, bad_sum))

  # print()
  return np.array([float(good_sum)/n_agents, float(mod_sum)/n_agents, float(mod2_sum)/n_agents, float(bad_sum)/n_agents])


def test_utils(conf=0.5, utils=[1,1,1]):
  # print('conf: {}'.format(conf))
  correct_state = 1
  good = 0.9
  moderate = 0.75
  bad = 0.4

  n_agents = 10
  good_agents = [Agent(conf=conf, aqual=(correct_state, good), utils=utils) for n in range(n_agents)]

  goodbad_agents = [Agent(conf=conf, aqual=(correct_state, good), utils=utils) for n in range(2)]
  goodbad_agents += [Agent(conf=conf, aqual=(correct_state, bad), utils=utils) for n in range(n_agents-2)]

  modbad_agents = [Agent(conf=conf, aqual=(correct_state, moderate), utils=utils) for n in range(2)]
  modbad_agents += [Agent(conf=conf, aqual=(correct_state, bad), utils=utils) for n in range(n_agents-2)]

  mod_agents = [Agent(conf=conf, aqual=(correct_state, moderate), utils=utils) for n in range(n_agents)]

  modgood_agents = [Agent(conf=conf, aqual=(correct_state, moderate), utils=utils) for n in range(2)]
  modgood_agents += [Agent(conf=conf, aqual=(correct_state, good), utils=utils) for n in range(n_agents-2)]

  badgood_agents = [Agent(conf=conf, aqual=(correct_state, bad), utils=utils) for n in range(2)]
  badgood_agents += [Agent(conf=conf, aqual=(correct_state, good), utils=utils) for n in range(n_agents-2)]

  bad_agents = [Agent(conf=conf, aqual=(correct_state, bad), utils=utils) for n in range(n_agents)]

  """test for each agent in information cascade"""
  good_actions, good_sum = test_agents(good_agents, correct_state)
  goodbad_actions, goodbad_sum = test_agents(goodbad_agents, correct_state)
  modbad_actions, modbad_sum = test_agents(modbad_agents, correct_state)
  mod_actions, mod_sum = test_agents(mod_agents, correct_state)
  modgood_actions, modgood_sum = test_agents(modgood_agents, correct_state)
  badgood_actions, badgood_sum = test_agents(badgood_agents, correct_state)
  bad_actions, bad_sum = test_agents(bad_agents, correct_state)

  sums = np.array([good_sum, goodbad_sum, modbad_sum, mod_sum, modgood_sum, badgood_sum, bad_sum], dtype=np.float)
  sums /= n_agents
  # print()
  return np.array([sums[0], sums[3], sums[6]])

def main():
  confs = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
  utils = [[1, 1, 1], [3, 10, 2], [5, 10, 1], [7, 8, 2],
            [8, 7, 2], [10, 5, 1], [10, 3, 2], [3, 2, 10], [10, 1, 5]]
  tests = 100

  means = np.zeros((len(utils), 3))
  for u, util in enumerate(utils):
    for t in range(tests):
      means[u] += test_utils(conf=0.4, utils=util)
  means /= tests
  print(means.T)

  plt.bar(range(len(utils)*3), means.flatten())
  for m, mean in enumerate(means):
    plt.bar(range(m*3, m*3+1), mean)

  plt.xlabel('sets of agents')
  plt.ylabel('percent of agents choosing correct state')
  plt.savefig('info_graph.png')
  # plt.show()


  # means = np.zeros((len(confs), 7))
  # for c, conf in enumerate(confs):
  #   for t in range(tests):
  #     means[c] += test_utils(conf)
  # means /= tests
  # print(means.T)

  # means = np.zeros((len(confs), 3))
  # for c, conf in enumerate(confs):
  #   for t in range(tests):
  #     means[c] += test_conf(conf)
  # means /= tests
  # print(means.T)
  #
  # print('\n********************\n')
  #
  # means = np.zeros((len(confs), 4))
  # for c, conf in enumerate(confs):
  #   for t in range(tests):
  #     means[c] += test_mixed(conf)
  # means /= tests
  # print(means.T)

if __name__ == '__main__':
  main()
