import numpy as np


def calculate_returns(history):
    returns = []

    for i in range(1, len(history)):
        r = (history[i] - history[i - 1]) / history[i - 1]
        returns.append(r)

    return np.array(returns)


def calculate_sharpe(returns, risk_free_rate=0.0):
    if len(returns) == 0:
        return 0

    excess_returns = returns - risk_free_rate

    std = np.std(excess_returns)

    if std == 0:
        return 0

    sharpe = np.mean(excess_returns) / std

    return sharpe


def calculate_volatility(returns):
    if len(returns) == 0:
        return 0

    return np.std(returns)


def calculate_drawdown(history):
    peak = history[0]
    max_drawdown = 0

    for value in history:
        if value > peak:
            peak = value

        drawdown = (peak - value) / peak

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return max_drawdown