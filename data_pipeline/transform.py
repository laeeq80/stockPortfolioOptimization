import pandas as pd
from pathlib import Path

# ----------------------------
# Config
# ----------------------------
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Function to process each CSV
# ----------------------------
def process_file(file_path):
    # Read CSV with multi-index headers and skip the spurious 'Date' header row at line 2
    df = pd.read_csv(file_path, header=[0,1], skiprows=[2])

    print(f"Columns after reading {file_path.name}:", df.columns.tolist())

    # Flatten columns
    df.columns = ['_'.join(filter(None, map(str, col))).strip('_') for col in df.columns]
    print(f"Columns after flattening: {df.columns.tolist()}")

    # Assume first column is Date (even if header says Price_Ticker)
    date_col = df.columns[0]
    df = df.rename(columns={date_col: 'Date'})
    df['Date'] = pd.to_datetime(df['Date'])

    # Find ticker from any column except Date
    # We can pick the ticker from the second level of the first non-date column
    # For that, extract tickers from original columns before flattening:
    # Or simply get ticker from any column except date

    # Extract ticker from columns (all columns except 'Date')
    # For example, after flattening, columns look like 'Close_AAPL', 'High_AAPL', etc.
    ticker = None
    for col in df.columns[1:]:
        parts = col.split('_')
        if len(parts) == 2:
            ticker = parts[1]
            break
    if ticker is None:
        ticker = "Unknown"

    # Use Close price for price column
    close_col = f"Close_{ticker}"
    if close_col not in df.columns:
        raise ValueError(f"No 'Close' price column found in file {file_path.name}")

    df = df.rename(columns={close_col: 'Price'})

    df = df.sort_values('Date')
    df['daily_return'] = df['Price'].pct_change()
    monthly_return = df['daily_return'].mean() * 21
    risk = df['daily_return'].std() * (21 ** 0.5)
    latest_price = df['Price'].iloc[-1]

    return {
        'ticker': ticker,
        'price_per_stock': round(latest_price, 2),
        'monthly_return': round(monthly_return, 4),
        'risk': round(risk, 4)
    }



# ----------------------------
# Process All Files
# ----------------------------
summary_data = []
for file in RAW_DIR.glob("*.csv"):
    print(f"Processing {file.name}")
    stats = process_file(file)
    summary_data.append(stats)

# Create summary DataFrame
summary_df = pd.DataFrame(summary_data)

# Save processed summary
summary_path = PROCESSED_DIR / "summary.csv"
summary_df.to_csv(summary_path, index=False)
print(f"✅ Summary saved to {summary_path}")
