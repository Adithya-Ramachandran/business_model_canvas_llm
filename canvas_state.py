# canvas_state.py

import streamlit as st
import json
import os
from constants import CANVAS_FILE


def initialize_canvas_state(reset=False):
    """Initializes or resets the canvas data in Streamlit's session_state."""
    if 'canvas_data' not in st.session_state or reset:
        st.session_state.canvas_data = {
            "business_idea_description": "",
            "target_groups_customers": "",
            "target_groups_users": "",
            "brand_messages_dna": "",
            "offerings_products_services": "",
            "resources_key_internal_assets": "",
            "partners_delivery": "",
            "primary_customer_segment": "",
            "jobs_to_get_done_functional": "",
            "jobs_to_get_done_emotional": "",
            "pains_list": "",
            "gains_list": "",
            "channels_customer": "",
            "core_value": "",
            "channels_partner": "",
            "unfair_advantage": "",
            "relationships_types": "",
            "processes_internal": "",
            "profit_pattern": "",
            "profit_revenue_streams": "",
            "profit_costs": "",
            "profit_investments": "",
            # --- New VPC Fields ---
            "gain_creators": "",
            "pain_relievers": "",
        }
        for key, value in st.session_state.canvas_data.items():
            if key not in st.session_state:
                st.session_state[key] = value

        if 'llm_chat_history' not in st.session_state or reset:
            st.session_state.llm_chat_history = []


def update_canvas_data_from_session():
    """Updates st.session_state.canvas_data from individual text area keys."""
    if 'canvas_data' in st.session_state:
        for key in st.session_state.canvas_data.keys():
            st.session_state.canvas_data[key] = st.session_state.get(key, "")


def save_canvas_to_file():
    """Saves the current canvas state to a JSON file."""
    update_canvas_data_from_session()
    data_to_save = st.session_state.get('canvas_data', {})
    try:
        with open(CANVAS_FILE, "w") as f:
            json.dump(data_to_save, f, indent=4)
        st.success(f"Canvas saved to {CANVAS_FILE}!")
    except Exception as e:
        st.error(f"Error saving canvas: {e}")


def load_canvas_from_file():
    """Loads a canvas state from a JSON file and updates session_state."""
    if os.path.exists(CANVAS_FILE):
        try:
            with open(CANVAS_FILE, "r") as f:
                loaded_data = json.load(f)
            # Initialize with default values first to ensure new fields exist
            initialize_canvas_state()
            # Then, update with loaded data
            st.session_state.canvas_data.update(loaded_data)

            for key, value in st.session_state.canvas_data.items():
                st.session_state[key] = value

            st.session_state.llm_chat_history = []
            st.rerun()
        except Exception as e:
            st.error(f"Error loading canvas: {e}")
    else:
        st.warning(f"No saved canvas found at {CANVAS_FILE}.")