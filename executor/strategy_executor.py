from strategies.base_strategy import BaseStrategy


def load_strategy(code):
    """
    Load any class that has an 'on_step' method
    """

    safe_globals = {
        "BaseStrategy": BaseStrategy,
    }

    local_vars = {}

    try:
        exec(code, safe_globals, local_vars)
    except Exception as e:
        raise RuntimeError(f"Error in generated code: {e}")

    strategy_class = None

    for obj in local_vars.values():
        if isinstance(obj, type):
            # 🔥 Check if it has on_step method
            if hasattr(obj, "on_step"):
                strategy_class = obj
                break

    if strategy_class is None:
        raise RuntimeError("No valid strategy class found")

    return strategy_class()