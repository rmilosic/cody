dev:
	uv run langgraph dev

test:
	uv run pytest --langsmith-output

viewer:
	cd viewer && npm run dev