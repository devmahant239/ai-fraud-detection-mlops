import csv
from transaction_generator import generate_transaction


def generate_csv(file_path, rows=1000):
    data = [generate_transaction() for _ in range(rows)]

    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"Generated {rows} transactions at {file_path}")


if __name__ == "__main__":
    generate_csv("data/raw/transactions.csv", rows=1000)