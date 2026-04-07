from strategies.base_strategy import BaseStrategy


class SimpleStrategy(BaseStrategy):
    def on_step(self, env):
        price = env.get_price()

        if price < 100:
            env.buy(1)
        elif price > 115:
            env.sell(1)