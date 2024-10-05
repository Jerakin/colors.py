import pytest
from colors import RGBColor
from colors import HSVColor
from colors import HexColor
from colors import RGBFloatColor


def test_rgb_color_object():
    colors = RGBColor(100, 100, 100)
    assert colors.red == 100 and colors.green == 100 and colors.blue == 100


def test_rgb_value_error():
    with pytest.raises(ValueError):
        RGBColor(300, 300, 300)


def test_rgb_value_error_negative():
    with pytest.raises(ValueError):
        RGBColor(-50, 50, 50)


def test_converting_rgb_to_hexadecimal():
    colors = RGBColor(100, 100, 100).hex
    assert colors.red == "64" and colors.green == "64" and colors.blue == "64"


def test_RGBFloatColor():
    colors = RGBFloatColor(1, 0, 1).float
    assert colors.red == 1.0 and colors.green == 0.0 and colors.blue == 1.0


def test_HexColor():
    colors = HexColor("646464").hex
    assert colors.red == "64" and colors.green == "64" and colors.blue == "64"


def test_HSVColor():
    colors = HSVColor(0, 1, 1).hsv
    assert colors.hue == 0 and colors.saturation == 1 and colors.value == 1


def test_hsv_value_error_s():
    with pytest.raises(ValueError):
        HSVColor(0, 2, 1)


def test_hsv_value_error_v():
    with pytest.raises(ValueError):
        HSVColor(0, 1, 2)


def test_hsv_hue_circle():
    assert HSVColor(2, 1, 1).hue == 0


def test_hex_value_error_len():
    with pytest.raises(ValueError):
        HexColor("#646464")


def test_hex_value_error_is_string():
    with pytest.raises(ValueError):
        HexColor(646464)


def test_hex_value_error_is_valid_HexColor():
    with pytest.raises(ValueError):
        HexColor("offfff")


def test_converting_hexadecimal_to_string():
    colors = str(RGBColor(100, 100, 100).hex)
    assert colors == "646464"


def test_hex_color_object():
    colors = HexColor("646464")
    assert colors.red == "64" and colors.green == "64" and colors.blue == "64"


def test_hex_get_color():
    colors = HexColor("646464").rgb
    assert colors.red == 100 and colors.green == 100 and colors.blue == 100


def test_convert_hex_to_HSVColor():
    colors = HexColor("646464").hsv
    assert colors.hue == 0 and colors.saturation == 0 and 0.3922 >= colors.value >= 0.3921


def test_converting_hex_object_to_list():
    colors = list(HexColor("646464").hsv)
    assert colors == [0.0, 0.0, 0.39215686274509803]


def test_hsv_color_object():
    colors = HSVColor(0, 1, 1)
    assert colors.hue == 0 and colors.saturation == 1 and colors.value == 1


def test_convert_hsv_to_RGBColor():
    colors = HSVColor(0, 1, 1).rgb
    assert colors.red == 255 and colors.green == 0 and colors.blue == 0


def test_coerce_object_to_string():
    import random
    colors = HSVColor(random.random(), random.random(), random.random())
    strings = 'style="color: RGBColor({})"'.format(colors)
    assert strings == 'style="color: RGBColor({}, {}, {})"'.format(*list(colors))


def test_color_equality():
    assert RGBColor(100, 100, 100) == HexColor("646464")
    assert HexColor("ffffff") != RGBColor(255, 255, 0)
    assert HexColor(u"ffffff") != RGBColor(255, 255, 0)


def test_rgb_float_color_object():
    colors = RGBFloatColor(1, 1, 1)
    assert colors.red == 1 and colors.green == 1 and colors.blue == 1


def test_RGBFloatColor_equality():
    assert RGBFloatColor(1, 1, 1) == RGBColor(255, 255, 255)
    assert RGBFloatColor(0.5, 0.5, 0.5) == RGBColor(128, 128, 128)
    assert RGBFloatColor(0.5, 0.5, 0.5).rgb == RGBColor(128, 128, 128)


def test_HexColor_float():
    assert RGBFloatColor(1, 0, 0) == HexColor("FF0000").float


def test_RGBColor_float():
    assert RGBFloatColor(1, 1, 1) == RGBColor(255, 255, 255).float


def test_HSVColor_float():
    assert RGBFloatColor(1, 0, 0) == HSVColor(0, 1, 1).float
