"""
Custom Button Component for Lunar Loot
Uses custom button images with click animations
"""

import streamlit as st
import base64
import os

def load_button_image(button_name):
    """Load button image and convert to base64"""
    button_path = os.path.join("ui_assets", "buttons", f"{button_name}.png")
    try:
        with open(button_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

def custom_button(button_type="launch", key=None):
    """
    Create a custom button with image and click animation
    
    Args:
        button_type: "launch", "begin", or "mission"
        key: Unique key for the button
    
    Returns:
        bool: True if button was clicked
    """
    
    # Map button types to image files
    button_images = {
        "launch": "Lunar_ Loot_Button",
        "begin": "Begin_Mission",
        "mission": "Mission_Button"
    }
    
    if button_type not in button_images:
        button_type = "launch"
    
    # Load button image
    img_base64 = load_button_image(button_images[button_type])
    
    if not img_base64:
        # Fallback to regular Streamlit button
        return st.button(button_type.title(), key=key)
    
    # Generate unique ID for this button
    button_id = f"custom_btn_{key or button_type}"
    
    # Create clickable button with image and animation
    button_html = f"""
    <style>
    .custom-button-{button_id} {{
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
        border: none;
        background: none;
        padding: 0;
        margin: 10px auto;
        display: block;
    }}
    
    .custom-button-{button_id}:hover {{
        transform: translateY(-3px);
        filter: brightness(1.2);
    }}
    
    .custom-button-{button_id}:active {{
        transform: translateY(2px) scale(0.98);
        filter: brightness(0.9);
    }}
    
    .custom-button-{button_id} img {{
        max-width: 100%;
        height: auto;
        display: block;
    }}
    </style>
    
    <div class="custom-button-{button_id}" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: '{button_id}_clicked'}}, '*')">
        <img src="data:image/png;base64,{img_base64}" alt="{button_type} button">
    </div>
    """
    
    # Display button
    st.markdown(button_html, unsafe_allow_html=True)
    
    # Check if button was clicked using session state
    if f'{button_id}_clicked' not in st.session_state:
        st.session_state[f'{button_id}_clicked'] = False
    
    # Use Streamlit's form or button underneath (invisible) for actual click handling
    # This is a workaround since HTML buttons can't directly trigger Streamlit reruns
    clicked = st.button(f"__{button_type}__", key=f"hidden_{button_id}", 
                        help=f"Click the {button_type} button above",
                        type="primary")
    
    return clicked


def image_button(image_path, key=None, width=None):
    """
    Generic image button component
    
    Args:
        image_path: Path to button image
        key: Unique key for the button
        width: Optional width in pixels
    
    Returns:
        bool: True if button was clicked
    """
    try:
        with open(image_path, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return st.button("Button", key=key)
    
    button_id = f"img_btn_{key or 'default'}"
    width_style = f"max-width: {width}px;" if width else "max-width: 100%;"
    
    button_html = f"""
    <style>
    .image-button-{button_id} {{
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
        {width_style}
    }}
    
    .image-button-{button_id}:hover {{
        transform: translateY(-3px);
        filter: brightness(1.2);
    }}
    
    .image-button-{button_id}:active {{
        transform: translateY(2px) scale(0.98);
        filter: brightness(0.9);
    }}
    
    .image-button-{button_id} img {{
        width: 100%;
        height: auto;
        display: block;
    }}
    </style>
    
    <div class="image-button-{button_id}">
        <img src="data:image/png;base64,{img_base64}" alt="button">
    </div>
    """
    
    st.markdown(button_html, unsafe_allow_html=True)
    
    # Hidden button for click handling
    return st.button(f"__{key}__", key=f"hidden_{button_id}", type="primary")
