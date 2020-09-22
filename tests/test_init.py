
import os

import canapi as cp


def test_polygon():
    polygon = cp.api("polygon")
    assert polygon


def test_estimize():
    estimize = cp.api("estimize")
    assert estimize


def test_iex():
    iex = cp.api("iexcloud")
    assert iex


def test_coinbasepro():
    cbpro = cp.api("coinbasepro")


def test_registry():

    httpbin = cp.api("httpbin")
    assert not httpbin

def test_add():

    path = cp.__path__[0] + "/../tests/test_registry"
    cp.add_registry("test", path)

    httpbin = cp.api("httpbin")
    assert httpbin
