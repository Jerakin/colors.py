import pytest

from colors import RGBColor
from colors import HSVColor
from colors import HexColor


def test_color_multiplication_operator():
    assert HexColor('ff9999') * HexColor('cccccc') == RGBColor(204.0, 122.4, 122.4)


def test_color_multiplication_function():
    assert RGBColor(100, 100, 100).multiply(HSVColor(0, 1, 1)).hex == HexColor("640000")


def test_color_addition_operator():
    assert HexColor('ff9999') + RGBColor(10, 10, 10) == RGBColor(255, 163, 163)


def test_color_addition_function():
    assert HexColor('aaffcc').add(RGBColor(10, 10, 10)) == RGBColor(180, 255, 214)


def test_color_subtracting_operator():
    assert HexColor('ff9999') - RGBColor(10, 10, 10) == RGBColor(245, 143, 143)


def test_color_subtracting_function():
    assert HexColor('aaffcc').subtract(RGBColor(10, 10, 10)) == RGBColor(160, 245, 194)


def test_color_dividing_operator():
    assert HexColor('ff9999') / RGBColor(10, 10, 10) == RGBColor(26, 15, 15)


def test_color_dividing_function():
    assert HexColor('aaffcc').divide(RGBColor(10, 10, 10)) == RGBColor(17, 26, 20)


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        color_HexColor = HexColor('00ffff')
        color_RGBColor = RGBColor(100, 100, 100)
        color_RGBColor / color_HexColor
