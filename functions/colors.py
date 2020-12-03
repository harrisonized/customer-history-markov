from collections import defaultdict
import math
import webcolors


# Objects included in this file:
# # color_name_to_hex
# # default_colors

# Functions included in this file:
# # generate_label_colors
# # hex_to_rgba
# # update rgba_opacity


color_name_to_hex = {'blue': '#1f77b4',
                     'orange': '#ff7f0e',
                     'green': '#2ca02c',
                     'red': '#d62728',
                     'purple': '#9467bd',
                     'brown': '#8c564b',
                     'pink': '#e377c2',
                     'colorless': '#7f7f7f',
                     'yellow': '#FFFF00',
                     'white': '#7f7f7f',
                     'black': '#000000'}

default_colors = list(color_name_to_hex.values())


def generate_label_colors(labels: list, colors: list):
    """Matches labels with colors
    If there are more labels than colors, repeat and cycle through colors
    """
    label_colors = defaultdict(dict)
    num_repeats = math.ceil(len(labels) / len(colors))
    for label in enumerate(labels):
        label_colors[label[1]] = (colors * num_repeats)[label[0]]
    return {**label_colors}


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
