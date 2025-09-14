# Copilot / AI agent instructions for the Truchet repo

Purpose: help an AI agent be immediately productive editing or extending this small Jupyter/PyCairo project that generates multi-scale Truchet tiles and images.

- Quick overview
  - This repo implements multiscale Truchet tile generation and rendering using PyCairo and NumPy. Core pieces:
    - `tiler.py` — orchestrates tiling, multiscale splitting, and image-driven tiling (`multiscale_truchet`, `image_truchet`, `show_tiles`).
    - `n6.py` — defines many concrete `Tile` subclasses (geometry + draw routines) and collects them into lists like `n6_tiles`, `n6_circles`, `n6_lattice`, etc.
    - `drawing.py` — thin Cairo context helpers (`cairo_context`, context managers, compass constants) used across the codebase.
    - `helpers.py`, `image_helpers.py` — small utility helpers (color conversion, slicing, downsampling) that `tiler.py` relies on.
    - `main.py` — trivial CLI entrypoint (prints a message).

- Data flow & architecture
  - The system composes tile classes (in `n6.py`) which subclass `TileBase` (in `tiler.py`). A tile instance's `draw_tile`/`draw` methods build Cairo paths into the provided `ctx`.
  - `multiscale_truchet` (in `tiler.py`) drives layout: it creates a `cairo_context`, iterates a grid of tiles at base size, then repeatedly optionally splits boxes to smaller tiles; `tile_chooser` decides which tile to draw.
  - Image-driven flows: `image_truchet` and `image_truchet4` sample a grayscale image and map average luminance to tile choices using `tile_value`/`tile_value4`.

- Project-specific conventions
  - Tiles are collected into lists with the `@collect(...)` decorator (see `n6.py`); these lists (e.g., `n6_tiles`, `n6_circles`) are the canonical tile collections used by notebooks.
  - Tile classes define a nested `G` class for precomputed geometry values (named w1c, w3c, w12, etc.). Use these names when adding new geometry pieces.
  - `stroke` decorator marks drawing primitives as strokes. `draw` methods may call `self.<primitive>(ctx, g)`; primitives expect `ctx` to be a Cairo-like context proxy from `drawing.py`.
  - Colors: use `helpers.color(...)` to get (r,g,b,a) tuples. Many callers pass `bg`/`fg` as floats or hex strings and `helpers.make_bgfg` returns dicts for `bg`/`fg`.

- Dependencies & environment
  - See `requirements.txt` / `pyproject.toml`. Key runtime dependencies: Python >= 3.12, `pycairo`, `numpy`, `pillow`, `shapely`, `jupyterlab`, `ipywidgets`.
  - Notes: `pycairo` may need system packages on Linux/macOS (cairo developer headers). README mentions `brew install cmake pkgconf cairo` for macOS.

- Developer workflows (how to run / test quickly)
  - Interactive exploration: open the included Jupyter notebooks (`Truchet.ipynb`, `N6.ipynb`, `N6 copy.ipynb`) and run cells that call `multiscale_truchet(...)` or `show_tiles(...)`.
  - Generate an SVG or PNG directly in Python: call `multiscale_truchet(..., format='png', output='~/out.png')` or use `show_tiles(...)` which returns a Cairo context object that Jupyter can render.
  - Quick lint/build: this is a small library — no build step. Use `python -m pip install -r requirements.txt` to install dependencies. Tests: none present.

- Patterns and examples to follow (concrete)
  - Adding a new tile: create a subclass of `TileBase` (or `Tile` pattern from `n6.py`), implement `init_tile(self, ctx, g, base_color=None)` if you need background shaping, and `draw(self, ctx, g)` to paint. Use `@collect(...)` to add to tile lists. Example: `Slash21` in `n6.py`.
  - Using `multiscale_truchet`: pass either `tiles=[tile_instances]` or a `tile_chooser(ux,uy,uw,ilayer)` callable. For image-based tiling prefer `image_truchet(...)` which wires tile value mapping automatically.
  - Inspect tile brightness: use `tiler.tile_value(tile)` or `tile_value4(tile)` to measure gray-level mapping used by `image_truchet`.

- Code conventions & gotchas
  - Many APIs use normalized coordinates (ux/uy/us) in `[0, 1]` relative to overall width/height — be careful when writing `tile_chooser` or `should_split` functions.
  - Cairo context proxies in `drawing.py` implement convenience context managers: `save_restore`, `rotated`, `flip_lr` — prefer these over manual save/restore.
  - `TileBase.draw_tile` expects `wh` to be the tile size in device pixels; nested `G` uses that to compute constants — avoid hardcoding pixel values inside tile code.
  - `multiscale_truchet` flips `bgfg` between layers (`bgfg = bgfg[::-1]`) — be aware of foreground/background alternation across layers.

- Files you will likely edit
  - Add tiles: `n6.py` (or new file under same layout)
  - Core graphing or tiling behavior: `tiler.py`
  - Utility helpers: `helpers.py`, `image_helpers.py`, `drawing.py`
  - Notebooks are the primary demo surface: `*.ipynb` (e.g., `N6.ipynb`, `Truchet.ipynb`)

- When uncertain, inspect these examples in the repo
  - `n6.py` for many tile examples and `@collect` usage
  - `tiler.py` for `multiscale_truchet`, `image_truchet`, `show_tiles`
  - `drawing.py` for how Cairo contexts are created and how to render to Jupyter/files

If anything above is unclear or you want more examples (e.g., exact `tile_chooser` patterns or how to write PNG output), tell me what to expand and I'll iterate.