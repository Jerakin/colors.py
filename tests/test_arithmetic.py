import pytest

from colors import RGBColor, RGBFloatColor
from colors import HSVColor
from colors import HexColor


def test_init_with_float(caplog):
    RGBColor(204.0, 122.4, 122.4)
    assert "value is not an integer, it will be rounded to" in caplog.text


def test_color_multiplication_operator():
    assert RGBFloatColor(0.78, 0.78, 0.78) * RGBFloatColor(0.28, 0.28, 0.28) == RGBFloatColor(0.22, 0.22, 0.22)
    assert HexColor("ff9999") * HexColor("cccccc") == RGBColor(204, 122, 122)


def test_color_addition_operator():
    assert HexColor("ff9999") + RGBColor(0, 10, 10) == RGBColor(255, 163, 163)


def test_color_subtracting_operator():
    assert HexColor("ff9999") - RGBColor(10, 10, 10) == RGBColor(245, 143, 143)


def test_color_division_operator():
    assert RGBFloatColor(0.7, 0.7, 0.7) / RGBFloatColor(0.2, 0.2, 0.2) == RGBFloatColor(3.5, 3.5, 3.5)
    assert RGBColor(179, 179, 179) / RGBColor(51, 51, 51) == RGBFloatColor(3.5, 3.5, 3.5)

    assert RGBFloatColor(0.2, 0.2, 0.2) / RGBFloatColor(1, 1, 1) == RGBFloatColor(0.2, 0.2, 0.2)
    assert RGBColor(51, 51, 51) / RGBColor(255, 255, 255)  == RGBColor(51, 51, 51)


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        color_HexColor = HexColor("00ffff")
        color_RGBColor = RGBColor(100, 100, 100)
        color_RGBColor / color_HexColor
