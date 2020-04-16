DB_CONTAINER_NAME=tg_bot_redis
DB_PWD=tg_bot_redis_pwd

.PHONY: start-db

start-db:
	docker-compose up -d

.PHONY: connect-to-db

connect-to-db:
	docker exec -it ${DB_CONTAINER_NAME} redis-cli -a ${DB_PWD}
