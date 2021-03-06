#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import logging

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


MY_API_KEY = '---'
MY_API_SECRET = '---'

PATH = os.path.dirname(os.path.abspath(__file__))
ENV_NAME = 'cb_Binance_3'

SLEEP = 4
TRAIN = True
tickcount = 0

logging.basicConfig(level=logging.INFO,
    handlers=[logging.FileHandler("{p}/logs/{fn}.log".format(p=PATH, fn=ENV_NAME)),
                logging.StreamHandler()]
)

log = logging.getLogger()


## Init exchange api
api = Binance(API_KEY=MY_API_KEY, API_SECRET=MY_API_SECRET)

## Init market environment
market_conn = VirtualExchange(api, symbols=['ETHUSDT'], period='5m',
                                balance=1000.0, lot_size=0.1)
market = MarketEnv(market_conn)

## Environment parameters
observation_shape = market.observation_space.shape
nb_actions = market.action_space.n
log.info('State shape = {a} | actions = {b}'.format(a=observation_shape, b=nb_actions))

## Init ML-model for agent
limit = observation_shape[1]
model = cnn_model_2in((limit, 4), (limit, 4), nb_actions, 'softmax')

## Init RL-metod parameters
memory = SequentialMemory(limit=10000, window_length=1)
# TODO implement policies for multiply symbols
policy = BoltzmannQPolicy()

## Init RL agent
agent = DQNAgent(model=model, nb_actions=nb_actions,
    memory=memory, nb_steps_warmup=1000,
    target_model_update=1e-2, policy=policy,
    processor=MultiInputProcessor(2),
    # enable_dueling_network=True, dueling_type='avg'
)
agent.compile(Adam(lr=1e-3), metrics=['mae'])

## Comment this row if you want to start learning again
agent.load_weights('{p}/dqn_{fn}_weights.h5f'.format(p=PATH, fn=ENV_NAME))

## Train or evaluate
if TRAIN:
    agent.training = True

observation = market.reset()

while True:
    try:
        # TODO add callbacks?

        ## Agent vybiraet dejstvie
        # (candles=9(mb=>(2,4)?), tickers=4, trades=2)
        # TODO actions for multy symbols market
        action = agent.forward(observation)

        ## Execute action
        observation, reward, done, info = market.step([action])

        ## Poluchaem otvet ot sredy
        agent.backward(reward, terminal=done)

        ## Esli dostigli konca
        if done:
            observation = market.reset()
            agent.reset_states()
            done = False
            log.info('Is terminal state. Reset..')
            log.info('='*40)
        
        log.info('Tick: {t} | {info}'.format(
                t=tickcount, info=info
        ))

        ## Check point
        if tickcount % 100 == 0:
            agent.save_weights('{p}/dqn_{fn}_weights.h5f'.format(p=PATH, fn=ENV_NAME), overwrite=True)
        
        ## Time shift and counter
        time.sleep(SLEEP)
        tickcount += 1

    except ConnectionError as e:
        log.exception(e)

    # TODO not working
    except KeyboardInterrupt as e:
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
