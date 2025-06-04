.PHONY: help setup run stop test clean

help:
	@echo "Commands:"
	@echo "  make setup  - Initial setup"
	@echo "  make run    - Start platform"
	@echo "  make stop   - Stop platform"
	@echo "  make test   - Run tests"
	@echo "  make logs   - View logs"

setup:
	docker-compose build
	docker-compose run --rm backend python -c "print('✅ Setup complete!')"

run:
	docker-compose up -d
	@echo "✅ Platform running!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"

stop:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose exec backend pytest
	docker-compose exec frontend npm test

clean:
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf frontend/node_modules