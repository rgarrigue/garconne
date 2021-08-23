from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

# TODO(rgarrigue): Starlette ":path" convertor used in shortening route get rid
# of the ?xxx part. Restablish the full URL for proper testing once fixed
# test_url = "https://user:password@httpbin.org:443/post?test=yes&debug=true"
test_url = "https://user:password@httpbin.org:443/post"


def test_health():
    health = client.head("/health")
    assert health.status_code == 200, health


def test_shorten():
    shorten = client.post(f"/api/v1/shorten/{test_url}")
    assert shorten.status_code == 200, shorten
    assert shorten.text != "", shorten


def test_lookup():
    shorten = client.post(f"/api/v1/shorten/{test_url}")
    lookup = client.get(f"/api/v1/lookup/{shorten.text}")
    assert lookup.status_code == 200, lookup
    assert lookup.text == test_url, lookup


def test_redirect():
    # request.get interpret ":password/..." as a port number, hence a simplified test url
    test_url = "https://httpbin.org:443/get"

    shorten = client.post(f"/api/v1/shorten/{test_url}")
    redirect = client.get(f"/{shorten.text}")
    assert redirect.status_code == 307, redirect
