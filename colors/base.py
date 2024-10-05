"""
colors.base
===========
Convert colors between rgb, hsv, and hex, perform arithmetic, blend modes,
and generate random colors within boundaries.
"""
from __future__ import annotations
import colorsys
import random as random_

__all__ = ('Color', 'HSVColor', 'RGBColor', "RGBFloatColor", 'HexColor', 'ColorWheel',
           'rgb', 'hsv', 'hex', 'random')

HEX_RANGE = frozenset('0123456789abcdef')


class Color:
    """ Abstract base class for all color types. """
    _color: list

    @property
    def hex(self) -> HexColor:
        """ Hex is used the same way for all types. """
        return HexColor('{:02x}{:02x}{:02x}'.format(*[int(x) for x in self.rgb]))

    @property
    def rgb(self):
        raise NotImplementedError

    @property
    def hsv(self):
        raise NotImplementedError

    def multiply(self, other: Color) -> RGBColor:
        self_rgb = self.rgb
        other_rgb = other.rgb
        return RGBColor(
            self_rgb.red * other_rgb.red / 255.0,
            self_rgb.green * other_rgb.green / 255.0,
            self_rgb.blue * other_rgb.blue / 255.0
        )

    __mul__ = multiply

    def add(self, other: Color) -> RGBColor:
        self_rgb = self.rgb
        other_rgb = other.rgb
        return RGBColor(
            min(255, self_rgb.red + other_rgb.red),
            min(255, self_rgb.green + other_rgb.green),
            min(255, self_rgb.blue + other_rgb.blue),
        )

    __add__ = add

    def divide(self, other: Color) -> RGBColor:
        self_rgb = self.rgb
        other_rgb = other.rgb
        if 0 in other_rgb:
            raise ZeroDivisionError
        return RGBColor(
            self_rgb.red / float(other_rgb.red),
            self_rgb.green / float(other_rgb.green),
            self_rgb.blue / float(other_rgb.blue),
        )

    __truediv__ = divide

    def subtract(self, other: Color) -> RGBColor:
        self_rgb = self.rgb
        other_rgb = other.rgb
        return RGBColor(
            max(0, (self_rgb.red - other_rgb.red)),
            max(0, (self_rgb.green - other_rgb.green)),
            max(0, (self_rgb.blue - other_rgb.blue)),
        )

    __sub__ = subtract

    def screen(self, other: Color) -> RGBColor:
        self_rgb = self.rgb
        other_rgb = other.rgb
        return RGBColor(
            255 - (((255 - self_rgb.red) * (255 - other_rgb.red)) / 255.0),
            255 - (((255 - self_rgb.green) * (255 - other_rgb.green)) / 255.0),
            255 - (((255 - self_rgb.blue) * (255 - other_rgb.blue)) / 255.0),
        )

    def difference(self, other: Color) -> RGBColor:
        self_rgb = self.rgb
        other_rgb = other.rgb
        return RGBColor(
            abs(self_rgb.red - other_rgb.red),
            abs(self_rgb.green - other_rgb.green),
            abs(self_rgb.blue - other_rgb.blue),
        )

    def overlay(self, other: Color) -> RGBColor:
        return self.screen(self.multiply(other))

    def invert(self):
        return self.difference(RGBColor(255, 255, 255))

    def __eq__(self, other: Color) -> bool:
        self_rgb = self.rgb
        other_rgb = other.rgb
        return self_rgb.red == other_rgb.red and self_rgb.green == other_rgb.green and self_rgb.blue == other_rgb.blue

    def __contains__(self, item: Color) -> bool:
        return item in self._color

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __iter__(self):
        """ Treat the color object as an iterable to iterate over color values"""
        return iter(self._color)

    def __len__(self) -> int:
        return len(self._color)

    def __str__(self) -> str:
        return ', '.join(map(str, self._color))


class HSVColor(Color):
    """ Hue Saturation Value """

    def __init__(self, h=0.0, s=0.0, v=0.0):
        if s > 1:
            raise ValueError('Saturation has to be less than 1')
        if v > 1:
            raise ValueError('Value has to be less than 1')

        # Hue can safely circle around 1
        if h >= 1:
            h -= int(h)

        self._color = [h, s, v]

    def __repr__(self) -> str:
        return f"HSVColor(h={self.hue}, s={self.saturation}, v={self.value})"

    @property
    def hue(self) -> float:
        return self._color[0]

    @hue.setter
    def hue(self, value: float):
        self._color[0] = value

    @property
    def saturation(self) -> float:
        return self._color[1]

    @saturation.setter
    def saturation(self, value: float):
        self._color[1] = value

    @property
    def value(self) -> float:
        return self._color[2]

    @value.setter
    def value(self, value: float):
        self._color[2] = value

    @property
    def rgb(self) -> RGBColor:
        return RGBColor(*map(lambda c: c * 255, colorsys.hsv_to_rgb(*self._color)))

    @property
    def hsv(self):
        return self

    @property
    def float(self) -> RGBFloatColor:
        return RGBFloatColor(*map(lambda c: c, colorsys.hsv_to_rgb(*self._color)))


class RGBColor(Color):
    """ Red Green Blue colors represented in a 0 - 255 range"""

    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self._color = [round(r), round(g), round(b)]
        for c in self._color:
            if 0 > c or c > 255:
                raise ValueError('Color values must be between 0 and 255')

    def __repr__(self) -> str:
        return f"RGBColor(r={self.red}, g={self.green}, b={self.blue})"

    @property
    def rgb(self) -> RGBColor:
        return self

    @property
    def hsv(self) -> HSVColor:
        return HSVColor(*colorsys.rgb_to_hsv(*map(lambda c: c / 255, self._color)))

    @property
    def float(self) -> RGBFloatColor:
        return RGBFloatColor(*map(lambda c: c / 255, self._color))

    @property
    def red(self) -> int:
        return self._color[0]

    @red.setter
    def red(self, value: int):
        self._color[0] = value

    @property
    def green(self) -> int:
        return self._color[1]

    @green.setter
    def green(self, value: int):
        self._color[1] = value

    @property
    def blue(self) -> int:
        return self._color[2]

    @blue.setter
    def blue(self, value: int):
        self._color[2] = value


class RGBFloatColor(Color):
    """ Red Green Blue colors represented in a 0-1 range """
    def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 0.0):
        self._color =  [r, g, b]
        for c in self._color:
            if 0 > c or c > 1:
                raise ValueError('Color values must be between 0 and 1')

    def __repr__(self) -> str:
        return f"RGBFloatColor(r={self.red}, g={self.green}, b={self.blue})"

    @property
    def hsv(self) -> HSVColor:
        return HSVColor(*colorsys.rgb_to_hsv(*map(lambda c: c, self._color)))

    @property
    def rgb(self) -> RGBColor:
        return self.hsv.rgb

    @property
    def float(self) -> RGBFloatColor:
        return self

    @property
    def red(self) -> float:
        return self._color[0]

    @red.setter
    def red(self, value: float):
        self._color[0] = value

    @property
    def green(self) -> float:
        return self._color[1]

    @green.setter
    def green(self, value: float):
        self._color[1] = value

    @property
    def blue(self) -> float:
        return self._color[2]

    @blue.setter
    def blue(self, value: float):
        self._color[2] = value


class HexColor(RGBColor):
    """ Typical 6 digit hexadecimal colors.

    Warning: accuracy is lost when converting a color to hex
    """
    def __init__(self, _hex='000000'):
        if not type(_hex) == str:
            raise ValueError("Hex must be string")

        if len(_hex) != 6:
            raise ValueError('Hex color must be 6 digits')

        _hex = _hex.lower()
        if not set(_hex).issubset(HEX_RANGE):
            raise ValueError('Not a valid hex number')

        self._color = _hex[:2], _hex[2:4], _hex[4:6]

    @property
    def rgb(self) -> RGBColor:
        return RGBColor(*[int(c, 16) for c in self._color])

    @property
    def hsv(self) -> HSVColor:
        return self.rgb.hsv

    @property
    def hex(self) -> HexColor:
        return self

    @property
    def float(self) -> RGBFloatColor:
        return RGBFloatColor(*[int(c, 16)/255.0 for c in self._color])

    def __str__(self) -> str:
        return '{}{}{}'.format(*self._color)


class ColorWheel:
    """ Iterate random colors distributed relatively evenly around the color wheel."""
    def __init__(self, start: float = 0):
        # A 1.1 shift is identical to 0.1
        if start >= 1:
            start -= 1
        self._phase = start

    def __iter__(self) -> ColorWheel:
        return self

    def __next__(self) -> HSVColor:
        shift = (random_.random() * 0.1) + 0.1
        self._phase += shift
        if self._phase >= 1:
            self._phase -= 1
        return HSVColor(self._phase, 1, 0.8)


def random() -> HSVColor:  # This name might be a bad idea?
    """ Generate a random color."""
    return HSVColor(random_.random(), random_.random(), random_.random())


# Simple aliases
rgb = RGBColor  # rgb(100, 100, 100), or rgb(r=100, g=100, b=100)
rgbf = RGBFloatColor  # rgb(100, 100, 100), or rgb(r=100, g=100, b=100)
hsv = HSVColor  # hsv(0.5, 1, 1), or hsv(h=0.5, s=1, v=1)
hex = HexColor  # hex('bada55')
