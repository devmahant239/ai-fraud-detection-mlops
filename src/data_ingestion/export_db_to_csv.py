import pandas as pd
import psycopg2


connection = psycopg2.connect(
    host="localhost",
    port=5434,
    database="fraud_db",
    user="admin",
    password="admin123"
)


query = "SELECT * FROM transactions"

df = pd.read_sql(query, connection)

df.to_csv("data/raw/transactions_from_db.csv", index=False)

print("Data exported successfully to data/raw/transactions_from_db.csv")

connection.close()