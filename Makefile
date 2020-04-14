MONGO_DB_CONTAINER_NAME=tg_bot_mongo
DB_NAME=tg_bot_mongo_db
DB_USER=tg_bot_mongo_user
DB_USER_PWD=tg_bot_mongo_password
AUTH_DB=admin

.PHONY: start-db

start-db:
	docker-compose up -d

.PHONY: connect-to-db

connect-to-db:
	docker exec -it ${MONGO_DB_CONTAINER_NAME} bash -c "mongo --username ${DB_USER} --password ${DB_USER_PWD} --authenticationDatabase ${AUTH_DB} mongodb://localhost:27017/${DB_NAME}"
