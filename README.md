# garconne

This is just a basic URL shortener app, mostly wrote to test CI/CD stuff around the app itself.

## Requirements

You've to install by yourself docker, docker-compose, make.

## Usage

```bash
# Setup the requirements, build and start the containers, run the tests, then cleanup
make

# Setup the requirements, build and start the containers, then display the live logs
make dev
# Same, only displaying the app logs
LOGS=app make dev

# Remove the containers
make clean
# Remove the containers, certificates, caches, binaries...
make wipe
```

Browse to

- The app itself https://localhost (or https://app.localhost)
- The app's OpenAPI doc https://localhost/docs
- Traefik dashboard https://traefik.localhost
- Prometheus https://prometheus.localhost
- Grafana https://grafana.localhost
- Redis Insight https://redis.localhost

When required, the default login is `admin`, password `garconne`

## Development

For a quicker development, install Python 3.9 & Poetry, then

```
docker run -d -p 6379:6379 --name redis redis
docker run -d -p 8001:8001 --name redisinsight redislabs/redisinsight
poetry install
poetry run uvicorn garconne.main:app --reload
```

Then you can test stuff in another terminal

```bash
curl -I http://localhost:8000/health
export ID=$(curl -X POST "http://localhost:8000/api/v1/shorten/https://user:password@example.com/bli/bla/bli/index.html?hello=world&world=hello")
curl http://localhost:8000/api/v1/lookup/$ID
```

## TODO

About the code itself

- Add [gunicorn](https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/gunicorn_conf.py)
- Organize the code
- Improve the workflow
  - Execute pytest in the docker-compose context ?
  - Add a docker-compose.development.yml override to live reload the code ?
- Hide /status and /metrics in the app's logs
- Replace vegeta by locust

About the contrib

- Add alerts in prometheus from https://awesome-prometheus-alerts.grep.to
- Fix Grafana's datasources and dashboards
- Add an app dashboard in Grafana
- Setup Grafana notifiers (alerts)
- Setup AlertManager & MailHog
- Vue.js based WebUI to CRUD shortened URLs
- Add Keycloak over it [example](https://github.com/stevegroom/traefikGateway/blob/master/traefik/docker-compose.yaml)

Next: same same, but Golang
