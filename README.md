# Data Engineering Project: Flight Prediction - Analytics Pipeline End-To-End

## 📌 Overview

This project is a comprehensive data engineering solution for analyzing Telegram chatbox interactions. The pipeline integrates data extraction, processing, visualization, and reporting using modern data engineering tools and technologies.

### Key Features
- **Data Extraction:** Collect Telegram chatbox interaction data
- **Processing:** Use Apache Spark for robust data transformation
- **Orchestration:** Apache Airflow for workflow management
- **Storage:** PostgreSQL for raw data, BigQuery for data warehousing
- **Visualization:** Interactive Streamlit dashboard
- **Containerization:** Docker for consistent environment deployment

## Target
The objective of this project is to create a **scalable and automated data pipeline** that:
- Extracts chatbot interaction data from Telegram.
- Processes and cleans data efficiently using Spark.
- Stores data in a structured format for further analysis.
- Provides business insights using visualizations.

## 🛠️ Technologies and Tools
This project uses the following technologies and tools:
- **Programming Languages:** Python, SQL
- **Data Extraction:** Telegram API via Make (Integromat)
- **ETL Tools:** Apache Airflow (workflow automation), Spark (data transformation)
- **Data Storage:** PostgreSQL (raw data), BigQuery (data warehouse)
- **Data Visualization:** Streamlit for interactive dashboards
- **Containerization:** Docker for deployment
- **Version Control:** Git, GitHub

## 📂 Project Structure

```
Telegram Chatbot Report - Data Pipeline/
├── dags/
│   ├── sql/
│   │   ├── transform_chat_data.sql
│   │   ├── clean_chat_data.sql
│   │   └── load_to_bigquery.sql
│   ├── dag_extract_data.py
│   ├── dag_transform_spark.py
│   ├── dag_load_data.py
├── .env
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── streamlit_dashboard.py
├── README.md
└── query.py
└── streaming.py
└── streamlit.py
```

## 📋 Prerequisites
- Git
- BigQuery Account
- Docker
- PostgreSQL Database
- Apache Airflow

## ⚙️ Installation
Follow these steps to get the project up and running on your local machine:

1. **Clone repository**:
   Clone this repository to your local machine:
   
bash
   git clone https://github.com/Gilight-Light/Covid19-Report-Telegram---Visualization-Data.git


2. **Docker build image**:
   We use Docker for environment consistency. To build the Docker image, run the following command:
   
bash
   astro dev docker start


### Run your pipeline and visual
1. **Run DAG**:
   We use Apache Airflow to automate the ETL tasks. Run the following command to initialize Airflow.
   - Login to Airflow at [localhost:8080](http://localhost:8080/) with user: airflow - password: airflow
   


2. **Run Streamlit**:
   
bash
   streamlit run streamlit.py

   - Open Streamlit at [localhost:8501](http://localhost:8501/)

3. **Get Telegram Chatbox Data in Make.com**

Demo: @UITCovid19_bot

## 🚀 Usage
1. **Airflow UI**:
   To monitor the pipeline, navigate to the Airflow UI:
   - Open your browser and go to [http://localhost:8080](http://localhost:8080).
   - Use the default credentials (usually admin/admin).

2. **Streamlit Dashboard**:
   This will launch an interactive dashboard on [http://localhost:8501](http://localhost:8501).

3. **Spark UI**:
      
      To monitor Spark jobs, navigate to the Spark UI:
      - Open your browser and go to [http://localhost:8081](http://localhost:8081).
      
   
### 🧑‍💻 Contributing
We welcome contributions! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (git checkout -b feature-name).
3. Make your changes and commit (git commit -am 'Add feature').
4. Push to the branch (git push origin feature-name).
5. Create a new Pull Request.

## 📚 Documentation
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Spark Documentation](https://spark.apache.org/docs/latest/)

