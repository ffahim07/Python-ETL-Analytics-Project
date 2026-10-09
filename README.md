# 🐍 Automated Data ETL Pipeline & Analytics (Python & SQLite)

## 📌 Project Overview
This is a portfolio-ready Python project that implements an automated **ETL (Extract, Transform, Load)** pipeline. The pipeline extracts raw transactional sales data from a CSV source, cleans and processes the data using Python, and loads the structured data into a lightweight SQLite database for analytics readiness.

## ⚙️ How the Pipeline Works
1. **Extract (`extract_data`)**: 
   * Programmatically checks for and generates a sample raw sales CSV file (`raw_sales_data.csv`) if it doesn't exist inside the `data/` directory.
   * Reads the raw dataset securely using Python's built-in file handling modules.
2. **Transform (`transform_data`)**: 
   * Performs data validation and cleaning by identifying and dropping duplicate rows.
   * Computes key metrics dynamically, such as calculating the `total_amount` (`price * quantity`) for every transaction.
3. **Load (`load_data`)**: 
   * Connects to a local SQLite database (`sales_warehouse.db`).
   * Automatically creates a structured target table (`cleaned_sales`) and stores the processed data reliably.

## 📂 Project Structure
```text
Python_ETL_Analytics_Project/
│
├── data/
│   ├── raw_sales_data.csv
│   └── sales_warehouse.db
│
├── venv/
├── etl_pipeline.py
└── README.md