
# Stock Market Data - Automated Deployment with GitHub Actions

This repository contains a **complete CI/CD pipeline** for a stock market data application, which includes:

- A **Frontend (Dash App)** for data visualization.
- A **Backend API (FastAPI)** to provide stock data using Yahoo Finance.
- **Infrastructure provisioning with Terraform** to create an **AWS EC2 instance**.
- **Automated deployment using GitHub Actions**, Docker, and Docker Compose.

---

## 📂 Project Structure

```
.
├── .github/workflows/       # GitHub Actions workflows
├── Data_Api/                 # Backend FastAPI application
├── Stock/                     # Frontend Dash application
├── terraform/                 # Terraform scripts for EC2 creation
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

---

## 🔄 Workflow Trigger

The GitHub Actions workflow is triggered **on every push to the `master` branch**.

```yaml
on:
  push:
    branches:
      - master
```

---

## ⚙️ Workflow Overview

### 1️⃣ Build and Push Docker Images
- Checks out the repository.
- Logs into **Docker Hub** using credentials stored as secrets.
- Builds and pushes Docker images for:
    - The **Frontend app** (from `Stock/`).
    - The **Backend API** (from `Data_Api/`).

### 2️⃣ Provision Infrastructure with Terraform
- Initializes Terraform.
- Validates the configuration.
- Plans and applies the infrastructure (creates the EC2 instance).

### 3️⃣ Deploy the Application to EC2
- Retrieves the **public IP** of the created EC2 instance using `terraform output`.
- SSH into the EC2 instance using a private key stored in GitHub Secrets.
- Pulls the latest Docker images from Docker Hub.
- Starts the application using Docker Compose.

---

## 🔐 Required GitHub Secrets

The following secrets must be configured in your **GitHub repository** under:

**Settings → Secrets and variables → Actions**

| Secret Name             | Description                                      |
|-------------------------|--------------------------------------------------|
| `DOCKERHUB_USERNAME`     | Your Docker Hub username                        |
| `DOCKERHUB_TOKEN`        | Docker Hub Personal Access Token (not password) |
| `AWS_ACCESS_KEY_ID`      | AWS Access Key for Terraform                    |
| `AWS_SECRET_ACCESS_KEY`  | AWS Secret Access Key for Terraform             |
| `EC2_SSH_KEY`            | Private SSH key to connect to the EC2 instance  |

---

## 🚀 Deployment Process

1. Push code to the **master** branch.
2. GitHub Actions will:
    - Build Docker images for frontend and backend.
    - Push the images to Docker Hub.
    - Use Terraform to create or update an **EC2 instance**.
    - SSH into the EC2 instance.
    - Pull the latest images.
    - Run the app using **docker-compose up**.

---

## 🐳 Docker Compose Configuration

The `docker-compose.yml` defines two services:  
- **Data_Api** - Backend API (port 5000).
- **Stock** - Frontend Dash application (port 8050).

```yaml
services:
  Data_Api:
    build: ./Data_Api
    container_name: Data_Api
    ports:
      - "5000:5000"
    networks:
      - stock-net

  stock:
    build: ./Stock
    container_name: stock
    ports:
      - "8050:8050"
    depends_on:
      - Data_Api
    networks:
      - stock-net

networks:
  stock-net:
    driver: bridge
```

---

## 🌐 Accessing the Application

Once deployed, you can access the application at:

- **Frontend (Stock App Dashboard):**  
    `http://<EC2_PUBLIC_IP>:8050`

- **Backend (FastAPI Stock Data API):**  
    `http://<EC2_PUBLIC_IP>:5000`

Replace `<EC2_PUBLIC_IP>` with the actual public IP of your EC2 instance, which will be shown in the GitHub Actions log after Terraform deployment.

---

## 📊 Technologies Used

- **GitHub Actions** - Continuous Integration & Deployment
- **Docker & Docker Compose** - Containerized application management
- **Terraform** - Infrastructure as Code to provision AWS EC2
- **AWS EC2** - Cloud server hosting
- **FastAPI** - Backend API
- **Dash (Plotly)** - Frontend for stock data visualization

---

## 👨‍💻 Author

- **Sethu Gopalan**  
- GitHub: [SethuGopalan](https://github.com/SethuGopalan)

---

## 🔔 Important Notes

- Make sure all **required secrets** are properly added to GitHub.
- Ensure your AWS credentials have the required permissions to create EC2 instances, security groups, and attach SSH key pairs.
- Always test locally using:
    ```sh
    docker-compose up --build
    ```
- For secure access, ensure your **EC2 Security Group** allows inbound traffic on ports `5000` and `8050`.

---
