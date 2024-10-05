import pytest

from colors import RGBColor as rgb
from colors import HSVColor as hsv
from colors import HexColor as hex


def test_color_multiplication_operator():
    assert hex('ff9999') * hex('cccccc') == rgb(204.0, 122.4, 122.4)


def test_color_multiplication_function():
    assert rgb(100, 100, 100).multiply(hsv(0, 1, 1)).hex == hex("640000")


def test_color_addition_operator():
    assert hex('ff9999') + rgb(10, 10, 10) == rgb(255, 163, 163)


def test_color_addition_function():
    assert hex('aaffcc').add(rgb(10, 10, 10)) == rgb(180, 255, 214)


def test_color_subtracting_operator():
    assert hex('ff9999') - rgb(10, 10, 10) == rgb(245, 143, 143)


def test_color_subtracting_function():
    assert hex('aaffcc').subtract(rgb(10, 10, 10)) == rgb(160, 245, 194)


def test_color_dividing_operator():
    assert hex('ff9999') / rgb(10, 10, 10) == rgb(26, 15, 15)


def test_color_dividing_function():
    assert hex('aaffcc').divide(rgb(10, 10, 10)) == rgb(17, 26, 20)


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        color_hex = hex('00ffff')
        color_rgb = rgb(100, 100, 100)
        color_rgb / color_hex
