import time
import logging

from datetime import datetime

from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from mas_tools.envs import MarketEnv
from mas_tools.markets import AbstractMarket
from mas_tools.api import Binance
from mas_tools.models import simple_model


#=============================================================================#
#   G L O B A L   V A R I A B L E S                                           #
#=============================================================================#
MY_API_KEY = '---'
MY_API_SECRET = '---'

ENV_NAME = 'Binance'


if __name__ == "__main__":
    api = Binance(API_KEY=MY_API_KEY, API_SECRET=MY_API_SECRET)

    connector = AbstractMarket(api, symbols=['ETHUSDT'], periods='5m', balance=1000.0)
    print('connector shape', connector.shape)

    market = MarketEnv(connector)

    observation_shape = market.observation_space.shape
    nb_actions = market.action_space.n
    print('state =', observation_shape, '| actions =', nb_actions)

    model = simple_model(observation_shape, nb_actions)

    memory = SequentialMemory(limit=10000, window_length=1)
    policy = BoltzmannQPolicy()

    agent = DQNAgent(model=model, nb_actions=nb_actions,
                     memory=memory, nb_steps_warmup=1000,
                     target_model_update=1e-2, policy=policy,
                     # enable_dueling_network=True, dueling_type='avg'
                    )
    agent.compile(Adam(lr=1e-3), metrics=['mae'])

    # agent.load_weights('dqn_{}_weights.h5f'.format(ENV_NAME))

    agent.fit(market, nb_steps=100000, visualize=False, verbose=2)

    agent.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

    agent.test(market, nb_episodes=5, visualize=False)

