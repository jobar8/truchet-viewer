"""
truchet-viewer - A Python library for generating multi-scale Truchet tile patterns and images using PyCairo.
"""

from .tiler import (
    TileBase,
    multiscale_truchet,
    image_truchet,
    image_truchet4,
    show_tiles,
    tile_value,
    tile_value4,
)
from .n6 import (
    n6_tiles,
    n6_circles,
    n6_lattice,
)

__all__ = [
    'TileBase',
    'multiscale_truchet',
    'image_truchet',
    'image_truchet4',
    'show_tiles',
    'tile_value',
    'tile_value4',
    'n6_tiles',
    'n6_circles',
    'n6_lattice',
]