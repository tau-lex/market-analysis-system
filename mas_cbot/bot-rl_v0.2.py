import os
import time
import logging
import requests

from datetime import datetime
import numpy as np

from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from rl.processors import MultiInputProcessor

from mas_tools.api import Binance
from mas_tools.markets import VirtualExchange
from mas_tools.envs import MarketEnv
from mas_tools.models import cnn_model_2in_with_feedback


#=============================================================================#
#   G L O B A L   V A R I A B L E S                                           #
#=============================================================================#
MY_API_KEY = '---'
MY_API_SECRET = '---'

PATH = os.path.dirname(os.path.abspath(__file__))
ENV_NAME = 'cb_Binance_5'

SLEEP = 5
TRAIN = True

logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler("{p}/logs/{fn}.log".format(p=PATH, fn=ENV_NAME)),
                                logging.StreamHandler()]
                    )

log = logging.getLogger()

if __name__ == "__main__":
    api = Binance(API_KEY=MY_API_KEY, API_SECRET=MY_API_SECRET)

    market_conn = VirtualExchange(api, symbols=['ETHUSDT'], period='1m',
                                    balance=1000.0, lot_size=0.1)

    market = MarketEnv(market_conn, True, True)

    observation_shape = market.observation_space.shape
    nb_actions = market.action_space.n
    log.info('State shape = {a} | actions = {b}'.format(a=observation_shape, b=nb_actions))

    limit = observation_shape[1]
    model = cnn_model_2in_with_feedback(
            (limit, 4), (limit, 4),
            market.feedback_shape, nb_actions, 'softmax')

    memory = SequentialMemory(limit=10000, window_length=1)
    # TODO implement policies for multiply symbols
    policy = BoltzmannQPolicy()

    agent = DQNAgent(model=model, nb_actions=nb_actions,
                     memory=memory, nb_steps_warmup=1000,
                     target_model_update=1e-2, policy=policy,
                     processor=MultiInputProcessor(3),
                     # enable_dueling_network=True, dueling_type='avg'
                    )
    agent.compile(Adam(lr=1e-3), metrics=['mae'])

    try:
        # Comment here if you want to start learning again
        agent.load_weights('{p}/dqn_{fn}_weights.h5f'.format(p=PATH, fn=ENV_NAME))
        pass
    except OSError as e:
        print(e)
    except ValueError as e:
        print(e)

    # agent.fit(market, nb_steps=100000, visualize=False, verbose=2)
    # agent.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
    # agent.test(market, nb_episodes=5, visualize=False)

    tickcount = 0

    if TRAIN:
        agent.training = True

    observation = market.reset()

    while True:
        try:
            # TODO add callbacks?

            # (candles=9(mb=>(2,4)?), tickers=4, trades=2)
            # TODO actions for multy symbols market
            action = agent.forward(observation)

            observation, reward, done, info = market.step([action])

            agent.backward(reward, terminal=done)

            if done:
                observation = market.reset()
                agent.reset_states()
                done = False
                log.info('Is terminal state. Reset..')
                log.info('='*40)
            
            log.info('Tick: {t} | {info}'.format(
                    t=tickcount, info=info
            ))

            if tickcount % 100 == 0:
                agent.save_weights('{p}/dqn_{fn}_weights.h5f'.format(p=PATH, fn=ENV_NAME), overwrite=True)
            
            time.sleep(SLEEP)
            tickcount += 1

        except requests.exceptions.ConnectionError as e:
            log.exception(e)

        # TODO not working
        except KeyboardInterrupt as e:
            ## https://stackoverflow.com/questions/15457786/ctrl-c-crashes-python-after-importing-scipy-stats
            # We catch keyboard interrupts here so that training can be be safely aborted.
            # This is so common that we've built this right into this function, which ensures that
            # the `on_train_end` method is properly called.
            log.info('Aborted by user. {} \nExit...'.format(e))
            agent.save_weights('{p}/dqn_{fn}_weights.h5f'.format(p=PATH, fn=ENV_NAME), overwrite=True)
            break

        except RuntimeError as e:
            log.exception(e)
            break

        # except Exception as e:
        #     print(e)
        #     # log.exception(e)
        #     break

