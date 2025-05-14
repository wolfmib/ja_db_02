
# start evething from your repo

# Step docker ps
johnnyhung@Johnny-MacMini-Work-Stataion ja_db_02 % docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS                    PORTS                                             NAMES
d7cfd84a509e   flink:1.17                        "/docker-entrypoint.…"   15 minutes ago   Up 14 minutes             6123/tcp, 8081/tcp                                ja_db_02-flink-taskmanager-1
cff060aedf46   obsidiandynamics/kafdrop          "/kafdrop.sh"            15 minutes ago   Up 14 minutes             0.0.0.0:9000->9000/tcp                            ja_db_02-kafdrop-1
b3a2ad913158   ja_db_02-automation               "bash -c 'python3 au…"   15 minutes ago   Up 14 minutes                                                               ja_db_02-automation-1
18b9d7bdf03e   ja_db_02-superset                 "/usr/bin/run-server…"   15 minutes ago   Up 14 minutes (healthy)   0.0.0.0:8088->8088/tcp                            ja_db_02-superset-1
b3cbdcbfc206   confluentinc/cp-kafka:7.2.1       "/etc/confluent/dock…"   15 minutes ago   Up 14 minutes             0.0.0.0:9092->9092/tcp                            ja_db_02-kafka-1
a19b889b3868   flink:1.17                        "/docker-entrypoint.…"   15 minutes ago   Up 14 minutes             6123/tcp, 0.0.0.0:8082->8081/tcp                  ja_db_02-flink-jobmanager-1
4caa4c3fcbb3   sosedoff/pgweb                    "/usr/bin/pgweb --bi…"   15 minutes ago   Up 14 minutes             0.0.0.0:8081->8081/tcp                            ja_db_02-pgweb-1
a9d6d4f131b2   postgres:15                       "docker-entrypoint.s…"   16 minutes ago   Up 15 minutes             0.0.0.0:5432->5432/tcp, 0.0.0.0:15432->5432/tcp   ja_db_02-db-1
5f4aea41e4ea   confluentinc/cp-zookeeper:7.2.1   "/etc/confluent/dock…"   16 minutes ago   Up 15 minutes             2888/tcp, 0.0.0.0:2181->2181/tcp, 3888/tcp        ja_db_02-zookeeper-1


# Step see  network
johnnyhung@Johnny-MacMini-Work-Stataion ja_db_02 % docker network ls
NETWORK ID     NAME               DRIVER    SCOPE
2f7b456f9f4d   bridge             bridge    local
29eee300c03b   host               host      local
4ecb71a21175   ja_db_02_default   bridge    local
dfb1e7c0c9b2   none               null      local



## Step: List Topics
docker run --network ja_db_02_default --rm confluentinc/cp-kafka:7.2.1 kafka-topics --bootstrap-server kafka:9092 --list



#########################



## Step: Create Topic
docker run --network ja_db_02_default --rm confluentinc/cp-kafka:7.2.1 kafka-topics --bootstrap-server kafka:9092 --create --topic testIMissYou -- partitions 1 --replication-factor 1


###########################




## Step: Send Message
## you need to added -i (note)
docker run -i --network ja_db_02_default --rm confluentinc/cp-kafka:7.2.1 kafka-console-producer --broker-list kafka:9092 --topic testIMissYou


#################




## Step: Consume Message
docker run --network ja_db_02_default --rm confluentinc/cp-kafka:7.2.1 kafka-console-consumer --bootstrap-server kafka:9092 --topic testIMissYou --from-beginning --timeout-ms 5000


########################













