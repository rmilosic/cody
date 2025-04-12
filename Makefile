dev:
	uv run langgraph dev --allow-blocking

test:
	uv run pytest --langsmith-output

viewer:
	cd viewer && npm run dev