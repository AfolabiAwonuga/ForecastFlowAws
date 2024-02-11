test:
	pytest --cov=ingest_function

lint:
	black .

sort_imports:
	isort .

run: test lint sort_imports