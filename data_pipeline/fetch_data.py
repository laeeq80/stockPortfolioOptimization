import yfinance as yf
import boto3
from botocore.exceptions import NoCredentialsError
import os
from datetime import datetime

# -------------------------------
# CONFIGURATION
# -------------------------------
TICKERS = ["AAPL", "GOOGL", "MSFT"]
START_DATE = "2023-01-01"
END_DATE = datetime.today().strftime('%Y-%m-%d')
LOCAL_DIR = "data/raw"
BUCKET_NAME = "stock-data"
MINIO_ENDPOINT = "localhost:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "admin123"
USE_SSL = False  # Keep it False for localhost

# -------------------------------
# Ensure local folder exists
# -------------------------------
os.makedirs(LOCAL_DIR, exist_ok=True)

# -------------------------------
# Initialize S3 client
# -------------------------------
s3 = boto3.client(
    's3',
    endpoint_url=f"http{'s' if USE_SSL else ''}://{MINIO_ENDPOINT}",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    verify=USE_SSL
)

# -------------------------------
# Create bucket if it doesn't exist
# -------------------------------
existing_buckets = s3.list_buckets()
if BUCKET_NAME not in [b['Name'] for b in existing_buckets.get('Buckets', [])]:
    s3.create_bucket(Bucket=BUCKET_NAME)
    print(f"✅ Created bucket: {BUCKET_NAME}")
else:
    print(f"✅ Bucket '{BUCKET_NAME}' already exists.")

# -------------------------------
# Download and upload data
# -------------------------------
for ticker in TICKERS:
    print(f"📥 Downloading data for {ticker}...")
    data = yf.download(ticker, start=START_DATE, end=END_DATE)
    filename = f"{ticker}.csv"
    local_path = os.path.join(LOCAL_DIR, filename)
    data.to_csv(local_path)

    print(f"☁️ Uploading {filename} to MinIO...")
    try:
        s3.upload_file(local_path, BUCKET_NAME, filename)
        print(f"✅ Uploaded: {filename}")
    except NoCredentialsError:
        print("❌ Credentials not available for MinIO upload.")
