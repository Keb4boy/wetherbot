start:
	poetry run uvicorn weather.main:app --port 8000 --host 0.0.0.0

install:
	pip install poetry && \
	poetry install
