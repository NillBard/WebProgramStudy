clean:
	rm -fr *.egg-info dist

sdist: clean
	python3 setup.py sdist

postgres:
	docker stop analyzer-postgres || true
	docker run --rm --detach --name=analyzer-postgres \
		--env POSTGRES_USER=user \
		--env POSTGRES_PASSWORD=hackme \
		--env POSTGRES_DB=analyzer \
		--publish 5432:5432 postgres


test: postgres
	pytest -vv --cov=analyzer --cov-report=term-missing test

