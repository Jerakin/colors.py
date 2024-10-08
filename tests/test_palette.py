from colors import RGBColor


def test_primary():
    import colors.primary
    assert colors.primary.red == RGBColor(255, 0, 0)


def test_rainbow():
    import colors.rainbow
    assert colors.rainbow.indigo == RGBColor(75, 0, 130)


def test_w3c():
    import colors.w3c
    assert colors.w3c.ghostwhite == RGBColor(248, 248, 255)



def test_wheel():
    from colors import ColorWheel
    wheel = ColorWheel()
    _iteration = 0
    for color in wheel:
        assert len(str(color.hex)) == 6
        _iteration += 1
        if _iteration >= 10:
            break
