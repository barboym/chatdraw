set -a; source ../.env; set +a
docker run -d \
  --name my-postgres \
  -e POSTGRES_PASSWORD=$DB_PASSWORD \
  -v ${DB_LOCALPATH}:/var/lib/postgresql/data \
  -p 5432:${DB_PORT} \
  postgres:17