def scaling(value, in_min, in_max, out_min, out_max):
    if value is None or in_max == in_min:
        return None
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min