class color_code:
    def print_rgb(r, g, b):
        color_code = f"\033[38;2;{r};{g};{b}m"
        return color_code

    green = print_rgb(141, 255, 84)
    yellow = print_rgb(255, 244, 84)
    red = print_rgb(255, 67, 69)
    purple = print_rgb(211, 107, 255)
    white = print_rgb(255, 255, 255)


