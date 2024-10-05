## Changes from mattrobenolt/colors.py
> [!IMPORTANT]
> Version 1.0.0 changes supported version too >=3.7

_These changes are still not in the upstream repo_
* Test suite
* Fully type hinted
* [#9](https://github.com/mattrobenolt/colors.py/pull/9) Support for Python 3
* [#10](https://github.com/mattrobenolt/colors.py/pull/10) RGBColor is strictly 24bit (rounds the rgb input)
* Added RGBFloatColor that represent colors in a 0.0 - 1.0 range (however, it doesn't enforce it to be clamped)
* Separation between arithmetics and blend modes. Operators returns non-clamped RGBFloatColor.
Blend mode returns the same color type as the caller.

# colors.py
Convert colors between rgb, hsv, and hex, perform arithmetic, blend modes, and generate random colors within boundaries
## Installation
Either grab the version explicit or use master.  
```$ pip install https://github.com/Jerakin/colors.py/archive/master.zip```

Latest release is _"[0.3.4](https://github.com/Jerakin/colors.py/releases/tag/0.3.4) added alias for RGBFloat `rgbf`"_  
* `pip install https://github.com/Jerakin/colors.py/releases/download/0.3.4/colors.py-0.3.4-py2.py3-none-any.whl`

## Basic Uses
```python
>>> import colors
```
Or create an alias.
```python
>>> from colors import RGBColor as rgb
```

### Create an RGB color object
```python
>>> colors.RGBColor(100, 100, 100)
RGBColor(r=100, g=100, b=100)
```
### Convert it to hexadecimal
```python
colors.HexColor(100, 100, 100).hex
HexColor("646464")
```
### Coerce the hexadecimal to a normal string
```python
>>> str(colors.RGBColor(100, 100, 100).hex)
646464
```

### Create a Hexadecimal color object
```python
>>> colors.HexColor('646464')
HexColor("646464")
```

### Extract the red/green/blue value from a hexadecimal
```python
>>> colors.HexColor('646464').rgb.red
100
```

### Convert a hexadecimal to HSV
```python
>>> colors.HexColor('646464').hsv
HSVColor(h=0.0, s=0.0, v=0.392156862745)
```

### Coerce hsv/rgb values to a list/tuple of values
```python
>>> list(colors.HexColor('646464').hsv)
[0.0, 0.0, 0.39215686274509803]
```

### Create an HSV color object
```python
>>> colors.HSVColor(0, 1, 1)
HSVColor(h=0, s=1, v=1)
```

### Convert it to RGB
```python
>>> colors.HSVColor(0, 1, 1).rgb
RGBColor(r=255, g=0, b=0)
```

### Create an float RGB color object
```python
>>> colors.RGBFloatColor(0.5, 0.5, 0.5)
RGBFloatColor(r=0.5, g=0.5, b=0.5)
```

### Convert it to RGB
```python
>>> colors.RGBFloatColor(0.5, 0.5, 0.5).rgb
RGBColor(r=128, g=128, b=128)
```
### Coerce a hexadecimal color to a string with formatting
```python
>>> f'#{colors.RGBFloatColor(0.5, 0.5, 0.5).hex}'
'#2f2336'
```
### Coerce RGB/HSV objects to a string for formatting
```python
>>> f'style="color: rgb({colors.RGBFloatColor(0.5, 0.5, 0.5).rgb})"'
'style="color: rgb(80, 124, 71)"'
```
### Compare color equality
```python
>>> colors.RGBColor(100, 100, 100) == colors.HexColor('646464')
True

>>> colors.hsv(0, 1, 1) == colors.RGBColor(255, 0, 0)
True
```
## Arithmetic
> [!IMPORTANT]
> All operators (`+`, `-`, `/`, `*`) returns non-clamped RGBFloatColor.

### Multiply
```python
>>> colors.HexColor('ff9999') * colors.HexColor('cccccc')
RGBFloatColor(r=0.8, g=0.48, b=0.48)
```

### Add
```python
>>> colors.HexColor('ff9999') + colors.RGBColor(10, 10, 10)
RGBFloatColor(r=1.0392156862745099, g=0.6392156862745098, b=0.6392156862745098)
```

### Subtract
```python
>>> colors.HexColor('ff9999') - colors.RGBColor(10, 10, 10)
RGBFloatColor(r=0.9607843137254902, g=0.5607843137254902, b=0.5607843137254902)

```

### Divide
```python
>>> colors.HexColor('ff9999') / colors.RGBColor(10, 10, 10)
RGBFloatColor(r=25.5, g=15.299999999999999, b=15.299999999999999)
```

## Blend Modes
> [!NOTE]
> The type of the Color returned is the same type as the caller.

### Screen
```python
>>> colors.HexColor('ff9999').screen(colors.RGBColor(10, 10, 10))
HexColor("ff9d9d")
```

### Difference
```python
>>> colors.HexColor('ff9999').difference(colors.RGBColor(10, 10, 10))
HexColor("f58f8f")
```
### Overlay
```python
>>> colors.HexColor('ff9999').overlay(colors.RGBColor(10, 10, 10))
HexColor("ff9b9b")
```

### Invert
```python
>>> colors.HexColor('000000').invert()
HexColor("ffffff")
```

### Color Dodge
```python
>>> RGBColor(195, 49, 171).color_dodge(RGBColor(14, 19, 14))
RGBColor(59, 24, 42)
```

### Linear Dodge
```python
>>> RGBColor(195, 49, 171).linear_dodge(RGBColor(14, 19, 14))
RGBColor(209, 68, 185)
```

### Color Burn
```python
>>> RGBColor(195, 49, 171).color_burn(RGBColor(107, 194, 145))
RGBColor(61, 0, 91)
```

### Linear Burn
```python
>>>  RGBColor(195, 49, 171).linear_burn(RGBColor(107, 194, 145))
RGBColor(47, 0, 61)
```

## Color palettes
`colors.py` current ships with three color palettes full of constants. See source for all available colors.
### `colors.primary`
```python
>>> import colors.primary
>>> colors.primary.red
RGBColor(r=255, g=0, b=0)
```
### `colors.rainbow`
```python
>>> import colors.rainbow
>>> colors.rainbow.indigo
RGBColor(r=75, g=0, b=130)
```

### `colors.w3c`
```python
>>> import colors.w3c
>>> colors.w3c.ghostwhite
<RGBColor red: 248, green: 248, blue: 255>
```

## The Color Wheel!
The color wheel allows you to randomly choose colors while keeping the colors relatively evenly distributed. Think generating random colors without pooling in one hue, e.g., not 50 green, and 1 red.
```python
>>> from colors import ColorWheel
>>> wheel = ColorWheel()
```
### Iterate the wheel to get the next value
ColorWheel is an iterable, but be careful if using inside any type of loop. It will iterate forever until you interject.
```python
>>> wheel.next()
<HSVColor hue: 0.177410230076, saturation: 1, value: 0.8>

>>> wheel.next()
<HSVColor hue: 0.278803914372, saturation: 1, value: 0.8>

>>> for color in wheel:
...   print(color.hex)
00cca4
002ecc
# Forever and ever and ever and ever
```
