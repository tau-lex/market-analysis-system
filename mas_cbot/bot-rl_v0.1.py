import time
import logging

from datetime import datetime
import numpy as np

from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from mas_tools.envs import MarketEnv
from mas_tools.markets import VirtualMarket, AbstractMarket
from mas_tools.api import Binance
from mas_tools.models import simple_model
from mas_tools.tools import get_script_dir


#=============================================================================#
#   G L O B A L   V A R I A B L E S                                           #
#=============================================================================#
MY_API_KEY = '---'
MY_API_SECRET = '---'

ENV_NAME = 'Binance_2'

SLEEP = 1
TRAIN = True


if __name__ == "__main__":
    api = Binance(API_KEY=MY_API_KEY, API_SECRET=MY_API_SECRET)

    connector = VirtualMarket(api, symbols=['ETHUSDT'], periods='5m',
                              balance=1000.0, lot_size=0.01)

    market = MarketEnv(connector)

    observation_shape = market.observation_space.shape
    nb_actions = market.action_space.n
    print('state =', observation_shape, '| actions =', nb_actions)

    model = simple_model(observation_shape, nb_actions, 'relu')

    memory = SequentialMemory(limit=10000, window_length=1)
    policy = BoltzmannQPolicy()

    agent = DQNAgent(model=model, nb_actions=nb_actions,
                     memory=memory, nb_steps_warmup=1000,
                     target_model_update=1e-2, policy=policy,
                     # enable_dueling_network=True, dueling_type='avg'
                    )
    agent.compile(Adam(lr=1e-3), metrics=['mae'])

    # agent.load_weights('dqn_{}_weights.h5f'.format(ENV_NAME))
    # agent.fit(market, nb_steps=100000, visualize=False, verbose=2)
    # agent.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
    # agent.test(market, nb_episodes=5, visualize=False)

    observation = market.reset()
    tickcount = 0

    if TRAIN:
        agent.training = True

    while True:
        try:
            # TODO add callbacks?

            action = agent.forward(observation)
            # TODO actions for multy symbols market
            action = np.argmax(action)

            observation, reward, done, info = market.step([action])

            if tickcount % 10 == 0:
                reward = -1
                
            agent.backward(reward, terminal=done)

            if done:
                observation = market.reset()
                done = False
                print('reset')
            
            print('action: %d | reward: %.2f | balance: %.2f' % \
                    (info['last_action'], reward, info['balance']))

            if tickcount % 100 == 0:
                agent.save_weights('E:/Projects/market-analysis-system/dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
            
            time.sleep(SLEEP)
            tickcount += 1

        except KeyboardInterrupt:
            # We catch keyboard interrupts here so that training can be be safely aborted.
            # This is so common that we've built this right into this function, which ensures that
            # the `on_train_end` method is properly called.
            agent.save_weights('E:/Projects/market-analysis-system/dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
            break

        except ConnectionError as e:
            # log.exception(e)
            pass

        except RuntimeError as e:
            print(e)

        # except Exception as e:
        #     print(e)
        #     # log.exception(e)
        #     break

