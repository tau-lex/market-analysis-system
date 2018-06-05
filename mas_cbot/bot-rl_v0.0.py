import time
import logging

from datetime import datetime

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
ORDER_RISK = 2 * 0.01
MONTH_RISK = 6 * 0.01

ENV_NAME = 'Binance_2'

SLEEP = 0.1


if __name__ == "__main__":
    # INITIALAZATION
    api = Binance(API_KEY=MY_API_KEY, API_SECRET=MY_API_SECRET)
    market = AbstractMarket(api, symbols=['ETHUSDT'], periods=['15m'],
                            balance=1000.0, order_risk=ORDER_RISK, month_risk=MONTH_RISK)

    market = MarketEnv(market, window=1)

    observation_shape = market.observation_space.shape
    nb_actions = market.action_space.n
    print('state =', observation_shape, '| act =', nb_actions)

    model = simple_model(observation_shape, nb_actions)

    memory = SequentialMemory(limit=10000, window_length=1)
    policy = BoltzmannQPolicy()

    agent = DQNAgent(model=model, nb_actions=nb_actions,
                        memory=memory, nb_steps_warmup=10,
                        target_model_update=1e-2, policy=policy,
                        # enable_dueling_network=True, dueling_type='avg'
                    )
    agent.compile(Adam(lr=1e-3), metrics=['mae'])

    agent.fit(market, nb_steps=10000, visualize=False, verbose=2)

    agent.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

    agent.test(market, nb_episodes=5, visualize=False)

    # # MAIN LOOP
    # while True:
    #     try:
    #         # add callbacks?
    #         # agent.training = True

    #         action = agent.forward(observation)

    #         observation, reward, done, info = market.step(action)

    #         done = False

    #         # market.do(action)
    #         # agent.learn()

    #         agent.backward(reward, terminal=done)

    #         # # Finally, evaluate our algorithm for 5 episodes.
    #         # dqn.test(market, nb_episodes=5, visualize=True)

    #         time.sleep(SLEEP)

    #     except KeyboardInterrupt:
    #         # We catch keyboard interrupts here so that training can be be safely aborted.
    #         # This is so common that we've built this right into this function, which ensures that
    #         # the `on_train_end` method is properly called.
    #         did_abort = True
    #         break

    #     except Exception as e:
    #         log.exception(e)

