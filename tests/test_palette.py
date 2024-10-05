from colors import RGBColor as rgb


def test_primary():
    import colors.primary
    assert colors.primary.red == rgb(255, 0, 0)


def test_rainbow():
    import colors.rainbow
    assert colors.rainbow.indigo == rgb(75, 0, 130)


def test_w3c():
    import colors.w3c
    assert colors.w3c.ghostwhite == rgb(248, 248, 255)



def test_wheel():
    from colors import ColorWheel
    wheel = ColorWheel()
    _iteration = 0
    for color in wheel:
        assert len(str(color.hex)) == 6
        _iteration += 1
        if _iteration >= 10:
            break
