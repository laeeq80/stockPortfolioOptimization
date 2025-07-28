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

class Particle:
    def __init__(self, stocks, portfolio_size):
        self.stocks = stocks
        self.portfolio_size = portfolio_size
        self.position = random.sample(range(len(stocks)), portfolio_size)
        self.velocity = []
        self.best_position = self.position[:]
        self.best_score = -float('inf')

    def get_portfolio(self):
        return Portfolio([self.stocks[i] for i in self.position])

class PSO:
    def __init__(self, stocks, num_particles, portfolio_size, num_iterations):
        self.stocks = stocks
        self.num_particles = num_particles
        self.portfolio_size = portfolio_size
        self.num_iterations = num_iterations
        self.swarm = [Particle(stocks, portfolio_size) for _ in range(num_particles)]
        self.global_best_position = None
        self.global_best_score = -float('inf')

    def evaluate(self, portfolio):
        risk = portfolio.average_risk()
        return 0 if risk == 0 else portfolio.average_return() / risk

    def difference(self, a, b):
        swaps = []
        a_set = set(a)
        b_set = set(b)
        to_remove = [x for x in a if x not in b_set]
        to_add = [x for x in b if x not in a_set]
        a_copy = a[:]
        for remove_stock, add_stock in zip(to_remove, to_add):
            i = a_copy.index(remove_stock)
            swaps.append((i, add_stock))
            a_copy[i] = add_stock
        return swaps

    def update_velocity(self, particle):
        w, c1, c2 = 0.5, 1.0, 1.0
        vel_inertia = particle.velocity[:int(w * len(particle.velocity))]
        swaps_cognitive = self.difference(particle.position, particle.best_position)
        swaps_social = self.difference(particle.position, self.global_best_position) if self.global_best_position else []

        def select_swaps(swaps, coeff):
            return [s for s in swaps if random.random() < coeff]

        new_velocity = vel_inertia + select_swaps(swaps_cognitive, c1) + select_swaps(swaps_social, c2)

        unique_velocity = {}
        for idx, stock_idx in new_velocity:
            unique_velocity[idx] = stock_idx
        particle.velocity = [(idx, stock_idx) for idx, stock_idx in unique_velocity.items()]

    def apply_velocity(self, particle):
        pos = particle.position[:]
        for i, new_stock in particle.velocity:
            pos[i] = new_stock
        if len(set(pos)) < len(pos):
            all_indices = set(range(len(self.stocks)))
            missing = list(all_indices - set(pos))
            for idx in range(len(pos)):
                if pos.count(pos[idx]) > 1 and missing:
                    pos[idx] = missing.pop()
        particle.position = pos

    def run(self):
        for _ in range(self.num_iterations):
            for particle in self.swarm:
                portfolio = particle.get_portfolio()
                score = self.evaluate(portfolio)

                if score > particle.best_score:
                    particle.best_score = score
                    particle.best_position = particle.position[:]

                if score > self.global_best_score:
                    self.global_best_score = score
                    self.global_best_position = particle.position[:]

            for particle in self.swarm:
                self.update_velocity(particle)
                self.apply_velocity(particle)

        best_stocks = [self.stocks[i] for i in self.global_best_position]
        return Portfolio(best_stocks)

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

if __name__ == "__main__":
    filepath = r"..\data\stocks_data.csv"
    stocks_data = read_stocks_from_csv(filepath)

    num_particles = int(input("Enter the number of particles: "))
    portfolio_size = int(input("Enter the portfolio size: "))
    num_iterations = int(input("Enter the number of iterations: "))

    pso = PSO(stocks_data, num_particles, portfolio_size, num_iterations)
    best_portfolio = pso.run()

    print("\nBest Portfolio:")
    for stock in best_portfolio.stocks:
        print(stock)

    print(f"\nTotal Value: {best_portfolio.total_value():.2f}")
    print(f"Average Risk: {best_portfolio.average_risk():.4f}")
    print(f"Average Return: {best_portfolio.average_return():.4f}")
