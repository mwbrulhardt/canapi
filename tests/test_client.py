
import json

from canapi.client import Endpoint, ClientAPI


def test_client_empty_endpoints():

    httpbin = ClientAPI(
        name="httpbin",
        uri="https://httpbin.org",
        endpoints = {}
    )

    assert httpbin
    assert httpbin.name == "httpbin"

    del ClientAPI.apis[httpbin.name]


def test_client_endpoints_one_level():

    methods = ["get", "post", "delete", "patch", "put"]
    config = lambda name: {"method": name, "path": "/anything"}

    httpbin = ClientAPI(
        name="httpbin",
        uri="https://httpbin.org",
        endpoints={m: config(m) for m in methods}
    )

    for m in methods:
        assert hasattr(httpbin, m)

        params = {
            'p0': '1'
        }
        endpoint = getattr(httpbin, m)
        data = endpoint(params=params)
        assert params == data['args']

    del ClientAPI.apis[httpbin.name]


def test_client_endpoints_with_template():

    httpbin = ClientAPI(
        name="httpbin",
        uri="https://httpbin.org",
        endpoints={
            "stream": {
                "method": "GET",
                "path": "/stream/${n}"
            }
        }
    )

    data = httpbin.stream(url_params={"n": 10})
    assert data

    del ClientAPI.apis[httpbin.name]


def test_subapi_groups():

    httpbin = ClientAPI(
        name="httpbin",
        uri="https://httpbin.org",
        endpoints={
            "anything": {
                "get": {
                    "method": "get",
                    "path": "/anything"
                },
                "post": {
                    "method": "post",
                    "path": "/anything"
                }
            }
        }
    )

    data = httpbin.anything.get()
    assert data

    del ClientAPI.apis[httpbin.name]
