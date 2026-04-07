import numpy as np
from metrics.metrics import (
    calculate_returns,
    calculate_sharpe,
    calculate_volatility,
    calculate_drawdown,
)


class Backtester:
    def __init__(self, env, strategy):
        self.env = env
        self.strategy = strategy
        self.history = []
        self.trades = []

    def run(self):
        self.env.reset()
        self.history = []
        self.trades = []

        step = 0

        while self.env.current_step < len(self.env.df) - 1:
            prev_position = self.env.get_position()

            # Strategy acts
            self.strategy.on_step(self.env)

            new_position = self.env.get_position()

            if new_position > prev_position:
                self.trades.append((step, "buy"))
            elif new_position < prev_position:
                self.trades.append((step, "sell"))

            portfolio_value = self.env.get_portfolio_value()
            self.history.append(portfolio_value)

            step += 1
            self.env.step()

        if len(self.history) < 2:
            return {
                "final_value": self.env.initial_cash,
                "history": self.history,
                "total_return": 0,
                "sharpe_ratio": 0,
                "volatility": 0,
                "max_drawdown": 0,
                "trades": self.trades,
            }

        returns = calculate_returns(self.history)

        total_return = (self.history[-1] - self.history[0]) / self.history[0]
        sharpe = calculate_sharpe(returns)
        volatility = calculate_volatility(returns)
        drawdown = calculate_drawdown(self.history)

        return {
            "final_value": self.history[-1],
            "history": self.history,
            "total_return": total_return,
            "sharpe_ratio": sharpe,
            "volatility": volatility,
            "max_drawdown": drawdown,
            "trades": self.trades,
        }