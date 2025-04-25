docker compose build && docker compose down && docker compose up -d && docker ps

echo "see the docker by command e.g."
echo "docker exec -it ja_db_02-db-1 psql -U ja_admin -d ja_clients"


echo "🌐 Opening pgweb UI... http://localhost:8081"
open http://localhost:8081

echo "BI Opening superset UI ... http://localhost:8088"
open http://localhost:8088


