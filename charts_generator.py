import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import tkinter as tk
import numpy as np
from datetime import datetime
import subprocess
import os

def generate_financial_data_chart(stock_symbols, start_date, end_date, price_type='Adj Close'):
    # Create subplots for multiple stocks in one figure
    fig, ax = plt.subplots(figsize=(10, 6))

    for stock_symbol in stock_symbols:
        try:
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
            if stock_data.empty:
                raise ValueError(f"No data found for {stock_symbol}")

            normalized_prices = stock_data[price_type] / stock_data[price_type].iloc[0]  # Normalize prices

            ax.plot(normalized_prices, label=stock_symbol)
        except Exception as e:
            print(f"Error fetching data for {stock_symbol}: {e}")
            continue

    if not ax.lines:
        plt.close()
        raise ValueError("No valid data available for the provided stock symbols.")

    ax.set_title(f"Normalized {price_type} for Selected Stocks")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Normalized {price_type}")
    ax.grid(True)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart with a unique filename in the project directory
    chart_filename = f"financial_chart_{', '.join(stock_symbols)}_{start_date}_{end_date}.png"
    chart_filepath = f"./{chart_filename}"  # Specify the full path for saving in the project directory
    plt.savefig(chart_filepath)
    plt.close()

    # Display measures below the chart
    measures_text = get_measures_text(stock_symbols, start_date, end_date, price_type)
    plt.figure(figsize=(10, 3))
    plt.text(0.5, 0.5, measures_text, ha='center', va='center', fontsize=10, bbox=dict(boxstyle='round', alpha=0.1))
    plt.axis('off')  # Turn off axis for a cleaner look
    plt.tight_layout()

    # Save the measures section with a unique filename
    measures_filename = f"measures_{', '.join(stock_symbols)}_{start_date}_{end_date}.png"
    measures_filepath = f"./{measures_filename}"
    plt.savefig(measures_filepath)
    plt.close()

    # Open the chart using the default image viewer
    open_image(chart_filepath)
    # Open the measures section using the default image viewer
    open_image(measures_filepath)

    return f"Chart for selected stocks successfully created as '{chart_filepath}'."

def get_measures_text(stock_symbols, start_date, end_date, price_type='Adj Close'):
    measures_text = "Calculated Measures:\n\n"

    for stock_symbol in stock_symbols:
        try:
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
            if stock_data.empty:
                raise ValueError(f"No data found for {stock_symbol}")

            # Calculate measures for each stock
            stock_data['Daily_Return'] = stock_data['Adj Close'].pct_change()
            sharpe_ratio = np.sqrt(252) * (stock_data['Daily_Return'].mean() / stock_data['Daily_Return'].std())
            cumulative_returns = (1 + stock_data['Daily_Return']).cumprod()
            peak_value = cumulative_returns.cummax()
            drawdown = (cumulative_returns - peak_value) / peak_value
            max_drawdown = drawdown.min()

            measures_text += f"{stock_symbol}\nSharpe Ratio: {sharpe_ratio:.4f}\nMDD: {max_drawdown:.4%}\n\n"

        except Exception as e:
            measures_text += f"{stock_symbol}\nError calculating measures: {str(e)}\n\n"
            continue

    return measures_text

def open_image(image_path):
    # Open the image using the default image viewer
    if os.name == 'posix':
        subprocess.run(['open', image_path])
    elif os.name == 'nt':
        os.startfile(image_path)

def on_generate():
    # Get user inputs
    selected_months = month_entry.get()
    stock_symbols = stock_entry.get().split(',')

    # Check if the user provided valid inputs
    try:
        selected_months = int(selected_months)
        if selected_months <= 0:
            raise ValueError("Number of past months must be a positive integer.")
    except ValueError:
        result_label.config(text="Invalid input. Please enter a valid number of past months.")
        return

    if not stock_symbols or not all(symbol.strip() for symbol in stock_symbols):
        result_label.config(text="Invalid input. Please enter a valid list of stock symbols.")
        return

    # Validate stock symbols
    valid_symbols = []
    for symbol in stock_symbols:
        try:
            stock_info = yf.Ticker(symbol)
            stock_info.history(period='1d')  # Accessing history to check if the symbol is valid
            valid_symbols.append(symbol)
        except:
            print(f"Invalid stock symbol or no data found: {symbol}")
            continue

    if not valid_symbols:
        result_label.config(text="No valid stock symbols found.")
        return

    # Calculate start and end dates based on the selected_months
    current_date = pd.to_datetime('today')
    end_date = current_date
    start_date = end_date - pd.DateOffset(months=selected_months)

    # Generate financial data chart and optionally calculate measures
    try:
        result = generate_financial_data_chart(valid_symbols, start_date, end_date, price_type_var.get())
        result_label.config(text=result)
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Financial Chart Generator")

    month_label = tk.Label(root, text="Enter the desired number of past months (e.g., 3):")
    month_label.pack()

    month_entry = tk.Entry(root)
    month_entry.pack()

    stock_label = tk.Label(root, text="Enter the list of stock symbols (comma-separated): ")
    stock_label.pack()

    stock_entry = tk.Entry(root)
    stock_entry.pack()

    price_type_label = tk.Label(root, text="Select the price type to plot:")
    price_type_label.pack()

    price_type_var = tk.StringVar()
    price_type_var.set('Adj Close')

    price_type_options = ['Open', 'High', 'Low', 'Close', 'Adj Close']
    price_type_menu = tk.OptionMenu(root, price_type_var, *price_type_options)
    price_type_menu.pack()

    generate_button = tk.Button(root, text="Generate Charts", command=on_generate)
    generate_button.pack()

    cancel_button = tk.Button(root, text="Cancel", command=root.destroy)
    cancel_button.pack()

    stock_options_label = tk.Label(root, text="Available Stocks: AAPL, GOOGL, MSFT")  # Add more stocks as needed
    stock_options_label.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()

