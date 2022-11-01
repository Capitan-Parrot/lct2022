def check_is_analog(analog, main_flat):
    return all(analog[param] == main_flat[param] for param in main_flat)

