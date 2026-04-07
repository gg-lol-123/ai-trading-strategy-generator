import pandas as pd
import json

from env.trading_env import TradingEnv
from loop.optimizer import StrategyOptimizer
from backtester.visualizer import plot_results


def main():
    # Load dataset
    df = pd.read_csv("data/sample_data.csv")

    # Create environment
    env = TradingEnv(df)

    # Optimizer (keep iterations low for free API)
    optimizer = StrategyOptimizer(env, model="gemini", iterations=2)

    # Initial prompt
    initial_prompt = """
    Create a trading strategy:
    - Buy when price is low
    - Sell when price is high
    - Must actively trade
    """

    # Run optimizer
    best_code, best_result = optimizer.optimize(initial_prompt)

    # ----- PRINT CLEAN RESULTS -----
    print("\n===== BEST STRATEGY =====\n")
    print(best_code)

    print("\n===== FINAL RESULTS =====")
    print(f"Final Value: {best_result['final_value']}")
    print(f"Return: {best_result['total_return']}")
    print(f"Sharpe: {best_result['sharpe_ratio']}")
    print(f"Drawdown: {best_result['max_drawdown']}")

    # ----- SAVE OUTPUTS -----
    with open("best_strategy.py", "w") as f:
        f.write(best_code)

    with open("results.json", "w") as f:
        json.dump(best_result, f, indent=4)

    print("\n Saved best_strategy.py and results.json")

    # ----- VISUALIZE -----
    plot_results(
        best_result["history"],
        list(df["close"]),
        best_result["trades"]
    )


if __name__ == "__main__":
    main()