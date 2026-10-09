import os
import csv
import sqlite3
from datetime import datetime

# 1. EXTRACT: স্যাম্পল র ডেটা সিএসভি ফাইল তৈরি এবং রিড করা
def extract_data():
    print("--- 1. EXTRACTING DATA ---")
    
    os.makedirs('data', exist_ok=True)
    file_path = 'data/raw_sales_data.csv'
    
    # ডামি সিএসভি ফাইল তৈরি করা যদি না থাকে
    if not os.path.exists(file_path):
        header = ['order_id', 'customer_name', 'product', 'category', 'price', 'quantity', 'order_date']
        rows = [
            [101, 'Tanvir Ahmed', 'Laptop', 'Electronics', 55000.0, 1, '2026-10-01'],
            [102, 'Nusrat Jahan', 'Mouse', 'Electronics', 1200.0, 2, '2026-10-02'],
            [103, 'Rakibul Hasan', 'Keyboard', 'Electronics', 3500.0, 1, '2026-10-03'],
            [101, 'Tanvir Ahmed', 'Laptop', 'Electronics', 55000.0, 1, '2026-10-01'],  # Duplicate row for testing cleaning
            [104, 'Farzana Mimi', 'Monitor', 'Electronics', 15000.0, 1, '2026-10-04'],
            [105, 'Imran Khan', 'Mouse', 'Electronics', 1200.0, 3, '2026-10-05']
        ]
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        print("Sample raw CSV file created successfully.")

    # সিএসভি ফাইল রিড করা
    data_rows = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_rows.append(row)
            
    print(f"Data extracted successfully with {len(data_rows)} rows.")
    return data_rows

# 2. TRANSFORM: ডেটা ক্লিনিং এবং নতুন টোটাল অ্যামাউন্ট ক্যালকুলেশন
def transform_data(rows):
    print("\n--- 2. TRANSFORMING DATA ---")
    
    unique_rows = []
    seen = set()
    
    # ডুপ্লিকেট রিমুভ করা
    for row in rows:
        row_tuple = tuple(row.items())
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_rows.append(row)
            
    print(f"Removed duplicates: {len(rows) - len(unique_rows)} rows dropped.")
    
    # নতুন কলাম (total_amount) যোগ করা এবং ডেটা টাইপ ঠিক করা
    transformed = []
    for row in unique_rows:
        price = float(row['price'])
        quantity = int(row['quantity'])
        total_amount = price * quantity
        
        row['total_amount'] = total_amount
        transformed.append(row)
        
    print("Data transformation completed successfully.")
    return transformed

# 3. LOAD: প্রসেস করা ডেটা SQLite ডেটাবেজে লোড করা
def load_data(rows):
    print("\n--- 3. LOADING DATA INTO DATABASE ---")
    
    db_path = 'data/sales_warehouse.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # টেবিল তৈরি করা
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cleaned_sales (
            order_id INTEGER,
            customer_name TEXT,
            product TEXT,
            category TEXT,
            price REAL,
            quantity INTEGER,
            order_date TEXT,
            total_amount REAL
        )
    ''')
    
    # পুরোনো ডেটা ক্লিয়ার করে নতুন ডেটা ইনসার্ট করা
    cursor.execute('DELETE FROM cleaned_sales')
    
    for row in rows:
        cursor.execute('''
            INSERT INTO cleaned_sales (order_id, customer_name, product, category, price, quantity, order_date, total_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(row['order_id']),
            row['customer_name'],
            row['product'],
            row['category'],
            float(row['price']),
            int(row['quantity']),
            row['order_date'],
            float(row['total_amount'])
        ))
        
    conn.commit()
    conn.close()
    print("Data loaded successfully into SQLite database ('sales_warehouse.db').")

# পাইপলাইন রান করার মূল ফাংশন
if __name__ == "__main__":
    raw_data = extract_data()
    clean_data = transform_data(raw_data)
    load_data(clean_data)
    print("\n🎉 ETL Pipeline executed successfully from end to end!")