import streamlit as st
import tempfile
from pathlib import Path

from truchet_viewer import multiscale_truchet
from truchet_viewer.n6 import n6_tiles, n6_circles, n6_connected, n6_filled, n6_lattice, n6_strokes, n6_weird
from truchet_viewer.carlson import carlson_tiles

# Set page config
st.set_page_config(page_title='Truchet Pattern Generator', layout='wide')

# Title
st.title('Truchet Pattern Generator')

# Create dictionary mapping tile set names to actual tile lists
TILE_SETS = {
    'all tiles': n6_tiles,
    'circles': n6_circles,
    'connected': n6_connected,
    'filled': n6_filled,
    'lattice': n6_lattice,
    'strokes': n6_strokes,
    'weird': n6_weird,
    'carlson': carlson_tiles,
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
        width = st.number_input('Width', min_value=200, max_value=2000, value=800, step=100)
    with col2:
        height = st.number_input('Height', min_value=200, max_value=2000, value=800, step=100)

    # Tile parameters
    nlayers = st.number_input('Layers', min_value=1, max_value=6, value=3)
    tilew = st.slider('Tile Size', min_value=20, max_value=300, value=100, step=20)
    chance = st.slider('Split Chance', min_value=0.0, max_value=1.0, value=0.45, step=0.05)

    # Colors
    bg_color = st.color_picker('Background Color', value='#335495')
    fg_color = st.color_picker('Foreground Color', value='#243b6a')

    # Additional controls
    seed = st.number_input('Random Seed', value=42)
    grid = st.checkbox('Show Grid', value=False)

    # Add a download button
    download = st.button('Download Image')

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

    # Display the pattern
    if pattern.pngio is not None:
        st.image(pattern.pngio, width='content')

    # Handle download if requested
    if download:
        # Create a temporary file for download
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            pattern.write_to(tmp.name)

            # Offer the file for download
            with open(tmp.name, 'rb') as f:
                st.download_button(
                    label='Download PNG', data=f.read(), file_name=f'truchet_{tile_set}_{seed}.png', mime='image/png'
                )

            # Clean up
            Path(tmp.name).unlink()

except Exception as e:
    st.error(f'Error generating pattern: {str(e)}')
