import csv
import random
import numpy as np
import cvxpy as cp

class Stock:
    def __init__(self, name, price_per_stock, risk, monthly_return):
        self.name = name
        self.price_per_stock = price_per_stock
        self.risk = risk
        self.monthly_return = monthly_return

    def __repr__(self):
        return f"{self.name} (Price: {self.price_per_stock}, Risk: {self.risk}, Return: {self.monthly_return})"

class Portfolio:
    def __init__(self, stocks, weights):
        self.stocks = stocks
        self.weights = weights  # weights = investment proportions

    def total_value(self):
        return sum(stock.price_per_stock for stock in self.stocks)

    def average_risk(self):
        risks = np.array([stock.risk for stock in self.stocks])
        cov_matrix = np.diag(risks**2)  # Simplified covariance matrix
        w = np.array(self.weights)
        return np.sqrt(w.T @ cov_matrix @ w)

    def average_return(self):
        returns = np.array([stock.monthly_return for stock in self.stocks])
        w = np.array(self.weights)
        return w.T @ returns

class MarkowitzModel:
    def __init__(self, stocks):
        self.stocks = stocks

    def optimize(self):
        n = len(self.stocks)
        returns = np.array([s.monthly_return for s in self.stocks])
        risks = np.array([s.risk for s in self.stocks])
        cov_matrix = np.diag(risks ** 2)

        weights = cp.Variable(n)

        # Objective: minimize portfolio variance
        objective = cp.Minimize(cp.quad_form(weights, cov_matrix))

        # Constraints: weights sum to 1, no short selling
        constraints = [
            cp.sum(weights) == 1,
            weights >= 0,
        ]

        problem = cp.Problem(objective, constraints)
        problem.solve()

        if weights.value is None:
            raise ValueError("Optimization failed.")

        return Portfolio(self.stocks, weights.value)

def read_stocks_from_csv(filepath):
    stocks = []
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stocks.append(Stock(
                name=row['CompanyName'],
                price_per_stock=float(row['PricePerStock']),
                risk=float(row['Risk']),
                monthly_return=float(row['MonthlyReturn'])
            ))
    return stocks

# --- Main Program ---
if __name__ == "__main__":
    filepath = r"..\data\stocks_data.csv"  # Update as needed
    stocks_data = read_stocks_from_csv(filepath)

    portfolio_size = int(input("Enter the portfolio size: "))

    if portfolio_size > len(stocks_data):
        print(f"Portfolio size {portfolio_size} is greater than available stocks {len(stocks_data)}.")
        portfolio_size = len(stocks_data)

    selected_stocks = random.sample(stocks_data, portfolio_size)

    model = MarkowitzModel(selected_stocks)

    try:
        best_portfolio = model.optimize()

        print("\nBest Portfolio (Markowitz Optimization):")
        for stock, weight in zip(best_portfolio.stocks, best_portfolio.weights):
            print(f"{stock.name}: Price = {stock.price_per_stock:.2f}, "
                  f"Risk = {stock.risk:.4f}, Return = {stock.monthly_return:.4f}, "
                  f"Weight = {weight:.4f}")

        print(f"\nTotal Invested Amount: {best_portfolio.total_value():.2f}")
        print(f"Portfolio Risk (Std Dev): {best_portfolio.average_risk():.4f}")
        print(f"Portfolio Expected Return: {best_portfolio.average_return():.4f}")

    except ValueError as e:
        print(f"Error: {e}")
