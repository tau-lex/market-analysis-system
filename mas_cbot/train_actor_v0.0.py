import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from cbot.api.binance import Binance
from cbot.environments import VirtualMarket


#=============================================================================#
#   G L O B A L   V A R I A B L E S                                           #
#=============================================================================#
MY_API_KEY = 'cNJBekTal8lT7WOCYXB8v8yj4m9VGo1rLRPIoqIdi58g3VKKwsX5EYT8iUOGqd7e'
MY_API_SECRET = 'sEkfMaDI3C2wUIBQBpcod3N5EDccCUKzVbCs8F38U5HdzAMXcudzW6wsZgUSw3bV'
ENV_NAME = 'BinanceVirt'


# Get the environment and extract the number of actions.
# env = VirtualMarket(Binance(MY_API_KEY, MY_API_SECRET))
env = VirtualMarket()
env.configure()
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n


#=============================================================================#
#   A C T O R   M O D E L                                                     #
#=============================================================================#
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())


#=============================================================================#
#   T R A I N   R U N                                                         #
#=============================================================================#
# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=50000, visualize=True, verbose=2)

# After training is done, we save the final weights.
dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=5, visualize=True)
