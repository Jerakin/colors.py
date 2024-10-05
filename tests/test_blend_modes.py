from colors import RGBColor, RGBFloatColor, HSVColor
from colors import HexColor


def test_screen():
    assert RGBColor(195, 49, 171).screen(RGBColor(107, 194, 145)) == RGBColor(220, 206, 219)
    assert HexColor("ff9999").screen(RGBColor(10, 10, 10)).hex == HexColor("ff9d9d")


def test_difference():
    assert RGBColor(195, 49, 171).difference(RGBColor(107, 194, 145)) == RGBColor(88, 145, 26)
    assert HexColor("ff9999").difference(RGBColor(10, 10, 10)).hex == HexColor("f58f8f")


def test_overlay():
    assert RGBColor(195, 49, 171).overlay(RGBColor(107, 194, 145)) == RGBColor(164, 156, 183)


def test_invert():
    assert HexColor("000000").invert() == RGBColor(255, 255, 255)


def test_color_burn():
    assert RGBColor(195, 49, 171).color_burn(RGBColor(107, 194, 145)) == RGBColor(61, 0, 91)


def test_linear_burn():
    assert RGBColor(195, 49, 171).linear_burn(RGBColor(107, 194, 145)) == RGBColor(47, 0, 61)


def test_linear_dodge():
    assert RGBColor(195, 49, 171).linear_dodge(RGBColor(14, 19, 14)) == RGBColor(209, 68, 185)


def test_color_dodge():
    assert RGBColor(195, 49, 171).color_dodge(RGBColor(14, 19, 14)) == RGBColor(59, 24, 42)


def test_color_divide():
    assert RGBColor(195, 49, 171).divide(RGBColor(107, 194, 145)) == RGBColor(140, 255, 216)


def test_color_subtract():
    assert RGBColor(195, 49, 171).subtract(RGBColor(107, 194, 145)) == RGBColor(0, 145, 0)


def test_color_multiplication_function():
    assert RGBColor(100, 100, 100).multiply(HSVColor(0, 1, 1)).hex == HexColor("640000")


def test_color_addition_function():
    assert HexColor("aaffcc").add(RGBColor(10, 0, 10)) == RGBColor(180, 255, 214)
