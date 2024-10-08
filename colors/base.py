"""
colors.base
===========
Convert colors between rgb, hsv, and hex, perform arithmetic, blend modes,
and generate random colors within boundaries.
"""
from __future__ import annotations
import colorsys
import random as random_
import logging
from numbers import Integral

__all__ = ("Color", "HSVColor", "RGBColor", "RGBFloatColor", "HexColor", "ColorWheel")

from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self, Union, TypeVar
    AnyColor = Union["RGBColor", "HSVColor", "RGBFloatColor", "HexColor"]
    T = TypeVar("T")
HEX_RANGE = frozenset("0123456789abcdef")

logger = logging.getLogger("colors.py")


class Color:
    """ Abstract base class for all color types. """
    _color: list

    @property
    def hex(self) -> HexColor:
        """ Hex is used the same way for all types. """
        return HexColor("{:02x}{:02x}{:02x}".format(*[int(x) for x in self.rgb]))

    @property
    def float(self) -> RGBFloatColor:
        raise NotImplementedError

    @property
    def rgb(self) -> RGBColor:
        raise NotImplementedError

    @property
    def hsv(self) -> HSVColor:
        raise NotImplementedError

    def multiply(self: T, other: AnyColor) -> T:
        """Blend mode operation."""
        color = [min(1, a * b) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def __mul__(self: T, other: AnyColor) -> RGBFloatColor:
        """Basic multiplication operation.

        Always returns a non-clamped RGBFloatColor.
        """
        color = [a * b for a, b in zip(self.float, other.float)]
        return RGBFloatColor(*color)

    def add(self: T, other: AnyColor) -> T:
        """Blend mode operation."""
        color = [min(1, a + b) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def __add__(self: T, other: AnyColor) -> RGBFloatColor:
        """Basic add operation.

        Always returns a non-clamped RGBFloatColor.
        """
        color = [a + b for a, b in zip(self.float, other.float)]
        return RGBFloatColor(*color)

    def divide(self: T, other: AnyColor) -> T:
        """Blend mode operation."""
        color = [max(0, min(1, 1 / (a / b))) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def __truediv__(self: T, other: AnyColor) -> RGBFloatColor:
        """Basic division operation.

        Always returns a non-clamped RGBFloatColor.
        """
        color = [a / b for a, b in zip(self.float, other.float)]
        return RGBFloatColor(*color)

    def subtract(self: T, other: AnyColor) -> T:
        """Blend mode operation."""
        color = [max(0, (b - a)) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def __sub__(self: T, other: AnyColor) -> RGBFloatColor:
        """Basic subtraction operation.

        Always returns a non-clamped RGBFloatColor.
        """
        color = [a - b for a, b in zip(self.float, other.float)]
        return RGBFloatColor(*color)

    def screen(self: T, other: AnyColor) -> T:
        """Wherever either colors are darker than white, the composite is brighter."""
        color = [1 - (((1 - a) * (1- b)) / 1.0) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def difference(self: T, other: AnyColor) -> T:
        color = [abs(a - b) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def overlay(self: T, other: AnyColor) -> T:
        """Blend mode. A combination of multiply and screen.

        Where the base layer is light, the top layer becomes lighter; where the base layer is dark,
         the top becomes darker; where the base layer is mid grey, the top is unaffected.
         An overlay with the same picture looks like an S-curve.
        """
        color = [(b> 0.5) * (1 - (1-2 * (b-0.5)) * (1 - a)) + (b <= 0.5) * ((2 * b) * a) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def invert(self: T) -> T:
        """Invert the current color."""
        return self.difference(RGBFloatColor(1, 1, 1))

    def color_dodge(self: T, other: AnyColor) -> T:
        """Blend mode. Brighter than the Screen blend mode. Results in an intense,
        contrasty color-typically results in saturated mid-tones and blown highlights."""
        color = [max(0, min(1, b / (1 - a))) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def linear_dodge(self: T, other: AnyColor) -> T:
        """Blend mode. Brighter than the Color Dodge blend mode, but less saturated and intense."""
        return self.add(other)

    def color_burn(self: T, other: AnyColor) -> T:
        """Blend mode. Darker than Multiply, with more highly saturated mid-tones and reduced highlights."""
        color = [max(0, min(1, 1 - (1 - b) / a)) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def linear_burn(self: T, other: AnyColor) -> T:
        """Blend mode. Darker than Multiply, but less saturated than Color Burn. """
        color = [max(0, min(1, a + b - 1)) for a, b in zip(self.float, other.float)]
        return self.__class__(RGBFloatColor(*color))

    def __eq__(self, other: AnyColor) -> bool:
        self_rgb = self.rgb
        other_rgb = other.rgb
        return self_rgb.red == other_rgb.red and self_rgb.green == other_rgb.green and self_rgb.blue == other_rgb.blue

    def __contains__(self, item: AnyColor) -> bool:
        return item in self._color

    def __ne__(self, other: AnyColor) -> bool:
        if isinstance(other, Color):
            return not self.__eq__(other)
        return NotImplemented

    def __iter__(self):
        """ Treat the color object as an iterable to iterate over color values"""
        return iter(self._color)

    def __len__(self) -> int:
        return len(self._color)

    def __str__(self) -> str:
        return ", ".join(map(str, self._color))


class HSVColor(Color):
    """ Hue Saturation Value """

    @overload
    def __init__(self, color: RGBColor): ...

    @overload
    def __init__(self, color: RGBFloatColor): ...

    @overload
    def __init__(self, color: HSVColor): ...

    @overload
    def __init__(self, color: HexColor): ...

    @overload
    def __init__(self, h: float, s: float, v: float): ...

    @overload
    def __init__(self): ...

    def __init__(self, h=0.0, s=0.0, v=0.0):
        if isinstance(h, Color):
            self._color = h.rgb._color
        else:
            if s > 1:
                raise ValueError("Saturation has to be less than 1")
            if v > 1:
                raise ValueError("Value has to be less than 1")

            # Hue can safely circle around 1
            if h >= 1:
                h -= int(h)

            self._color = [h, s, v]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(h={self.hue}, s={self.saturation}, v={self.value})"

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

    @overload
    def __init__(self, color: RGBColor): ...

    @overload
    def __init__(self, color: RGBFloatColor): ...

    @overload
    def __init__(self, color: HSVColor): ...

    @overload
    def __init__(self, color: HexColor,): ...

    @overload
    def __init__(self, r: int, g: int, b: int): ...

    @overload
    def __init__(self): ...

    def __init__(self, r = 0, g = 0, b = 0):
        if isinstance(r, Color):
            self._color = r.rgb._color
        else:
            self._color = [round(r), round(g), round(b)]

            for i, c in enumerate([r, g, b]):
                if not isinstance(c, Integral) and not c.is_integer():
                    logger.warning("%s = %s value is not an integer, it will be rounded to %s.", "rgb"[i], c, round(c))
                if not 0 <= c <= 255:
                    raise ValueError("Color values must be between 0 and 255 (is %s)", c)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(r={self.red}, g={self.green}, b={self.blue})"

    @property
    def rgb(self) -> RGBColor:
        return self

    @property
    def hsv(self) -> HSVColor:
        return self.float.hsv

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
    @overload
    def __init__(self, color: RGBColor): ...

    @overload
    def __init__(self, color: RGBFloatColor): ...

    @overload
    def __init__(self, color: HSVColor): ...

    @overload
    def __init__(self, color: HexColor): ...

    @overload
    def __init__(self, r: float, g: float, b: float): ...

    @overload
    def __init__(self): ...

    def __init__(self, r = 0.0, g = 0.0, b = 0.0):
        if isinstance(r, Color):
            self._color = r.float._color
        else:
            self._color =  [r, g, b]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(r={self.red}, g={self.green}, b={self.blue})"

    @property
    def hsv(self) -> HSVColor:
        color = colorsys.rgb_to_hsv(*map(lambda c_: c_, self._color))
        for c in color:
            if not 0 <= c <= 1:
                logger.info("Color value not in 0-1 range, clamping will occur.")

        return HSVColor(*[min(1.0, max(0.0, c)) for c in color])

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
    @overload
    def __init__(self, color: RGBColor): ...

    @overload
    def __init__(self, color: RGBFloatColor): ...

    @overload
    def __init__(self, color: HSVColor): ...

    @overload
    def __init__(self, color: HexColor): ...

    @overload
    def __init__(self, hex_string): ...

    @overload
    def __init__(self): ...

    def __init__(self, hex_string="000000"):
        if isinstance(hex_string, Color):
            self._color = hex_string.hex._color
        else:
            if not isinstance(hex_string, str):
                raise ValueError("Hex must be string")

            if len(hex_string) != 6:
                raise ValueError("Hex color must be 6 digits")

            _hex = hex_string.lower()
            if not set(_hex).issubset(HEX_RANGE):
                raise ValueError("Not a valid hex number")

            self._color = [_hex[:2], _hex[2:4], _hex[4:6]]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{"".join(self._color)}")'

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
        return "{}{}{}".format(*self._color)


class ColorWheel:
    """Iterate random colors distributed relatively evenly around the color wheel."""
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
