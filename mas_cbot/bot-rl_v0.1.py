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
from mas_tools.models import simple_model2
from mas_tools.tools import get_script_dir


#=============================================================================#
#   G L O B A L   V A R I A B L E S                                           #
#=============================================================================#
MY_API_KEY = '6zi9c6rsgJOekOoRCYyL5a8pgMcrmnfp8bnhi5eZ5hjkshwN2AQX3U2yIrKuzz20'
MY_API_SECRET = 'VGDdAIqSfPfkFtTuNFmyzCDeCg0aQocy4rLO3gtjcI194b3VypMkREdgdNCxgSyI'

ENV_NAME = 'Binance_2'

SLEEP = 0.3
TRAIN = True


if __name__ == "__main__":
    api = Binance(API_KEY=MY_API_KEY, API_SECRET=MY_API_SECRET)

    connector = VirtualMarket(api, symbols=['ETHUSDT'], periods='5m', balance=1000.0)
    print('connector shape', connector.shape)

    market = MarketEnv(connector)

    observation_shape = market.observation_space.shape
    nb_actions = market.action_space.n
    print('state =', observation_shape, '| actions =', nb_actions)

    model = simple_model2(observation_shape, nb_actions)

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
    print('first state=', observation.shape)

    if TRAIN:
        agent.training = True

    while True:
        try:
            # TODO add callbacks?

            action = agent.forward(observation)
            # TODO actions for multy symbols market
            action = np.argmax(action)

            observation, reward, done, info = market.step([action])

            agent.backward(reward, terminal=done)

            if done:
                observation = market.reset()
                done = False
                print('reset')
            
            print('reward= {%.2f}, balance= {%.2f}', reward, info['balance'])

            time.sleep(SLEEP)

        except KeyboardInterrupt:
            # We catch keyboard interrupts here so that training can be be safely aborted.
            # This is so common that we've built this right into this function, which ensures that
            # the `on_train_end` method is properly called.
            agent.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
            break

        except Exception as e:
            print(e)
            # log.exception(e)

