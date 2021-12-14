postgres:
	docker stop analyzer-postgres || true
	docker run --rm --detach --name=analyzer-postgres \
		--env POSTGRES_USER=postgres \
		--env POSTGRES_PASSWORD=postgres \
		--env POSTGRES_DB=analyzer \
		--publish 5432:5432 postgres

clean:
	rm -fr *.egg-info dist

sdist: clean
	python3 setup.py sdist

test: postgres
	pytest -vv --cov=analyzer --cov-report=term-missing test

