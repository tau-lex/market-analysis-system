# -*- coding: utf-8 -*-
import numpy as np

from gym import Env
from gym.spaces import Discrete, Box
from gym.utils import seeding

from mas_tools.markets import AbstractMarket


class MarketEnv(Env):
    """
    The class implements an Env class interface from the Gym (OpenAI) package,
    to communicate with real market data.
    """

    reward_range = (0, np.inf)
    action_space = None
    observation_space = None
    metadata = {'render.modes': ['human', 'rgb_array'],
                'video.frames_per_second' : 15}
    viewer = None

    def __init__(self, market: AbstractMarket, window=1, **kwargs):
        """MarketEnv constructor.
        
        Arguments:
            market (AbstractMarket): Wrapper for access to the market through API, or other solutions.
            window (int): This is the size of the state of the environment (The number of time intervals).
        """

        self.market = market
        self.window = window
        self.position = self.window

        self.action_space = Discrete(3)
        # TODO
        self.observation_space = Box(low=0.0, high=self.market.data.max(0)[2],
                                        shape=(self.window, self.market.data.shape[1]),
                                        dtype=np.float)

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Arguments:
            action (object): an action provided by the environment

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """

        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        done = False

        observation = self.market.observation(self.position, self.window)

        if action == 0:
            self.market.buy_order(observation[self.window-1, 1])
        elif action == 1:
            pass
        elif action == 2:
            self.market.sell_order(observation[self.window-1, 1])

        self.position += 1
        reward = self.market.balance
        if self.position >= len(self.market) or reward <= 0:
            done = True

        info = {}

        return (observation, reward, done, info)

    def reset(self):
        """Resets the state of the environment and returns an initial observation.

        Returns: observation (object): the initial observation of the space.
        """
        self.position = self.window
        self.market.reset()
        observation = self.market.observation(self.position, self.window)

        return observation

    def render(self, mode='human', close=False):
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).

        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.

        Arguments:
            mode (str): The mode to render with.
            close (bool): Close all open renderings.
        """

        if mode == 'rgb_array':
            return np.array(...) # return RGB frame suitable for video
        elif mode is 'human':
            pass # pop up a window and render
        else:
            super(MarketEnv, self).render(mode=mode) # just raise an exception

    def configure(self, *args, **kwargs):
        """Provides runtime configuration to the environment.
        This configuration should consist of data that tells your
        environment how to run (such as an address of a remote server,
        or path to your ImageNet data). It should not affect the
        semantics of the environment.
        """
        raise NotImplementedError()

    def close(self):
        """Override _close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        if self.viewer: self.viewer.close()

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).
        
        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def __del__(self):
        self.close()

    def __str__(self):
        return '<{} instance>'.format(type(self).__name__)

