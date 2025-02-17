
slope = 0.01702
intercept = -300.57852

def pixel_to_temperature(pixel):
    
    pixel.Value = (pixel.Value * slope) + intercept
    return pixel