import matplotlib.pyplot as plt


def plot_results(history, prices, trades=None):
    plt.figure(figsize=(12, 6))

    # Portfolio value
    plt.plot(history, label="Portfolio Value")

    # Scaled price for comparison
    scaled_prices = [p * (history[0] / prices[0]) for p in prices]
    plt.plot(scaled_prices[:len(history)], linestyle="--", label="Price (scaled)")

    # Plot trades
    if trades:
        for step, action in trades:
            if step < len(history):
                if action == "buy":
                    plt.scatter(step, history[step], marker="^")
                elif action == "sell":
                    plt.scatter(step, history[step], marker="v")

    plt.title("Trading Strategy Performance")
    plt.xlabel("Time Step")
    plt.ylabel("Value")
    plt.legend()

    # Save graph
    plt.savefig("performance.png")

    # Show graph
    plt.show()