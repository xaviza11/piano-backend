start:
	uvicorn main:app --reload

test:
    pytest tests/
