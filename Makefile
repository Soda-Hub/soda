all: test dev

dev:
	uvicorn app:app --reload

prod:
	gunicorn -w 4 -k uvicorn.workers.UvicornWorker --log-level debug app:app

test:
	pytest --cov . tests.py
	-rm test.db
