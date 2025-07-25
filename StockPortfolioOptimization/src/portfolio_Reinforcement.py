import csv
import random

class Stock:
    def __init__(self, name, price_per_stock, risk, monthly_return):
        self.name = name
        self.price_per_stock = price_per_stock
        self.risk = risk
        self.monthly_return = monthly_return

    def __repr__(self):
        return (f"{self.name} (Price: {self.price_per_stock}, "
                f"Risk: {self.risk}, Return: {self.monthly_return})")

class Portfolio:
    def __init__(self, stocks):
        self.stocks = stocks

    def total_value(self):
        return sum(stock.price_per_stock for stock in self.stocks)

    def average_risk(self):
        return sum(stock.risk for stock in self.stocks) / len(self.stocks)

    def average_return(self):
        return sum(stock.monthly_return for stock in self.stocks) / len(self.stocks)

class ReinforcementLearner:
    def __init__(self, stocks, portfolio_size, episodes):
        self.stocks = stocks
        self.portfolio_size = portfolio_size
        self.episodes = episodes
        self.q_table = {}
        self.epsilon = 0.2
        self.alpha = 0.1
        self.gamma = 0.9

    def get_state_key(self, selected_indexes):
        return tuple(sorted(selected_indexes))

    def get_possible_actions(self, current_indexes):
        return [i for i in range(len(self.stocks)) if i not in current_indexes]

    def reward(self, portfolio):
        return portfolio.average_return() / (portfolio.average_risk() + 1e-6)

    def learn(self):
        best_portfolio = None
        best_reward = float('-inf')

        for _ in range(self.episodes):
            current_indexes = []

            for _ in range(self.portfolio_size):
                state_key = self.get_state_key(current_indexes)
                possible_actions = self.get_possible_actions(current_indexes)

                if not possible_actions:
                    break

                if random.random() < self.epsilon:
                    action = random.choice(possible_actions)
                else:
                    q_values = [
                        (self.q_table.get(self.get_state_key(current_indexes + [a]), 0), a)
                        for a in possible_actions
                    ]
                    action = max(q_values, key=lambda x: x[0])[1] if q_values else random.choice(possible_actions)

                current_indexes.append(action)

                # Update Q-table
                portfolio = Portfolio([self.stocks[i] for i in current_indexes])
                current_reward = self.reward(portfolio)

                next_state_key = self.get_state_key(current_indexes)
                old_q = self.q_table.get(state_key, 0)
                future_q = max(
                    [self.q_table.get(self.get_state_key(current_indexes + [a]), 0)
                     for a in self.get_possible_actions(current_indexes)],
                    default=0
                )

                self.q_table[state_key] = old_q + self.alpha * (current_reward + self.gamma * future_q - old_q)

            # Evaluate final portfolio of the episode
            final_portfolio = Portfolio([self.stocks[i] for i in current_indexes])
            final_reward = self.reward(final_portfolio)

            if final_reward > best_reward:
                best_portfolio = final_portfolio
                best_reward = final_reward

        return best_portfolio

def read_stocks_from_csv(filepath):
    stocks = []
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    stocks.append(Stock(
                        name=row['CompanyName'],
                        price_per_stock=float(row['PricePerStock']),
                        risk=float(row['Risk']),
                        monthly_return=float(row['MonthlyReturn'])
                    ))
                except ValueError:
                    pass
    except FileNotFoundError:
        print(f"CSV file not found: {filepath}")
    return stocks

# --- Main ---
if __name__ == "__main__":
    filepath = r"..\data\stocks_data.csv"  # Update as needed
    stocks_data = read_stocks_from_csv(filepath)

    if not stocks_data:
        print("No valid stock data found.")
    else:
        portfolio_size = int(input("Enter the portfolio size: "))
        episodes = int(input("Enter the number of episodes: "))

        rl = ReinforcementLearner(stocks_data, portfolio_size, episodes)
        best_portfolio = rl.learn()

        print("\nBest Portfolio (Reinforcement Learning):")
        for stock in best_portfolio.stocks:
            print(stock)

        print(f"\nTotal Value: {best_portfolio.total_value():.2f}")
        print(f"Average Risk: {best_portfolio.average_risk():.4f}")
        print(f"Average Return: {best_portfolio.average_return():.4f}")
