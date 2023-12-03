
```markdown
# Financial Chart Generator

The Financial Chart Generator is a Python script that allows you to generate financial charts for multiple stocks and calculate relevant measures.

## Features

- **Multiple Stocks:** Plot financial charts for multiple stocks simultaneously.
- **Custom Time Period:** Specify the desired number of past months to analyze.
- **Price Types:** Choose from Open, High, Low, Close, or Adjusted Close prices for plotting.
- **Measures Calculation:** Automatically calculates Sharpe Ratio and Maximum Drawdown for each selected stock.

## Requirements

Make sure you have the following Python libraries installed:

- pandas
- matplotlib
- yfinance
- tkinter
- numpy

You can install the required libraries using:

```bash
pip install pandas matplotlib yfinance tkinter numpy
```

## Usage

1. Run the `chart_generator.py` script.
2. Enter the desired number of past months and a list of stock symbols (comma-separated).
3. Choose the price type for plotting.
4. Click the "Generate Charts" button.
5. View the generated charts and measures.

### Example

```bash
python chart_generator.py
```

### Available Stocks

- AAPL
- GOOGL
- MSFT

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```