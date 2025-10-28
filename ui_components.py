# ui_components.py

import streamlit as st

def display_card(unique_key, title, content_placeholder="", height="auto", border_color="transparent", title_size="p",
                 border_style="solid", text_color="#F0F2F6", bg_color="#262730", outer_margin_bottom="0px",
                 is_business_description=False, widget_key_prefix=""): # <-- ADD THIS NEW ARGUMENT
    """Displays a generic card-like section with a title and a text_area for user input."""

    title_html = ""
    if title_size == "h4":
        title_html = f"<h4 style='color: #F0F2F6;'>{title}</h4>"
    elif title_size == "h5":
        title_html = f"<h5 style='color: #F0F2F6;'>{title}</h5>"
    elif title_size == "bold":
        title_html = f"<strong style='color: #F0F2F6;'>{title}</strong>"
    else:
        title_html = f"<p style='margin-bottom: 0px; color: #F0F2F6;'><strong>{title}</strong></p>"

    if not is_business_description:
        st.markdown(title_html, unsafe_allow_html=True)
    elif is_business_description:
        st.markdown("", unsafe_allow_html=True)

    st.markdown(f"""
        <style>
            .stTextArea[data-testid="stTextarea-{widget_key_prefix}{unique_key}"] > label {{
                display: none;
            }}
            .stTextArea[data-testid="stTextarea-{widget_key_prefix}{unique_key}"] {{
                border: 1px {border_style} {border_color};
                border-radius: 5px;
                background-color: {bg_color};
                margin-bottom: {outer_margin_bottom};
            }}
            .stTextArea[data-testid="stTextarea-{widget_key_prefix}{unique_key}"] textarea {{
                min-height: {height}px;
                color: {text_color};
                font-size: 0.9em;
                padding: 10px;
                border: none;
                resize: vertical;
                box-shadow: none;
                background-color: transparent;
            }}
            .stTextArea[data-testid="stTextarea-{widget_key_prefix}{unique_key}"] textarea::placeholder {{
                color: rgba(240, 242, 246, 0.6);
            }}
        </style>
    """, unsafe_allow_html=True)

    # The widget's key is now unique, but the session_state key used for data is the original.
    # We use a callback to ensure changes in the prefixed widget update the main session state.
    def update_state():
        st.session_state[unique_key] = st.session_state[f"{widget_key_prefix}{unique_key}"]

    st.text_area(
        label=f"Content for {title}",
        value=st.session_state.get(unique_key, content_placeholder),
        height=height if isinstance(height, int) else 100,
        key=f"{widget_key_prefix}{unique_key}", # <-- MAKE THE WIDGET KEY UNIQUE
        on_change=update_state if widget_key_prefix else None # <-- ENSURE DATA SYNCS BACK
    )