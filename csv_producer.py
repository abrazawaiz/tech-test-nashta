import csv
import json
import time
from kafka import KafkaProducer

# Kafka Config
KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "ecommerce_customer_v2"
CSV_FILE = "data/ecommerce_customer.csv"

def dict_to_struct(row):
    fields = [{"type": "string", "optional": True, "field": k} for k in row.keys()]
    
    return {
        "schema": {
            "type": "struct",
            "fields": fields,
            "optional": False,
            "name": "ecommerce_customer_record"
        },
        "payload": row
    }

def main():
    print("Starting CSV Kafka Producer...")
    print(f"Broker: {KAFKA_BROKER}")
    print(f"Topic : {TOPIC_NAME}")
    print(f"File  : {CSV_FILE}")
    print("-" * 50)

    # Inisialisasi Producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        retries=5,
    )

    try:
        with open(CSV_FILE, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            
            for i, row in enumerate(reader, start=1):
                
                clean_row = {k: (v if v != "" else None) for k, v in row.items()}
                
                message = dict_to_struct(clean_row)
                
                producer.send(TOPIC_NAME, value=message)
                print(f"[SENT {i}] {clean_row['Customer ID']}") 
                
                time.sleep(0.01) 

        producer.flush()
        print("-" * 50)
        print("All data published successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        producer.close()
        print("Producer finished.")

if __name__ == "__main__":
    main()
