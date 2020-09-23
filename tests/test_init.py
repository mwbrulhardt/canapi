
import os

import canapi as cp


def test_polygon():
    polygon = cp.api("polygon")
    assert False


def test_estimize():
    estimize = cp.api("estimize")
    assert estimize


def test_iex():
    iexcloud = cp.api("iexcloud")
    assert iexcloud


def test_coinbasepro():
    cbpro = cp.api("coinbasepro")


def test_from_config():
    httpbin = cp.from_config({
        "name": "httpbin",
        "uri": "https://httpbin.org",
        "endpoints": {
            "get_anything": {
                "method": "GET",
                "path": "/anything"
            }
        }
    })
    assert httpbin
