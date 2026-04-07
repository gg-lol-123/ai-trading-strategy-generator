import random
import pandas as pd

from backtester.backtester import Backtester
from env.trading_env import TradingEnv
from llm.generator import generate_strategy


class StrategyOptimizer:
    def __init__(self, model="gemini", iterations=3):
        self.model = model
        self.iterations = iterations

        # Load multiple datasets
        self.datasets = [
            pd.read_csv("data/reliance.csv"),
            pd.read_csv("data/tcs.csv"),
            pd.read_csv("data/infy.csv"),
            pd.read_csv("data/hdfc.csv"),
        ]

    def evaluate_strategy(self, strategy_class):
        results = []

        for df in self.datasets:
            env = TradingEnv(df)
            strategy = strategy_class()

            backtester = Backtester(env, strategy)
            result = backtester.run()

            results.append(result)

        # Aggregate metrics
        avg_return = sum(r["total_return"] for r in results) / len(results)
        avg_sharpe = sum(r["sharpe_ratio"] for r in results) / len(results)
        avg_drawdown = sum(r["max_drawdown"] for r in results) / len(results)
        total_trades = sum(len(r["trades"]) for r in results)

        return {
            "avg_return": avg_return,
            "avg_sharpe": avg_sharpe,
            "avg_drawdown": avg_drawdown,
            "total_trades": total_trades,
            "raw_results": results
        }

    def optimize(self, user_prompt):
        best_score = -999
        best_code = None
        best_result = None

        for i in range(self.iterations):
            print(f"\n===== ITERATION {i+1} =====")

            code = generate_strategy(user_prompt, self.model)

            try:
                local_scope = {}
                exec(code, {}, local_scope)

                strategy_class = None
                for v in local_scope.values():
                    if isinstance(v, type):
                        strategy_class = v
                        break

                if strategy_class is None:
                    print("No class found")
                    continue

                result = self.evaluate_strategy(strategy_class)

                print("Return:", result["avg_return"])
                print("Sharpe:", result["avg_sharpe"])
                print("Drawdown:", result["avg_drawdown"])
                print("Trades:", result["total_trades"])

                # Reject weak strategies
                if result["total_trades"] < 5:
                    print("Too few trades")
                    continue

                if result["avg_drawdown"] > 0.3:
                    print("Too risky")
                    continue

                # Score function
                score = (
                    result["avg_return"]
                    + result["avg_sharpe"] * 0.5
                    - result["avg_drawdown"] * 1.5
                )

                if score > best_score:
                    print("New BEST strategy!")
                    best_score = score
                    best_code = code
                    best_result = result

            except Exception as e:
                print("Error:", e)
                continue

        return best_code, best_result