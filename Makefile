test:
	pytest tests/unit -s -vv --cov=comprasnet --cov-report term-missing

integration_test:
	pytest tests/integration -s -vv --cov=comprasnet --cov-report term-missing

