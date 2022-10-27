class ColorString(str):
    def __new__(cls, value, *args, **kwargs):
        return super(ColorString, cls).__new__(cls, value)

    def __init__(self, values, fill: str = " "):
        self.fill = fill

    def __mul__(self, value):
        return self + self.fill * value
