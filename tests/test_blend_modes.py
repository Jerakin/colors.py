from colors import RGBColor as rgb
from colors import HexColor as hex


def test_screen():
    assert hex('ff9999').screen(rgb(10, 10, 10)).hex == hex("ff9d9d")


def test_difference():
    assert hex('ff9999').difference(rgb(10, 10, 10)).hex == hex("f58f8f")

def test_overlay():
    assert hex('ff9999').overlay(rgb(10, 10, 10)).hex == hex("ff9b9b")


def test_invert():
    assert hex('000000').invert() == rgb(255, 255, 255)
