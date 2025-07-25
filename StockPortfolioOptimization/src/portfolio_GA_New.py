import csv
import random

class Stock:
    def __init__(self, name, price_per_stock, risk, monthly_return):
        self.name = name
        self.price_per_stock = price_per_stock
        self.risk = risk
        self.monthly_return = monthly_return

    def __repr__(self):
        return f"{self.name} (Price: {self.price_per_stock}, Risk: {self.risk}, Return: {self.monthly_return})"

class Portfolio:
    def __init__(self, stocks):
        self.stocks = stocks

    def total_value(self):
        return sum(stock.price_per_stock for stock in self.stocks)

    def average_risk(self):
        return sum(stock.risk for stock in self.stocks) / len(self.stocks)

    def average_return(self):
        return sum(stock.monthly_return for stock in self.stocks) / len(self.stocks)

class GeneticAlgorithm:
    def __init__(self, stocks, population_size, portfolio_size):
        self.stocks = stocks
        self.population_size = population_size
        self.portfolio_size = portfolio_size
        self.population = self.initialize_population()

    def initialize_population(self):
        return [Portfolio(random.sample(self.stocks, self.portfolio_size)) for _ in range(self.population_size)]

    def evaluate_portfolio(self, portfolio):
        return portfolio.average_return() / portfolio.average_risk()

    def selection(self):
        self.population.sort(key=self.evaluate_portfolio, reverse=True)
        return self.population[:self.population_size // 2]

    def crossover(self, parent1, parent2):
        child_stocks = list(set(parent1.stocks + parent2.stocks))
        if len(child_stocks) < self.portfolio_size:
            child_stocks += random.sample([s for s in self.stocks if s not in child_stocks],
                                          self.portfolio_size - len(child_stocks))
        return Portfolio(random.sample(child_stocks, self.portfolio_size))

    def mutate(self, portfolio):
        if random.random() < 0.1:
            index = random.randint(0, self.portfolio_size - 1)
            new_stock = random.choice([s for s in self.stocks if s not in portfolio.stocks])
            portfolio.stocks[index] = new_stock

    def run(self, generations):
        for _ in range(generations):
            selected = self.selection()
            next_generation = selected[:]
            while len(next_generation) < self.population_size:
                parent1, parent2 = random.sample(selected, 2)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                next_generation.append(child)
            self.population = next_generation

        return max(self.population, key=self.evaluate_portfolio)

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

# --- Main program ---
if __name__ == "__main__":
    filepath = r"..\data\stocks_data.csv"  # Use raw string for Windows paths
    stocks_data = read_stocks_from_csv(filepath)

    population_size = int(input("Enter the population size: "))
    portfolio_size = int(input("Enter the portfolio size: "))
    generations = int(input("Enter the number of generations: "))

    ga = GeneticAlgorithm(stocks_data, population_size, portfolio_size)
    best_portfolio = ga.run(generations)

    print("\nBest Portfolio:")
    for stock in best_portfolio.stocks:
        print(stock)

    print(f"\nTotal Value: {best_portfolio.total_value():.2f}")
    print(f"Average Risk: {best_portfolio.average_risk():.4f}")
    print(f"Average Return: {best_portfolio.average_return():.4f}")
