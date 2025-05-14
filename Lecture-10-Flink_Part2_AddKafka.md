## Step 2: Add Kafka + Zookeeper Docker Containers
- ✅ Goal: Flink consumes from a Kafka topic
- ⚙️ Add Kafka and Zookeeper to your existing docker-compose.yml
- 🔁 Run a test Kafka producer + Flink consumer to confirm streaming works

---

---

## edit yml

  zookeeper:
    image: confluentinc/cp-zookeeper:7.2.1
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.2.1
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  kafdrop:
    image: obsidiandynamics/kafdrop
    depends_on:
      - kafka
    ports:
      - "9000:9000"
    environment:
      KAFKA_BROKERCONNECT: kafka:9092


---

## docker ps to check


---

## go to Lecture_Practice_Kafka.md to check how to do quick-test
---

