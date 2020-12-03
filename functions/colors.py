from collections import defaultdict
import math
import webcolors


# Objects included in this file:
# # color_dict
# # color_list

# Functions included in this file:
# # generate_color_dict
# # hex_to_rgba
# # update rgba_opacity


color_dict = {'black': '#000000',
              'blue': '#1f77b4',
              'brown': '#8c564b',
              'colorless': '#7f7f7f',
              'green': '#2ca02c',
              'orange': '#ff7f0e',
              'pink': '#e377c2',
              'purple': '#9467bd',
              'red': '#d62728',
              'white': '#7f7f7f',
              'yellow': '#FFFF00'}


color_list = list(color_dict.values())


def generate_color_dict(labels: list, colors: list):
    """Matches labels with colors
    If there are more labels than colors, repeat and cycle through colors
    """
    color_dict = defaultdict(dict)
    repetitions = math.ceil(len(labels) / len(colors))
    for label in enumerate(labels):
        color_dict[label[1]] = (color_list * mult)[label[0]]
    return {**color_dict}


def hex_to_rgba(hex_color, opacity=1):
    """Example usage:
    Input: #2ca02c
    Output: 'rgba(44, 160, 44, 0)'
    """
    int_rgb = webcolors.hex_to_rgb(hex_color)
    return f"rgba({int_rgb.red}, {int_rgb.green}, {int_rgb.blue}, {opacity})"


def update_rgba_opacity(rgba, new_opacity=0.5):
    """Example usage:
    Input: 'rgba(44, 160, 44, 1)'
    Output: 'rgba(44, 160, 44, 0.5)'
    """
    rgba_list = rgba[4:].strip('()').split(', ')
    rgba_list[-1] = str(new_opacity)
    return 'rgba('+', '.join(rgba_list)+')'