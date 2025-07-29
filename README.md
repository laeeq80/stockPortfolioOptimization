# Stock Portfolio Optimization — Data Engineering Project

A modular data engineering pipeline that fetches, stores, transforms, and analyzes historical stock data to support portfolio optimization strategies. Built using modern, cloud-native tools and structured for local development with MinIO (S3-compatible object store).

## Project Goals

- Automate data ingestion from external stock APIs
- Store raw and processed data in an S3-like object storage (MinIO)
- Prepare data for downstream analytics and optimization algorithms
- Simulate real-world cloud-based data pipelines locally

## Project Structure

stockPortfolioOptimization/
├── dags/                     # (Planned) Airflow DAGs  
├── data_pipeline/  
│   ├── fetch_data.py         # Ingest data from yFinance & upload to MinIO  
│   ├── transform.py          # Clean and preprocess data (WIP)  
│   └── load_to_db.py         # Load transformed data to SQL or parquet (WIP)  
├── optimizer/  
│   └── optimize.py           # Portfolio optimization algorithms  
├── streaming/                # (Planned) Real-time ingestion via Kafka  
├── dashboard/                # (Optional) Visualizations via Streamlit or Jupyter  
├── data/  
│   └── raw/                  # Raw CSVs (excluded from Git)  
├── docker-compose.yml        # Setup MinIO, Airflow, and dependencies  
├── requirements.txt          # Python dependencies  
├── start_local_env.bat       # Start environment (for Windows users)  
├── .gitignore                # Ignore raw data and secrets  
└── README.md  

## Tools and Technologies

Category        | Tools Used
----------------|--------------------------
Language        | Python
Data Sources    | yfinance (Yahoo Finance API)
Object Storage  | MinIO (S3-compatible)
Data Handling   | Pandas, Boto3, CSV
Containerization| Docker, Docker Compose
Orchestration   | Airflow (planned)
Visualization   | Streamlit / Jupyter (optional)

## Step 1: Data Ingestion (Completed)

- Downloads historical stock data using yfinance
- Saves raw CSVs to data/raw/
- Uploads files to local MinIO bucket (stock-data)
- MinIO runs at: http://localhost:9001  
  - Access Key: admin  
  - Secret Key: admin123

This simulates a cloud-based object storage pipeline on your local machine.

## How to Run

1. Start Local Environment

   On Windows:

start_local_env.bat


Or via Docker Compose directly:

docker compose up -d

2. Run the Ingestion Script


## Git Best Practices

The data/raw/ directory is excluded from version control via .gitignore. All data is reproducible by rerunning the ingestion pipeline.

## Next Steps

- transform.py: Clean and enrich data
- load_to_db.py: Load to PostgreSQL or Parquet
- Add DAGs for Airflow orchestration
- Build dashboard or notebook visualizations
- Connect optimization outputs to Streamlit dashboard

## License

MIT License

