import pytest
from colors import RGBColor as rgb
from colors import HSVColor as hsv
from colors import HexColor as hex
from colors import random
from colors import RGBFloatColor as rgbf


def test_rgb_color_object():
    colors = rgb(100, 100, 100)
    assert colors.red == 100 and colors.green == 100 and colors.blue == 100


def test_rgb_value_error():
    with pytest.raises(ValueError):
        rgb(300, 300, 300)


def test_converting_rgb_to_hexadecimal():
    colors = rgb(100, 100, 100).hex
    assert colors.red == "64" and colors.green == "64" and colors.blue == "64"


def test_rgbf():
    colors = rgbf(1, 0, 1).float
    assert colors.red == 1.0 and colors.green == 0.0 and colors.blue == 1.0


def test_hex():
    colors = hex('646464').hex
    assert colors.red == "64" and colors.green == "64" and colors.blue == "64"


def test_hsv():
    colors = hsv(0, 1, 1).hsv
    assert colors.hue == 0 and colors.saturation == 1 and colors.value == 1


def test_hsv_value_error_s():
    with pytest.raises(ValueError):
        hsv(0, 2, 1)


def test_hsv_value_error_v():
    with pytest.raises(ValueError):
        hsv(0, 1, 2)


def test_hsv_hue_circle():
    assert hsv(2, 1, 1).hue == 0


def test_hex_value_error_len():
    with pytest.raises(ValueError):
        hex("#646464")


def test_hex_value_error_is_string():
    with pytest.raises(ValueError):
        hex(646464)


def test_hex_value_error_is_valid_hex():
    with pytest.raises(ValueError):
        hex("offfff")


def test_converting_hexadecimal_to_string():
    colors = str(rgb(100, 100, 100).hex)
    assert colors == "646464"


def test_hex_color_object():
    colors = hex('646464')
    assert colors.red == "64" and colors.green == "64" and colors.blue == "64"


def test_hex_get_color():
    colors = hex('646464').rgb
    assert colors.red == 100 and colors.green == 100 and colors.blue == 100


def test_convert_hex_to_hsv():
    colors = hex('646464').hsv
    assert colors.hue == 0 and colors.saturation == 0 and 0.3922 >= colors.value >= 0.3921


def test_converting_hex_object_to_list():
    colors = list(hex('646464').hsv)
    assert colors == [0.0, 0.0, 0.39215686274509803]


def test_hsv_color_object():
    colors = hsv(0, 1, 1)
    assert colors.hue == 0 and colors.saturation == 1 and colors.value == 1


def test_convert_hsv_to_rgb():
    colors = hsv(0, 1, 1).rgb
    assert colors.red == 255 and colors.green == 0 and colors.blue == 0


def test_coerce_object_to_string():
    colors = random().rgb
    strings = 'style="color: rgb({})"'.format(colors)
    assert strings == 'style="color: rgb({}, {}, {})"'.format(*list(colors))


def test_random_colors():
    colors1 = random()
    colors2 = random()
    assert colors1 != colors2
    assert len(str(random().hex)) == 6


def test_color_equality():
    assert rgb(100, 100, 100) == hex('646464')
    assert hex("ffffff") != rgb(255, 255, 0)


def test_rgb_float_color_object():
    colors = rgbf(1, 1, 1)
    assert colors.red == 1 and colors.green == 1 and colors.blue == 1


def test_RGBFloatColor_equality():
    assert rgbf(1, 1, 1) == rgb(255, 255, 255)
    assert rgbf(0.5, 0.5, 0.5) == rgb(128, 128, 128)
    assert rgbf(0.5, 0.5, 0.5).rgb == rgb(128, 128, 128)


def test_HexColor_float():
    assert rgbf(1, 0, 0) == hex("FF0000").float


def test_RGBColor_float():
    assert rgbf(1, 1, 1) == rgb(255, 255, 255).float


def test_HSVColor_float():
    assert rgbf(1, 0, 0) == hsv(0, 1, 1).float


def test_RGBFloatColor_value_error():
    with pytest.raises(ValueError):
        rgbf(300.0, 300.0, 300.0)
