
from functools import reduce

colors = {
    "GREY": (122, 119, 111),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "DARK-RED": (168, 50, 50),
    "LIGHT-RED": (168, 74, 50),
    "YELLOW": (242, 245, 66)
}


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900


def flatten(ls):
    def flatten_element(e):
        if isinstance(e, list):
            if not e:
                return []
            elif isinstance(e[0], list):
                return flatten(e)
            else:
                return e
        else:
            return [e]

    return list(reduce(lambda others, e: others + flatten_element(e), ls, []))