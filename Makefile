start-with-ml:
	docker-compose up -d --build
start-infra:
	docker-compose up -d --build database queue cdn-master cdn-volume
start: start-infra
	docker-compose up -d --build api worker frontend
stop:
	docker-compose down
test-dependencies:
	cd tests/ && pip install -r requirements.txt
test:
	cd tests/ && behave