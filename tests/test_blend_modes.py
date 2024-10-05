from colors import RGBColor
from colors import HexColor


def test_screen():
    assert HexColor("ff9999").screen(RGBColor(10, 10, 10)).hex == HexColor("ff9d9d")


def test_difference():
    assert HexColor("ff9999").difference(RGBColor(10, 10, 10)).hex == HexColor("f58f8f")

def test_overlay():
    assert HexColor("ff9999").overlay(RGBColor(10, 10, 10)).hex == HexColor("ff9b9b")


def test_invert():
    assert HexColor("000000").invert() == RGBColor(255, 255, 255)
