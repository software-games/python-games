#!/usr/bin/env python3

"""
Create SVG files for all 28 dominoes and save them in the `dominoes_svg` directory.

The SVG files are named `domino_i_j.svg` where `i` and `j` are the two numbers on the
domino. Images are 200x400 pixels with the pips (dots) being 5.5% of the domino width.

% python3 -m venv .venv
% source .venv/bin/activate
% pip install --upgrade pip
% pip install svgwrite  # https://pypi.org/project/svgwrite
% mkdir dominoes_svg
% python3 ./dominoes_svg.py
% open dominoes_svg/*
"""
import svgwrite
from svgwrite.drawing import Drawing


pip_offsets = (0.25, 0.5, 0.75)
pip_locations = (
    (()),
    ((1, 1),),
    ((0, 0), (2, 2)),
    ((0, 0), (1, 1), (2, 2)),
    ((0, 0), (0, 2), (2, 0), (2, 2)),
    ((0, 0), (0, 2), (1, 1), (2, 0), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (2, 2)),
)


def svg_die(svg: Drawing, die: int, pip_count: int, width_in_px: int = 200) -> None:
    """
    Draw a single die (half of a domino) on the SVG canvas.
    die 0 is the top of the half of the domino. die 1 for the bottom half of the domino.
    pip_count is the number of pips (dots) on the die from 0 to 6.
    """
    assert die in (0, 1)
    assert 0 <= pip_count <= 6
    pip_width = width_in_px * 0.055
    # Draw each of the pips...
    for x, y in pip_locations[pip_count]:
        center = (
            2 + pip_offsets[x] * width_in_px,
            2 + width_in_px * die + pip_offsets[y] * width_in_px,
        )
        # pip radius is 5.5% of the width so 11 pixels on a 200px wide domino
        svg.add(svg.circle(center=center, r=pip_width, fill="blue"))


def svg_domino(svg: Drawing, domino: tuple[int, int], width_in_px: int = 200) -> None:
    """
    Draw a domino on the SVG canvas by:
    1. Draw the bounding rect.
    2. Draw the dividing line.
    3. Call svg_die() to draw each half of the domino.
    """
    size = (width_in_px, width_in_px * 2)
    svg.add(svg.rect(insert=(2, 2), size=size, fill="white", stroke="blue"))
    pip_width = width_in_px * 0.055
    x1 = 2 + pip_offsets[0] * width_in_px - pip_width  # Left of the left-most pip
    x2 = 2 + pip_offsets[2] * width_in_px + pip_width  # Right of the right-most pip
    svg.add(svg.line(start=(x1, width_in_px), end=(x2, width_in_px), stroke="blue"))
    for die, pip_count in enumerate(domino):
        svg_die(svg, die, pip_count, width_in_px)


def dominoes_svg(width_in_px=200) -> None:
    """
    Create SVG files for all 28 dominoes and save them in the `dominoes_svg` directory.
    """
    x = 4
    y = 4
    for i in range(7):
        for j in range(i, 7):
            filename = f"dominoes_svg/domino_{i}_{j}.svg"
            size = (f"{width_in_px+x}px", f"{width_in_px*2+y}px")
            svg = svgwrite.Drawing(filename=filename, size=size)
            svg_domino(svg, (i, j), width_in_px)
            svg.save(pretty=True)


if __name__ == "__main__":
    dominoes_svg(width_in_px=200)
