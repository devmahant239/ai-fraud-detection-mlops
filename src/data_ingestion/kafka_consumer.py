import json
from kafka import KafkaConsumer
import psycopg2


connection = psycopg2.connect(
    host="localhost",
    port=5434,
    database="fraud_db",
    user="admin",
    password="admin123"
)

cursor = connection.cursor()


consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",

    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    ),

    auto_offset_reset="earliest",
    group_id="fraud-detection-group"
)


for message in consumer:

    transaction = message.value


    cursor.execute(
        """
        INSERT INTO transactions
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            transaction["transaction_id"],
            transaction["user_id"],
            transaction["amount"],
            transaction["transaction_type"],
            transaction["merchant_category"],
            transaction["location"],
            transaction["device_type"],
            transaction["failed_attempts"],
            transaction["is_international"],
            transaction["transaction_time"],
            transaction["is_fraud"]
        )
    )

    connection.commit()

    print(
        f"Stored transaction: {transaction['transaction_id']}"
    )