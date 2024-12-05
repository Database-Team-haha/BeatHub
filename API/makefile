# Load environment variables from .env file
include .env

all: createdb runreload

dropdb:
	PGPASSWORD=$(PASSWORD_DB) dropdb -h $(HOST_DB) -p $(PORT_DB) -U $(USER_DB) $(NAME_DB)

createdb:
	PGPASSWORD=$(PASSWORD_DB) createdb -h $(HOST_DB) -p $(PORT_DB) -U $(USER_DB) $(NAME_DB)

run:
	uvicorn app:app --host 172.20.10.3 --port 8000

runreload:
	uvicorn app:app --host 172.20.10.3 --port 8000 --reload

re: dropdb all