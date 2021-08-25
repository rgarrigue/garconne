.DEFAULT_GOAL := default

default: setup lint build run unit_test load_test wipe
dev: setup lint build clean run unit_test logs

setup:
	contrib/scripts/mkcert_install.sh
	contrib/scripts/generate_localhost_certificate.sh
	contrib/scripts/vegeta_install.sh

build:
	docker-compose build --pull --no-cache

run:
	docker-compose up -d --scale app=2
	sleep 60

logs:
	docker-compose logs -f $(LOGS)

lint:
	poetry run black --line-length=120 .
	poetry run flake8
	poetry run isort -e --color --gitignore garconne/*.py
	poetry run mypy .
	shellcheck contrib/scripts/*.sh

unit_test:
	# Using FastAPI's TestClient means we need to run the unit tests inside the compose network
	# Running "poetry run pytest" fails because it's unable to resolve redis
	docker-compose run --rm --entrypoint 'sh -c' app 'pip3 install pytest requests ; pytest'

load_test:
	echo "POST https://app.localhost/api/v1/shorten/https://user:password@test.com:443/test/index.html" | vegeta attack -duration=300s -rate=10 | vegeta report
	# echo "POST http://app.localhost:8000/api/v1/shorten/https://user:password@test.com:443/test/index.html" | vegeta attack -duration=300s -rate=10 | vegeta report

clean:
	docker-compose down
	docker rmi -f localhost/garconne

wipe:
	docker-compose down
	docker rmi -f localhost/garconne
	rm -rf mkcert contrib/certs/*.pem vegeta .*_cache */__pycache__
