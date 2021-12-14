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

devenv: clean
	rm -rf env
	# создаем новое окружение
	python3.8 -m venv env
	# обновляем pip
	pip install -U pip
	# устанавливаем основные + dev зависимости из extras_require (см. setup.py)
	pip install -U'.[dev]'