# Tech Test @ NashTa Group

## How to Run

# 1. Build & Push Producer Image
docker build -t abrazawaiz/csv-producer-nashta:latest .
docker push abrazawaiz/csv-producer-nashta:latest

# 2. Deploy Infrastructure (Kafka, Kafka Connect, Postgres)
kubectl apply -f k8s/kafka.yaml
kubectl apply -f k8s/postgres.yaml

# Wait until all pods are running
kubectl get pods -w

# 3. Run Producer Job (publish CSV to Kafka topic)
kubectl apply -f k8s/csv-producer-job.yaml

# 4. Deploy Kafka Connector
# Enable port forwarding (keep this terminal open)
kubectl port-forward svc/kafka-connect 8083:8083

# In another terminal, submit connector config
curl -X POST -H "Content-Type: application/json" \
  --data @postgres-sink.json \
  http://localhost:8083/connectors

# 5. Verification
kubectl exec -it deploy/postgres -- \
psql -U myuser -d ecommerce \
-c "SELECT * FROM ecommerce_customer_v2 LIMIT 10;"

# Cleanup
kubectl delete -f k8s/
kubectl delete job csv-producer-job
