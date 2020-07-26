def color(r, g, b):
    return bytes([b, g, r])

def decimalToRgb(colors_array):
    return [round(i*255) for i in colors_array]
