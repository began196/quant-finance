import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def backtest_strategy(signals, returns, plot_charts=False):
    """
    Backtests a trading strategy based on given signals and asset returns, and optionally plots performance charts.
    
    Parameters:
        signals (pd.Series or list): Trading signals (-1 for short, 1 for long, 0 for no position).
        returns (pd.Series or list): Daily returns of the asset.
        plot_charts (bool): If True, plots the Cumulative Returns and Drawdown charts.
    
    Returns:
        dict: A dictionary containing total profit/loss, Sharpe ratio, max drawdown, cumulative return,
              and the full DataFrame with the strategy performance.
    """
    # Create a DataFrame from the input signals and returns
    df = pd.DataFrame({
        'signals': signals,
        'returns': returns
    })

    # Calculate the strategy returns (shift signal by 1 to simulate trade-on-open)
    df['strategy_returns'] = df['signals'].shift(1) * df['returns']
    df['strategy_returns'].fillna(0, inplace=True)

    # Calculate cumulative returns
    df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

    # Total Profit/Loss
    total_pnl = df['strategy_returns'].sum()

    # Sharpe Ratio: (mean return - risk-free rate) / std dev of returns
    # Assuming risk-free rate = 0 for simplicity
    mean_return = df['strategy_returns'].mean()
    std_return = df['strategy_returns'].std()
    sharpe_ratio = (mean_return / std_return) * np.sqrt(252) if std_return != 0 else np.nan

    # Max Drawdown
    cumulative_max = df['cumulative_returns'].cummax()
    drawdown = (df['cumulative_returns'] - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()

    # Cumulative Return
    cumulative_return = df['cumulative_returns'].iloc[-1] - 1

    # Create the results dictionary
    results = {
        'Total PnL': total_pnl,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown': max_drawdown,
        'Cumulative Return': cumulative_return,
        'Performance DataFrame': df
    }

    # Plot the performance charts if requested
    if plot_charts:
        plot_performance(df, drawdown)
    
    return results

def plot_performance(df, drawdown):
    """
    Plots cumulative returns and drawdown.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the strategy performance data.
        drawdown (pd.Series): The drawdown series for the strategy.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot Cumulative Returns
    ax1.plot(df['cumulative_returns'], label='Cumulative Returns', color='blue')
    ax1.set_title('Cumulative Returns')
    ax1.set_ylabel('Cumulative Value')
    ax1.grid(True)
    ax1.legend()

    # Plot Drawdown
    ax2.plot(drawdown, label='Drawdown', color='red')
    ax2.set_title('Drawdown')
    ax2.set_ylabel('Drawdown (%)')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()

