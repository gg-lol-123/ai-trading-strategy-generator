import gradio as gr
import pandas as pd

from env.trading_env import TradingEnv
from loop.optimizer import StrategyOptimizer
from backtester.visualizer import plot_results


def run_strategy(user_prompt):
    optimizer = StrategyOptimizer(model="gemini", iterations=2)

    best_code, best_result = optimizer.optimize(user_prompt)

    if best_result is None:
        return "No valid strategy found", "Try again", None

    # Use first dataset for visualization
    df = pd.read_csv("data/reliance.csv")

    plot_results(
        best_result["raw_results"][0]["history"],
        list(df["close"]),
        best_result["raw_results"][0]["trades"]
    )

    result_text = f"""
Final Value: {best_result['raw_results'][0]['final_value']}

Avg Return: {best_result['avg_return']}
Avg Sharpe: {best_result['avg_sharpe']}
Avg Volatility: {best_result['raw_results'][0]['volatility']}
Avg Drawdown: {best_result['avg_drawdown']}

Total Trades: {best_result['total_trades']}
"""

    return best_code, result_text, "performance.png"


# NEW CLEAN UI USING BLOCKS
with gr.Blocks(title="AI Trading Strategy Generator") as interface:

    gr.Markdown("# 🤖 AI Trading Strategy Generator")

    with gr.Row():
        user_input = gr.Textbox(
            label="Enter Strategy Idea",
            lines=6,
            placeholder="e.g. Use moving average crossover strategy"
        )

    run_btn = gr.Button("🚀 Run Strategy")

    with gr.Row():
        code_output = gr.Code(
            label="Generated Strategy Code",
            language="python"
        )

    with gr.Row():
        result_output = gr.Textbox(
            label="Results",
            lines=6
        )

    with gr.Row():
        graph_output = gr.Image(label="Performance Graph")

    run_btn.click(
        fn=run_strategy,
        inputs=user_input,
        outputs=[code_output, result_output, graph_output]
    )


if __name__ == "__main__":
    interface.launch()

# to run the code --> python -m ui.app