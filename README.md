Tech Test @ NashTa Group

## How to Run

### 1. Build & Push Producer Image
\\\bash
docker build -t abrazawaiz/csv-producer-nashta:latest .
docker push abrazawaiz/csv-producer-nashta:latest
\\\

### 2. Deploy Infrastructure
Start Kafka, Kafka Connect, and Postgres on Kubernetes:
\`\`\`bash
kubectl apply -f k8s/kafka.yaml
kubectl apply -f k8s/postgres.yaml
\`\`\`
Wait until all pods are running:
\`\`\`bash
kubectl get pods -w
\`\`\`

### 3. Run Producer Job
This job reads the CSV and publishes messages to the topic \`ecommerce_customer_v2\`:
\`\`\`bash
kubectl apply -f k8s/csv-producer-job.yaml
\`\`\`

### 4. Deploy Kafka Connector
1. **Enable Port Forwarding** (keep this terminal open):
\`\`\`bash
kubectl port-forward svc/kafka-connect 8083:8083
\`\`\`

2. **Submit Connector Config** (in a new terminal):
\`\`\`bash
curl -X POST -H "Content-Type: application/json" \
  --data @postgres-sink.json \
  http://localhost:8083/connectors
\`\`\`

### 5. Verification
Check if data is synced to PostgreSQL:
\`\`\`bash
kubectl exec -it deploy/postgres -- psql -U myuser -d ecommerce -c "SELECT * FROM ecommerce_customer_v2 LIMIT 10;"
\`\`\`

---

## 🧹 Cleanup
Remove all resources:
\`\`\`bash
kubectl delete -f k8s/
kubectl delete job csv-producer-job
\`\`\`

