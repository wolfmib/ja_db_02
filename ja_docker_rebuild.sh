docker compose build && docker compose down && docker compose up -d && docker ps

echo "see the docker by command e.g."
echo "docker exec -it ja_db_02-db-1 psql -U ja_admin -d ja_clients"


echo "🌐 Opening pgweb UI... http://localhost:8081"
open http://localhost:8081

echo "BI Opening superset UI ... http://localhost:8088"
open http://localhost:8088

echo "Flink Services UP .... http://localhost:8082"
open http://localhost:8082/

echo "Current activated 3 servcies"


echo "| Prompt        | Value you can use                  |"
echo "|---------------|------------------------------------|"
echo "| Username      | `admin`                            |"
echo "| User first name | `John`                           |"
echo "| User last name  | `Hung`                           |"
echo "| Email         | `john@jagroupai.com`               |"
echo "| Password      | your choice, e.g. `admin123!`      |"
