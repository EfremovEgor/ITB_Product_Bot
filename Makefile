run-db:
	docker run --name bot_database -p 5433:5433 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=product_bot_db -v ${PWD}/db_data:/var/lib/postgresql/data -d postgres:latest