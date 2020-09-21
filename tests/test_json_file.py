
import canopy as cp


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
