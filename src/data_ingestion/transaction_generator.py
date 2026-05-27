import random
import uuid
from datetime import datetime


TRANSACTION_TYPES = ["online", "pos", "atm", "bank_transfer"]
MERCHANT_CATEGORIES = ["grocery", "electronics", "travel", "fuel", "shopping", "restaurant"]
LOCATIONS = ["Ahmedabad", "Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad"]
DEVICE_TYPES = ["mobile", "web", "card", "atm"]


def generate_transaction():
    amount = round(random.uniform(100, 200000), 2)
    failed_attempts = random.randint(0, 5)
    is_international = random.choice([0, 1])

    is_fraud = 1 if amount > 100000 or failed_attempts >= 3 or is_international == 1 else 0

    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": f"U{random.randint(1000, 9999)}",
        "amount": amount,
        "transaction_type": random.choice(TRANSACTION_TYPES),
        "merchant_category": random.choice(MERCHANT_CATEGORIES),
        "location": random.choice(LOCATIONS),
        "device_type": random.choice(DEVICE_TYPES),
        "failed_attempts": failed_attempts,
        "is_international": is_international,
        "transaction_time": datetime.now().isoformat(),
        "is_fraud": is_fraud,
    }