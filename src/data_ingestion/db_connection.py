import psycopg2


connection = psycopg2.connect(
    host="localhost",
    port=5434,
    database="fraud_db",
    user="admin",
    password="admin123"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    transaction_id VARCHAR(100),
    user_id VARCHAR(50),
    amount FLOAT,
    transaction_type VARCHAR(50),
    merchant_category VARCHAR(50),
    location VARCHAR(50),
    device_type VARCHAR(50),
    failed_attempts INT,
    is_international INT,
    transaction_time TIMESTAMP,
    is_fraud INT
)
""")

connection.commit()

print("Table created successfully")

cursor.close()
connection.close()