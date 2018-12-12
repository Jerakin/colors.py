import unittest
from colors import rgb, hsv, hex, random


class TestColors(unittest.TestCase):
    def test_rgb_color_object(self):
        colors = rgb(100, 100, 100)
        self.assertTrue(colors.red == 100 and colors.green == 100 and colors.blue == 100, "RGB Color object")

    def test_converting_rgb_to_hexadecimal(self):
        colors = rgb(100, 100, 100).hex
        self.assertTrue(colors.red == "64" and colors.green == "64" and colors.blue == "64", "Converting rgb to hex")

    def test_converting_hexadecimal_to_string(self):
        colors = str(rgb(100, 100, 100).hex)
        self.assertTrue(colors == "646464", "Converting hex to string")

    def test_hex_color_object(self):
        colors = hex('646464')
        self.assertTrue(colors.red == "64" and colors.green == "64" and colors.blue == "64", "hex Color object")

    def test_hex_get_color(self):
        colors = hex('646464').rgb
        self.assertTrue(colors.red == 100 and colors.green == 100 and colors.blue == 100, "Get rgb from hex")

    def test_convert_hex_to_hsv(self):
        colors = hex('646464').hsv
        self.assertTrue(
            colors.hue == 0 and colors.saturation == 0 and 0.3922 >= colors.value >= 0.3921, "Converting hex to hsv")

    def test_converting_hex_object_to_list(self):
        colors = list(hex('646464').hsv)
        self.assertTrue(colors == [0.0, 0.0, 0.39215686274509803], "Converting hex to hsv")

    def test_hsv_color_object(self):
        colors = hsv(0, 1, 1)
        self.assertTrue(colors.hue == 0 and colors.saturation == 1 and colors.value == 1, "HSV Color object")

    def test_convert_hsv_to_rgb(self):
        colors = hsv(0, 1, 1).rgb
        self.assertTrue(colors.red == 255 and colors.green == 0 and colors.blue == 0, "RGB Color object")

    def test_coerce_object_to_string(self):
        colors = random().rgb
        strings = 'style="color: rgb({})"'.format(colors)
        self.assertTrue(strings == 'style="color: rgb({}, {}, {})"'.format(*list(colors)), "RGB Color object")

    def test_random_colors(self):
        colors1 = random()
        colors2 = random()
        self.assertFalse(colors1 == colors2, "Duplicated random colors")

    def test_color_equality(self):
        self.assertTrue(rgb(100, 100, 100) == hex('646464'), "Color's are not equal")
        self.assertTrue(hsv(0, 1, 1) == rgb(255, 0, 0), "Color's are not equal")


class TestColorsArithmetic(unittest.TestCase):
    def test_color_multiplication_operator(self):
        self.assertTrue(hex('ff9999') * hex('cccccc') == rgb(204.0, 122.4, 122.4), "Multiply color values with operator")

    def test_color_multiplication_function(self):
        self.assertTrue(rgb(100, 100, 100).multiply(hsv(0, 1, 1)).hex == hex("640000"), "Multiply color values with function")

    def test_color_addition_operator(self):
        self.assertTrue(hex('ff9999') + rgb(10, 10, 10) == rgb(255, 163, 163), "Adding color values with operator")

    def test_color_addition_function(self):
        self.assertTrue(hex('aaffcc').add(rgb(10, 10, 10)) == rgb(180, 255, 214), "Adding color values with function")

    def test_color_subtracting_operator(self):
        self.assertTrue(hex('ff9999') - rgb(10, 10, 10) == rgb(245, 143, 143), "Subtracting color values with operator")

    def test_color_subtracting_function(self):
        self.assertTrue(hex('aaffcc').subtract(rgb(10, 10, 10)) == rgb(160, 245, 194), "Subtracting color values with function")

    def test_color_dividing_operator(self):
        self.assertTrue(hex('ff9999') / rgb(10, 10, 10) == rgb(25.5, 15.3, 15.3), "Dividing color values with operator")

    def test_color_dividing_function(self):
        self.assertTrue(hex('aaffcc').divide(rgb(10, 10, 10)) == rgb(17, 25.5, 20.4), "Dividing color values with function")

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            color_hex = hex('00ffff')
            color_rgb = rgb(100, 100, 100)
            color_rgb / color_hex


class TestColorsBlendModes(unittest.TestCase):
    def test_screen(self):
        self.assertTrue(hex('ff9999').screen(rgb(10, 10, 10)).hex == hex("ff9d9d"), "Screen values")

    def test_difference(self):
        self.assertTrue(hex('ff9999').difference(rgb(10, 10, 10)).hex == hex("f58f8f"), "Difference values")

    def test_overlay(self):
        self.assertTrue(hex('ff9999').overlay(rgb(10, 10, 10)).hex == hex("ff9b9b"), "Overlay values")

    def test_invert(self):
        self.assertTrue(hex('000000').invert() == rgb(255, 255, 255), "Inverting values")
