@echo off
echo Starting local development environment...
docker compose up -d
timeout /t 5
echo MinIO should now be available at http://localhost:9001
echo Access Key: admin
echo Secret Key: admin123
