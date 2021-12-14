
postgres:
	docker stop analyzer-postgres || true
	docker run --rm --detach --name=analyzer-postgres \
		--env POSTGRES_USER=user \
		--env POSTGRES_PASSWORD=hackme \
		--env POSTGRES_DB=analyzer \
		-p 5432:5432 postgres

testing: postgres
	pytest -vv --cov=analyzer --cov-report=term-missing test


docker: sdist
	docker build --target=api -t $(PROJECT_NAME):$(VERSION) .

