class BaseStrategy:
    def on_step(self, env):
        """
        Called at every timestep
        Must be implemented by all strategies
        """
        raise NotImplementedError