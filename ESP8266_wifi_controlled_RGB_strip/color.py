class Color():
    def __init__(self, red, green, blue):
        self.red = float(red)
        self.green = float(green)
        self.blue = float(blue)
        self.Saturation = 0.0
        self.Hue = 0.0
        self.Value = 0.0
        self.convHSV()
    
    def convHSV(self):
        # Normalize RGB values to [0, 1]
        nred, ngreen, nblue = self.red / 255.0, self.green / 255.0, self.blue / 255.0
        
        # Find the maximum and minimum RGB values
        cmax = max(nred, ngreen, nblue)
        cmin = min(nred, ngreen, nblue)
        diff = cmax - cmin
        
        # Calculate Hue
        if cmax == cmin:
            self.Hue = 0.0
        elif cmax == nred:
            self.Hue = (60.0 * ((ngreen - nblue) / diff) + 360.0) % 360.0
        elif cmax == ngreen:
            self.Hue = (60 * ((nblue - nred) / diff) + 120) % 360
        else:
            self.Hue = (60 * ((nred - ngreen) / diff) + 240) % 360
        
        # Calculate Saturation
        if cmax == 0:
            self.Saturation = 0
        else:
            self.Saturation = (diff / cmax) * 100
        
        # Calculate Value
        self.Value = cmax * 100


    def convRGB(self):
        # Normalize HSV values
        nhue = self.Hue % 360.0
        nsaturation = self.Saturation / 100.0
        nvalue = self.Value / 100.0
        
        # Calculate chroma
        chroma = nvalue * nsaturation
        
        # Calculate intermediate values
        hprime = nhue / 60.0
        x = chroma * (1 - abs((hprime % 2) - 1))
        m = nvalue - chroma
        
        # Calculate RGB values
        if 0 <= hprime < 1:
            nred, ngreen, nblue = chroma, x, 0
        elif 1 <= hprime < 2:
            nred, ngreen, nblue = x, chroma, 0
        elif 2 <= hprime < 3:
            nred, ngreen, nblue = 0, chroma, x
        elif 3 <= hprime < 4:
            nred, ngreen, nblue = 0, x, chroma
        elif 4 <= hprime < 5:
            nred, ngreen, nblue = x, 0, chroma
        else:
            nred, ngreen, nblue = chroma, 0, x
        
        # Adjust RGB values by adding m
        self.red = int((nred + m) * 255.0)
        self.green = int((ngreen + m) * 255.0)
        self.blue = int((nblue + m) * 255.0)

    def get_RGBcolor(self):
        return (self.red, self.green, self.blue)
    
    def get_HSVcolor(self):
        return (self.Hue, self.Saturation, self.Value)



