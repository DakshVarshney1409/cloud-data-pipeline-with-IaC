# 📁 README: Project 2 & 3 - Cloud-Ready Data Pipeline & IaC

This project combines the **High-Throughput Data Pipeline (Project 2)** with **Infrastructure as Code (IaC) using Terraform (Project 3)**, showcasing expertise in **Microservices, Docker, Redis caching, MongoDB persistence, and Cloud DevOps principles.**

## 🌟 Project Goals

* **Microservices:** Decouple data generation from ingestion.
* **High-Throughput:** Ingest market data at high frequency (simulated 20+ updates/sec).
* **Caching (Redis):** Implement a low-latency cache for the latest price data.
* **Persistence (MongoDB):** Store high-volume time-series data using a NoSQL database.
* **DevOps/IaC (Terraform):** Define and provision the entire cloud infrastructure (VPC, ECR, IAM Roles) necessary for deployment.
* **Containerization (Docker Compose):** Define and run the local development environment using a single command.

## ⚙️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Microservices** | Python/FastAPI | **Data Generator** and **Ingestion API** (Decoupled Architecture) |
| **Containerization** | Docker, Docker Compose | Environment management, service definition, and networking |
| **Caching** | Redis | High-speed storage for latest price (`last_price:AAPL`) |
| **Persistence** | MongoDB | High-volume storage for historical quotes |
| **DevOps/IaC** | Terraform, AWS (Simulated) | Provisioning ECR, VPC, IAM roles for production deployment |

---

## 🚀 Setup and Run Instructions (Local Docker)

### 1. Environment Setup

1.  **Install Dependencies:** Ensure you have the required Python packages for connections and the generator:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Verify Docker:** Confirm `docker compose` is installed and functioning.

### 2. Run the Infrastructure

Navigate to the project root directory (where `docker-compose.yml` is located).

1.  **Build and Start All Services:** This creates the Python image and starts Redis and MongoDB.
    ```bash
    docker compose up --build -d
    ```

2.  **Verify Status:** Ensure all three containers are running:
    ```bash
    docker ps
    ```

3.  **Start the Data Feed (Generator):** Open a **new terminal** and run the external simulation script.
    ```bash
    python project2_generator.py
    ```

### 3. Verification

* **API Health Check:** Verify the Ingestion API can connect to both Redis and Mongo.
    ```bash
    curl http://localhost:8000/health
    # Expected: {"redis_status": "OK", "mongodb_status": "OK"}
    ```
* **Low-Latency Cache Test:** Fetch the latest price (pulled directly from Redis). Run this multiple times rapidly.
    ```bash
    curl http://localhost:8000/market_data/last_price/AAPL
    ```

---

## ☁️ Phase 3: Cloud Migration (Terraform IaC)

The `terraform/` directory contains the Infrastructure as Code used to provision the production environment.

### 1. IaC Execution (Simulated)

In a live environment, these commands provision the necessary cloud resources:

```bash
cd terraform/
terraform init
terraform plan 
# terraform apply (Actual resource creation)

2. IaC Components - it is a table : Correct it. 
FileAWS Resources ProvisionedDevOps Principlemain.tfVPC & Subnets: Network foundation for the application.Networking/Cloud Architecturemain.tfECR Repository: Storage for the final production Docker image.Continuous Integration (CI)main.tfIAM Roles: Permissions required for the container runtime (ECS Task Execution Role).Security/Least PrivilegeThe output.tf file provides the ecr_repository_url and vpc_id—critical parameters that would be passed to a CI/CD pipeline (e.g., GitHub Actions or Jenkins) to facilitate the final deployment to a service like AWS ECS Fargate.