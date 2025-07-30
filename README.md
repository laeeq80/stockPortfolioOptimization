# Stock Portfolio Optimization — Data Engineering Project

A modular data engineering pipeline that fetches, stores, transforms, and analyzes historical stock data to support portfolio optimization strategies. Built using modern, cloud-native tools and structured for local development with MinIO (S3-compatible object store).

## Project Goals

- Automate data ingestion from external stock APIs  
- Store raw and processed data in an S3-like object storage (MinIO)  
- Prepare and enrich data for downstream analytics and optimization algorithms  
- Simulate real-world cloud-based data pipelines locally  

## Project Structure

stockPortfolioOptimization/

├── dags/                     # (Planned) Airflow DAGs  
├── data_pipeline/  
│   ├── fetch_data.py         # Ingest data from yFinance & upload to MinIO  
│   ├── transform.py          # Clean, preprocess, and enrich data (Completed)  
│   └── load_to_db.py         # Load transformed data to SQL or parquet (WIP)  
├── optimizer/  
│   └── optimize.py           # Portfolio optimization algorithms  
├── streaming/                # (Planned) Real-time ingestion via Kafka  
├── dashboard/                # (Optional) Visualizations via Streamlit or Jupyter  
├── data/  
│   ├── raw/                  # Raw CSVs (excluded from Git)  
│   └── processed/            # Transformed and summary CSV outputs  
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

## Pipeline Steps Completed

### 1. Data Ingestion

- Downloads historical stock data using yfinance  
- Saves raw CSVs to `data/raw/`  
- Uploads files to local MinIO bucket (`stock-data`)  
- MinIO runs at: http://localhost:9001  
  - Access Key: admin  
  - Secret Key: admin123  

This simulates a cloud-based object storage pipeline on your local machine.

### 2. Data Transformation (Completed)

- Reads raw CSVs with multi-index headers  
- Flattens and renames columns for easier processing  
- Parses and converts 'Date' columns to datetime  
- Calculates key metrics per ticker:  
  - Latest price  
  - Monthly return  
  - Risk (volatility)  
- Generates a consolidated summary CSV in `data/processed/`

## How to Run

1. Start Local Environment

   On Windows:

start_local_env.bat

Or via Docker Compose directly:

2. Run the Ingestion Script
3. Run the Transformation Script

## Git Best Practices

The `data/raw/` directory is excluded from version control via `.gitignore`. All data is reproducible by rerunning the ingestion pipeline.

## Next Steps

- Implement `load_to_db.py` to load data into PostgreSQL or Parquet  
- Develop Airflow DAGs for orchestration  
- Add real-time streaming ingestion via Kafka  
- Build dashboards or notebooks for visualization  
- Expand portfolio optimization algorithms  

## License

MIT License
