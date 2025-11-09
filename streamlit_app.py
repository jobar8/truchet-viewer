import streamlit as st
import re


from truchet_viewer import multiscale_truchet
from truchet_viewer.n6 import n6_tiles, n6_circles, n6_connected, n6_filled, n6_lattice, n6_strokes, n6_weird
from truchet_viewer.carlson import carlson_tiles

# Set page config
st.set_page_config(page_title='Truchet Pattern Generator', layout='wide')

# Title
st.title('Truchet Pattern Generator')

# Create dictionary mapping tile set names to actual tile lists
TILE_SETS = {
    'All tiles': n6_tiles,
    'Circles': n6_circles,
    'Connected': n6_connected,
    'Filled': n6_filled,
    'Lattice': n6_lattice,
    'Strokes': n6_strokes,
    'Weird': n6_weird,
    'Carlson': carlson_tiles,
}

# Create sidebar for controls
with st.sidebar:
    st.header('Pattern Controls')

    # Tile set selection
    tile_set = st.selectbox(
        'Tile Set',
        options=list(TILE_SETS.keys()),
        index=1,  # n6_circles by default
    )

    # Canvas dimensions
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input('Width', min_value=200, max_value=2560, value=800, step=100)
    with col2:
        height = st.number_input('Height', min_value=200, max_value=2000, value=800, step=100)

    # Tile parameters
    nlayers = st.number_input('Layers', min_value=1, max_value=6, value=2)
    tilew = st.slider('Tile Size', min_value=20, max_value=300, value=100, step=20)
    chance = st.slider('Split Chance', min_value=0.0, max_value=1.0, value=0.45, step=0.05)

    # Colors
    bg_color = st.color_picker('Background Color', value='#335495')
    fg_color = st.color_picker('Foreground Color', value='#243b6a')

    # Additional controls
    seed = st.number_input('Random Seed', value=42)
    grid = st.checkbox('Show Grid', value=False)

    # Add a download button
    download = st.button('Generate for Download')

# Main content area
try:
    # Generate pattern with current parameters
    pattern = multiscale_truchet(
        tiles=TILE_SETS[tile_set],
        width=width,
        height=height,
        tilew=tilew,
        nlayers=nlayers,
        chance=chance,
        bg=bg_color,
        fg=fg_color,
        grid=grid,
        seed=seed,
        format='png',  # Force PNG format for consistent display
    )

    # Display the pattern (use width='content' per request)
    if pattern.pngio is not None:
        st.image(pattern.pngio, width='content')

    # Handle download if requested
    if download:
        # Use the currently displayed PNG bytes when available to avoid re-rendering.
        data_bytes = None
        if getattr(pattern, 'pngio', None) is not None:
            try:
                data_bytes = pattern.pngio.getvalue()
            except Exception:
                data_bytes = None

        if data_bytes is None:
            # Fallback: render to memory and use that
            pattern_mem = multiscale_truchet(
                tiles=TILE_SETS[tile_set],
                width=width,
                height=height,
                tilew=tilew,
                nlayers=nlayers,
                chance=chance,
                bg=bg_color,
                fg=fg_color,
                grid=grid,
                seed=seed,
                format='png',
                output=None,
            )
            if getattr(pattern_mem, 'pngio', None) is not None:
                data_bytes = pattern_mem.pngio.getvalue()

        if data_bytes:
            # sanitize tile_set label for a filename
            def _sanitize(name: str) -> str:
                # Replace any sequence of non-alphanumeric, dot, underscore, or dash with underscore
                s = name.replace(' ', '_')
                s = re.sub(r"[^A-Za-z0-9._-]+", '_', s)
                return s.strip(' _').lower() or 'tiles'

            safe_label = _sanitize(tile_set)
            filename = f'truchet_{safe_label}_{seed}_{width}x{height}.png'
            st.sidebar.download_button(
                label='Download PNG',
                data=data_bytes,
                file_name=filename,
                mime='image/png',
                icon=':material/download:',
            )
        else:
            st.sidebar.error('Failed to create PNG for download.')

except Exception as e:
    st.error(f'Error generating pattern: {str(e)}')
