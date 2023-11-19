start:
	poetry run uvicorn weather.main:app --port 8000 --host 0.0.0.0 --reload --reload-dir . --log-config=log_config.ini

install:
	pip install poetry && \
	poetry install
