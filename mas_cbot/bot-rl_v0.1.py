import os
import time
import logging

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
from mas_tools.models import simple_model, cnn_model_2in


#=============================================================================#
#   G L O B A L   V A R I A B L E S                                           #
#=============================================================================#
MY_API_KEY = '---'
MY_API_SECRET = '---'

PATH = os.path.dirname(os.path.abspath(__file__))
ENV_NAME = 'cb_Binance_2'

SLEEP = 1
TRAIN = True

logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.FileHandler("{p}/logs/{fn}.log".format(p=PATH, fn=ENV_NAME)),
                                logging.StreamHandler()]
                    )

log = logging.getLogger()

if __name__ == "__main__":
    api = Binance(API_KEY=MY_API_KEY, API_SECRET=MY_API_SECRET)

    market_conn = VirtualExchange(api, symbols=['ETHUSDT'], period='5m',
                                    balance=1000.0, lot_size=0.01)

    market = MarketEnv(market_conn)

    observation_shape = market.observation_space.shape
    nb_actions = market.action_space.n
    log.info('State shape = {a} | actions = {b}'.format(a=observation_shape, b=nb_actions))

    # (candles=9, tickers=4, trades=2)
    limit = observation_shape[1]
    model = cnn_model_2in((limit, 4), (limit, 4), nb_actions, 'relu')
    # model = cnn_model_2in((4, limit), (4, limit), nb_actions, 'relu')

    memory = SequentialMemory(limit=10000, window_length=1)
    # TODO implement policies for multiply symbols
    policy = BoltzmannQPolicy()

    agent = DQNAgent(model=model, nb_actions=nb_actions,
                     memory=memory, nb_steps_warmup=1000,
                     target_model_update=1e-2, policy=policy,
                     processor=MultiInputProcessor(2),
                     # enable_dueling_network=True, dueling_type='avg'
                    )
    agent.compile(Adam(lr=1e-3), metrics=['mae'])

    # agent.load_weights('dqn_{}_weights.h5f'.format(ENV_NAME))
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
            action = agent.forward(np.hsplit(observation[0], 2))
            # TODO actions for multy symbols market
            action = np.argmax(action)

            observation, reward, done, info = market.step([action])

            if tickcount % 10 == 0:
                reward = -1
                
            agent.backward(reward, terminal=done)

            if done:
                observation = market.reset()
                done = False
                log.debug('Is terminal state. Reset..')
            
            log.info('Tick: {t} / Action={a} / Reward={r} / Balance={b}'.format(
                    t=tickcount, a=info['last_action'],
                    r=reward, b=info['balance']
            ))

            if tickcount % 100 == 0:
                agent.save_weights('{p}/dqn_{fn}_weights.h5f'.format(p=PATH, fn=ENV_NAME), overwrite=True)
            
            time.sleep(SLEEP)
            tickcount += 1

        except ConnectionError as e:
            log.exception(e)

        except KeyboardInterrupt:
            # We catch keyboard interrupts here so that training can be be safely aborted.
            # This is so common that we've built this right into this function, which ensures that
            # the `on_train_end` method is properly called.
            log.exception('Aborted by user.\nExit...')
            agent.save_weights('{p}/dqn_{fn}_weights.h5f'.format(p=PATH, fn=ENV_NAME), overwrite=True)
            break

        except RuntimeError as e:
            log.exception(e)
            break

        # except Exception as e:
        #     print(e)
        #     # log.exception(e)
        #     break

