class Color():
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.Saturation = 0
        self.Hue = 0
        self.Value = 0
        self.convHSV()
    
    def convHSV(self):
        self.Value = max(self.red, self.green, self.blue)
        min_value = min(self.red, self.green, self.blue)
        if self.Value != 0:
            Saturation = (self.Value - min_value) / self.Value
        Hue = 0 if self.Value == self.red == self.green == self.blue  else \
            60 * (self.green - self.blue) / (self.Value - min_value) if self.Value == self.red != self.green != self.blue else \
            60 * (self.blue - self.red) / (self.Value - min_value) + 120 if self.Value == self.green != self.red != self.blue else \
            120 if self.green == 255 and self.red == 0 and self.blue == 0 else \
            60 * (self.red - self.green) / (self.Value - min_value) + 240 if self.Value == self.blue != self.red != self.green else \
            240 if  self.blue == 255 and self.red == 0 and self.green == 0  else \
            60 * ((self.green - self.red) / (self.Value - min_value) + 2) if self.Value != self.red != self.green != self.blue else 0

    def convRGB(self):
        self.Value = self.Value / 255
        Chroma = self.Value * self.Saturation
        X = Chroma * (1 - abs((self.Hue / 60) % 2 - 1))
        m = self.Value - Chroma
        (self.red, self.green, self.blue) = (Chroma, X, 0) if 0 <= self.Hue < 60 else \
            (X, Chroma, 0) if 60 <= self.Hue < 120 else \
            (0, Chroma, X) if 120 <= self.Hue < 180 else \
            (0, X, Chroma) if 180 <= self.Hue < 240 else \
            (X, 0, Chroma) if 240 <= self.Hue < 300 else \
            (Chroma, 0, X)
        (self.red, self.green, self.blue) = ((self.red + m) * 255, (self.green + m) * 255, (self.blue + m) * 255)